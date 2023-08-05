"""
Includes base class and functions for data preprocessing and loading.
"""

from difflib import SequenceMatcher
from abc import abstractmethod, ABCMeta

import cloudpickle
import numpy as np
import pandas as pd
from pandas.errors import MergeError
from sklearn.model_selection import ParameterGrid
from sklearn.utils import check_scalar


def _cols(x):
    return [f'{col}_team{x}' for col in ('home', 'away')]


def _create_names_mapping_table(data_source1, data_source2):
    """Map most similar teams names between two data sources."""

    keys = ['date', 'league', 'division', 'year']

    # Generate teams names combinations
    names_combinations = pd.merge(
        data_source1[keys + _cols('')], data_source2[keys + _cols('')], on=keys
    )

    # Calculate similarity index
    similarity = names_combinations.apply(
        lambda row: SequenceMatcher(None, row.home_team_x, row.home_team_y).ratio()
        + SequenceMatcher(None, row.away_team_x, row.away_team_y).ratio(),
        axis=1,
    )

    # Append similarity index
    names_combinations_similarity = pd.concat(
        [names_combinations[_cols('_x') + _cols('_y')], similarity], axis=1
    )

    # Filter correct matches
    indices = names_combinations_similarity.groupby(_cols('_x'))[0].idxmax().values
    names_matching = names_combinations.take(indices)

    # Teams matching
    matching1 = names_matching.loc[:, ['home_team_x', 'home_team_y']].drop_duplicates()
    matching2 = names_matching.loc[:, ['away_team_x', 'away_team_y']].drop_duplicates()
    matching1.columns = matching2.columns = cols = ['team1', 'team2']
    matching = matching1.append(matching2)
    similarity = matching.apply(
        lambda row: SequenceMatcher(None, row.team1, row.team2).ratio(), axis=1
    )
    names_combinations_similarity = pd.concat(
        [matching, similarity], axis=1
    ).reset_index(drop=True)
    indices = names_combinations_similarity.groupby('team1')[0].idxmax()
    names_mapping = names_combinations_similarity.take(indices)[cols].reset_index(
        drop=True
    )

    return names_mapping


def _combine_odds(odds):
    """Combine the odds of different outcomes."""
    combined_odds = 1 / (1 / odds).sum(axis=1)
    return combined_odds


class _BaseDataLoader(metaclass=ABCMeta):
    """The base class for dataloaders.

    Warning: This class should not be used directly. Use the derive classes
    instead.
    """

    def __init__(self, param_grid=None):
        self.param_grid = param_grid

    @classmethod
    @abstractmethod
    def _get_schema(cls):
        return

    @classmethod
    @abstractmethod
    def _get_outcomes(cls):
        return

    @classmethod
    @abstractmethod
    def _get_params(cls):
        return

    @abstractmethod
    def _get_data(self):
        return

    def _check_param_grid(self):
        """Check the parameters grid."""
        if self.param_grid is not None:
            full_param_grid_df = pd.DataFrame(self._get_params())
            try:
                param_grid_df = pd.concat(
                    [
                        pd.merge(
                            pd.DataFrame(ParameterGrid(params)),
                            full_param_grid_df,
                            how='left',
                        )
                        for params in ParameterGrid(self.param_grid).param_grid
                    ]
                )
            except MergeError:
                raise ValueError(
                    'Parameter grid includes parameters names '
                    'not not allowed by available data'
                )
            error_msg = 'Parameter grid includes values not allowed by available data.'
            param_grid_df = pd.merge(param_grid_df, full_param_grid_df, how='left')
            if np.any(pd.merge(param_grid_df, full_param_grid_df, how='left').isna()):
                raise ValueError(error_msg)
            param_grid_df = pd.merge(param_grid_df, full_param_grid_df)
            if param_grid_df.size == 0:
                raise ValueError(error_msg)
            else:
                self.param_grid_ = ParameterGrid(
                    [
                        {k: [v] for k, v in row.to_dict().items()}
                        for _, row in param_grid_df.iterrows()
                    ]
                )
        else:
            self.param_grid_ = self._get_params()
        return self

    def _check_schema(self):
        """Check the schema."""
        schema = self._get_schema()
        self.schema_ = [] if schema is None else schema
        if any([data_type is None for *_, data_type in self.schema_]):
            raise ValueError('All columns in schema should include a data type.')
        self.schema_odds_cols_ = pd.Index(
            [col for col, _ in self.schema_ if col.split('__')[-1] == 'odds'],
            dtype=object,
        )
        self.schema_output_cols_ = pd.Index(
            [col for col, _ in self.schema_ if len(col.split('__')) == 2],
            dtype=object,
        )
        self.schema_input_cols_ = pd.Index(
            [col for col, _ in self.schema_ if col not in self.schema_output_cols_],
            dtype=object,
        )
        return self

    def _check_outcomes(self):
        """Check the outcomes."""
        outcomes = self._get_outcomes()
        self.outcomes_ = [] if outcomes is None else outcomes
        return self

    def _check_odds_type(self, odds_type):
        """Check the odds type."""
        self.odds_type_ = odds_type
        odds_cols = [
            col
            for col in self.schema_odds_cols_
            if col.split('__')[0] == self.odds_type_
        ]
        if self.odds_type_ is not None:
            if not isinstance(self.odds_type_, str):
                raise TypeError(
                    'Parameter `odds_type` should be a string or None. '
                    f'Got {type(self.odds_type_).__name__} instead.'
                )
            if not odds_cols:
                raise ValueError(
                    'Parameter `odds_type` should be a prefix of available odds '
                    f'columns. Got {self.odds_type_} instead.'
                )
        return self

    def _check_drop_na_thres(self, drop_na_thres):
        """Check drop na threshold."""
        self.drop_na_thres_ = drop_na_thres if drop_na_thres is not None else 0.0
        check_scalar(
            self.drop_na_thres_, 'drop_na_thres', float, min_val=0.0, max_val=1.0
        )
        return self

    def _check_data(self):
        """Check the data."""
        data = self._get_data()
        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                f'Data should be a pandas dataframe. Got {type(data).__name__} instead.'
            )
        if data.size == 0:
            raise ValueError('Data should be a pandas dataframe with positive size.')
        if 'fixtures' not in data.columns or data['fixtures'].dtype.name != 'bool':
            raise KeyError(
                'Data should include a boolean column `fixtures` to distinguish '
                'between train and fixtures data.'
            )
        if 'date' not in data.columns or data['date'].dtype.name != 'datetime64[ns]':
            raise KeyError(
                'Data should include a datetime column `date` to represent the date.'
            )
        if self.schema_ and not set([col for col, _ in self.schema_]).issuperset(
            data.columns.difference(['fixtures'])
        ):
            raise ValueError('Data contains columns not included in schema.')
        if not set(data.columns).issuperset(pd.DataFrame(self.param_grid_).columns):
            raise ValueError(
                'Data columns should contain the parameters from parameters grid.'
            )
        data = data.set_index('date').sort_values('date')
        self.data_ = data[~data.index.isna()]
        return self

    def _convert_data_types(self, data):
        """Cast the data type of columns."""
        data_types = set([data_type for _, data_type in self.schema_])
        for data_type in data_types:
            converted_cols = list(
                {
                    col
                    for col, selected_data_type in self.schema_
                    if selected_data_type is data_type and col in data.columns
                }
            )
            if converted_cols:
                data_converted_cols = data[converted_cols].fillna(
                    -1 if data_type is int else np.nan
                )
                data.loc[:, converted_cols] = (
                    data_converted_cols.values.astype(data_type)
                    if data_type is not np.datetime64
                    else pd.to_datetime(data_converted_cols.iloc[:, 0])
                )
        return data

    def _drop_na_cols(self, data):

        # Drop columns
        self.dropped_na_cols_ = pd.Index([], dtype=object)
        if self.drop_na_thres_ > 0.0:
            input_cols = data.columns.intersection(self.schema_input_cols_)
            data_dropped_na_cols = data[input_cols].dropna(
                axis=1, thresh=int(data.shape[0] * self.drop_na_thres_)
            )
            self.dropped_na_cols_ = pd.Index(
                [
                    col
                    for col in data[input_cols]
                    if col not in data_dropped_na_cols.columns
                ],
                dtype=object,
            )
        if data.columns.difference(self.dropped_na_cols_).size == 0:
            raise ValueError(
                'All columns were removed. Set `drop_na_thres` parameter to a '
                'lower value.'
            )

        return self

    def _extract_training_cols(self, data):
        self.input_cols_ = pd.Index(
            [
                col
                for col in data.columns
                if col in self.schema_input_cols_ and col not in self.dropped_na_cols_
            ],
            dtype=object,
        )
        self.output_cols_ = pd.Index(
            [col for col in data.columns if col in self.schema_output_cols_],
            dtype=object,
        )
        self.odds_cols_ = pd.Index(
            sorted(
                [
                    col
                    for col in data.columns.append(self.dropped_na_cols_)
                    if col in self.schema_odds_cols_
                    and (col.split('__')[0] == self.odds_type_)
                    and any(
                        [
                            col.split('__')[1] == outcome_col.split('__')[0]
                            and any(
                                [
                                    outcome_col.split('__')[1]
                                    == output_col.split('__')[1]
                                    for output_col in self.output_cols_
                                ]
                            )
                            for outcome_col, _ in self.outcomes_
                        ]
                    )
                ],
                key=lambda col: col.split('__')[1],
            )
            if self.odds_type_ is not None
            else [],
            dtype=object,
        )

    def _extract_train_data(self, drop_na_thres=None, odds_type=None):

        # Checks parameters
        self._check_param_grid()
        self._check_schema()
        self._check_outcomes()
        self._check_drop_na_thres(drop_na_thres)
        self._check_odds_type(odds_type)

        # Extract training data
        self._check_data()
        mask = self.data_['fixtures']
        data = self.data_[~mask].drop(columns=['fixtures'])

        # Filter data
        data = (
            pd.merge(data.reset_index(), pd.DataFrame(self.param_grid_))
            .set_index('date')
            .sort_values('date')
        )
        if data.size == 0:
            raise ValueError('Parameter grid did not select any training data.')

        # Drop missing values
        self._drop_na_cols(data)

        # Extract training data columns
        data_dropped_na_cols = data.drop(columns=self.dropped_na_cols_)
        self._extract_training_cols(data_dropped_na_cols)

        return data

    def _extract_targets(self, data):
        schema_odds_keys = {col.split('__')[1] for col in self.odds_cols_}
        schema_output_keys = {col.split('__')[1] for col in self.output_cols_}
        Y = []
        output_cols = []
        for col, func in sorted(self.outcomes_, key=lambda tpl: tpl[0]):
            odds_key, output_key = col.split('__')
            if (
                odds_key in schema_odds_keys if schema_odds_keys else True
            ) and output_key in schema_output_keys:
                output_cols.extend(
                    [col for col in data.columns if col.split('__')[-1] == output_key]
                )
                Y.append(pd.Series(func(data), name=col))
        dropna = data[list(set(output_cols))].isna().sum(axis=1).astype(bool).values
        Y = pd.concat(Y, axis=1).reset_index(drop=True)[~dropna] if Y else None
        return Y

    def extract_train_data(self, drop_na_thres=0.0, odds_type=None):
        """Extract the training data.

        Read more in the :ref:`user guide <user_guide>`.

        It returns historical data that can be used to create a betting
        strategy based on heuristics or machine learning models.

        The data contain information about the matches that belong
        in two categories. The first category includes any information
        known before the start of the match, i.e. the training data ``X``
        and the odds data ``O``. The second category includes the outcomes of
        matches i.e. the multi-output targets ``Y``.

        The method selects only the the data allowed by the ``param_grid``
        parameter of the initialization method
        :func:`~sportsbet.datasets._base._BaseDataLoader.__init__`.
        Additionally, columns with missing values are dropped through the
        ``drop_na_thres`` parameter, while the types of odds returned is defined
        by the ``odds_type`` parameter.

        Parameters
        ----------
        drop_na_thres : float, default=0.0
            The threshold that specifies the input columns to drop. It is a float in
            the :math:`[0.0, 1.0]` range. Higher values result in dropping more values.
            The default value ``drop_na_thres=0.0`` keeps all columns while the
            maximum value ``drop_na_thres=1.0`` keeps only columns with non
            missing values.

        odds_type : str, default=None
            The selected odds type. It should be one of the available odds columns
            prefixes returned by the method
            :func:`~sportsbet.datasets._base._BaseDataLoader.get_odds_types`. If
            ``odds_type=None`` then no odds are returned.

        Returns
        -------
        (X, Y, O) : tuple of :class:`~pandas.DataFrame` objects
            Each of the components represent the training input data ``X``, the
            multi-output targets ``Y`` and the corresponding odds ``O``, respectively.
        """

        # Extract training data
        data = self._extract_train_data(drop_na_thres, odds_type)

        # Extract targets
        Y = self._extract_targets(data)

        # Convert data types
        data = self._convert_data_types(data).iloc[Y.index]

        return (
            data[self.input_cols_],
            Y.reset_index(drop=True),
            data[self.odds_cols_].reset_index(drop=True)
            if self.odds_cols_.size
            else None,
        )

    def extract_fixtures_data(self):
        """Extract the fixtures data.

        Read more in the :ref:`user guide <user_guide>`.

        It returns fixtures data that can be used to make predictions for
        upcoming matches based on a betting strategy.

        Before calling the
        :func:`~sportsbet.datasets._BaseDataLoader.extract_fixtures_data` method for
        the first time, the :func:`~sportsbet.datasets._BaseDataLoader.extract__data`
        should be called, in order to match the columns of the input, output and
        odds data.

        The data contain information about the matches known before the
        start of the match, i.e. the training data ``X`` and the odds
        data ``O``. The multi-output targets ``Y`` is always equal to ``None``
        and are only included for consistency with the method
        :func:`~sportsbet.datasets._base._BaseDataLoader.extract_train_data`.

        The ``param_grid`` parameter of the initialization method
        :func:`~sportsbet.datasets._base._BaseDataLoader.__init__` has no effect
        on the fixtures data.

        Returns
        -------
        (X, None, O) : tuple of :class:`~pandas.DataFrame` objects
            Each of the components represent the fixtures input data ``X``, the
            multi-output targets ``Y`` equal to ``None`` and the
            corresponding odds ``O``, respectively.
        """

        # Extract fixtures data
        if hasattr(self, 'data_'):
            mask = self.data_['fixtures']
        else:
            raise AttributeError(
                'Extract the training data before extracting the fixtures data.'
            )
        data = self.data_[mask].drop(columns=['fixtures'])

        # Convert data types
        data = self._convert_data_types(data)

        # Remove past data
        data = data[data.index >= pd.to_datetime('today').floor('D')]

        return (
            data[self.input_cols_],
            None,
            data[self.odds_cols_].reset_index(drop=True)
            if self.odds_cols_.size
            else None,
        )

    def save(self, path):
        """Save the dataloader object.

        Parameters
        ----------
        path : str
            The path to save the object.

        Returns
        -------
        self: object
            The dataloader object.
        """
        with open(path, 'wb') as file:
            cloudpickle.dump(self, file)
        return self

    @classmethod
    def get_all_params(cls):
        """Get the available parameters.

        It can be used to get the allowed names and values for the
        ``param_grid`` parameter of the dataloader object.

        Returns
        -------
        param_grid: list
            A list of all allowed params and values.
        """
        all_params = pd.DataFrame(cls._get_params())
        all_params = [
            {k: [v] for k, v in params.to_dict().items()}
            for _, params in all_params.sort_values(list(all_params.columns)).iterrows()
        ]
        return all_params

    @classmethod
    def get_odds_types(cls):
        """Get the available odds types.

        It can be used to get the allowed odds types of the dataloader's  class method
        :func:`~sportsbet.datasets._base._BaseDataLoader.extract_train_data`.

        Returns
        -------
        odds_types: list of str
            A list of available odds types.
        """
        schema = cls._get_schema()
        schema = [] if schema is None else schema
        return sorted(
            {col.split('__')[0] for col, _ in schema if col.split('__')[-1] == 'odds'}
        )


def load(path):
    """Load the dataloader object.

    Parameters
    ----------
    path : str
        The path of the dataloader pickled file.

    Returns
    -------
    dataloader: object
        The dataloader object.
    """
    with open(path, 'rb') as file:
        dataloader = cloudpickle.load(file)
    return dataloader
