import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt

from bluebelt.core.checks import check_kwargs

import bluebelt.core.decorators

import bluebelt.core.index
import bluebelt.core.series
import bluebelt.core.dataframe

import warnings

def resolution_methods(cls):

    def sum(self):
        result = self.grouped.sum(min_count=1)
        return result

    def mean(self):
        result = self.grouped.mean()
        return result

    def var(self):
        result = self.grouped.var()
        return result
            
    def std(self):
        result = self.grouped.std()
        return result

    def min(self):
        result = self.grouped.min()
        return result

    def max(self):
        result = self.grouped.max()
        return result

    
    def count(self):
        result = self.grouped.count()
        return result
    
    def value_range(self):
        result = self.grouped.apply(lambda x: x.max() - x.min())
        return result

    def diff_quantity(self):
        # if this week > last week: this week - last week / this week
        # if this week < last week: last week - this week / last week

        if isinstance(self._obj, pd.Series):
            result = (self.grouped.sum() - self.grouped.sum().shift()).abs() / np.maximum(self.grouped.sum(), self.grouped.sum().shift().fillna(0))
        else:
            result = (self.grouped.sum().sum(axis=1) - self.grouped.sum().sum(axis=1).shift()).abs() / np.maximum(self.grouped.sum().sum(axis=1), self.grouped.sum().sum(axis=1).shift().fillna(0))

        return result

    def diff_distribution(self, **kwargs):

        index_groups = self.grouped.obj.index.names
        _level = self.level[-1] if isinstance(self.level, list) else self.level
        group = index_groups[self.grouped.obj.index.names.index(_level) + 1]
            
        if self.grouped.obj.index.names[-1] != _level:
            if isinstance(self._obj, pd.Series):
                result = self.grouped.apply(lambda s: s.groupby(group).sum()).unstack(level=-1)
                result = pd.Series((result - result.shift().multiply((result.sum(axis=1) / result.sum(axis=1).shift()), axis=0)).abs().sum(axis=1, min_count=1) / (result.sum(axis=1) * 2), name='distribution')    
                
            else:
                result = self.grouped.apply(lambda s: s.groupby(group).sum()).sum(axis=1).unstack(level=-1)
                result = pd.Series((result - result.shift().multiply((result.sum(axis=1) / result.sum(axis=1).shift()), axis=0)).abs().sum(axis=1, min_count=1) / (result.sum(axis=1) * 2), name='distribution')
        else:
            result = pd.Series(index=self.grouped.sum().index, data=[0]*self.grouped.sum().size, name=self._obj.name)
        
        return result

    def diff_skills(self, **kwargs):
    
        index_groups = self.grouped.obj.index.names
        _level = self.level[-1] if isinstance(self.level, list) else self.level
        group = index_groups[self.grouped.obj.index.names.index(_level) + 1]
            
        if self.grouped.obj.index.names[-1] != _level and isinstance(self._obj, pd.DataFrame):
            this_week = self._obj.groupby(group).shift(0)
            last_week = self._obj.groupby(group).shift(1)

            _ratio = last_week.sum(axis=1).divide(this_week.sum(axis=1))

            # copy _ratio series to ratio colums (mirror this week)
            ratio = pd.DataFrame(index=_ratio.index, data=[])
            for column in this_week.columns:
                ratio[column] = pd.Series(_ratio, name=column)

            # normalise this week
            this_week_normalised = ratio.multiply(this_week)
            absolute_diff = (this_week_normalised - last_week).abs().sum(axis=1)
            absolute_diff = absolute_diff.groupby(['year', 'week']).sum()
            this_week_normalised = this_week_normalised.sum(axis=1).groupby(['year', 'week']).sum()

            # divide by 2 because 100% shift of skills would otherwise result in 200%; 100% from skill x + 100% to skill y
            result = (absolute_diff / (this_week_normalised * 2))
            
        else:
            result = pd.Series(index=self.grouped.sum().index, data=[0]*self.grouped.sum().size, name=self._obj.name)
        
        return result

    setattr(cls, 'sum', sum)
    setattr(cls, 'mean', mean)
    setattr(cls, 'var', var)
    setattr(cls, 'std', std)
    setattr(cls, 'min', min)
    setattr(cls, 'max', max)
    setattr(cls, 'count', count)
    setattr(cls, 'value_range', value_range)
    setattr(cls, 'diff_quantity', diff_quantity)
    setattr(cls, 'diff_distribution', diff_distribution)
    setattr(cls, 'diff_skills', diff_skills)
    return cls

@bluebelt.core.decorators.class_methods
@resolution_methods
class GroupByDatetimeIndex():
    """
    Group a pandas.Series or pandas.DataFrame by DateTime index and apply a specific function.
        arguments
        series: pandas.Series
        how: str
            a string with date-time keywords that can be parsed to group the index
            keywords:
            
            default value "week"

        Apply one of the following functions:
            .sum()
            .mean()
            .min()
            .max()
            .std()
            .value_range()
            .count()
            .subsize_count()

        e.g. series.blue.data.group_index(how="week").sum()
        
    """
    
    def __init__(self, _obj, level="week", complete=False, **kwargs):

        self._obj = _obj
        self.level = level
        self.complete = complete
        self.nrows = self._obj.shape[0]
        self.calculate(**kwargs)

    def calculate(self, **kwargs):
        
        # convert to pd.MultiIndex
        if isinstance(self._obj, pd.Series):
            if 'month' in self.level:
                self._obj = bluebelt.core.series.SeriesToolkit(self._obj).index.to_datetimemultiindex()
            else:
                self._obj = bluebelt.core.series.SeriesToolkit(self._obj).index.to_isodatetimemultiindex()
        elif isinstance(self._obj, pd.DataFrame):
            if 'month' in self.level:
                self._obj = bluebelt.core.dataframe.DataFrameToolkit(self._obj).index.to_datetimemultiindex()
            else:
                self._obj = bluebelt.core.dataframe.DataFrameToolkit(self._obj).index.to_isodatetimemultiindex()

        # check the index type
        if not isinstance(self._obj.index, pd.MultiIndex):
            # convert to isodatetimemultiindex or datetimemultiindex
            if self.iso:
                index = bluebelt.core.index.IndexToolkit(self._obj.index, **kwargs).iso()
            else:
                index = bluebelt.core.index.IndexToolkit(self._obj.index, **kwargs).dt()
        else:
            index = self._obj.index

        self.grouped = self._obj.groupby(level=self.level)

    def __str__(self):
        return ""
    
    def __repr__(self):
        return self.grouped.__repr__()


    def subsize_count(self, count=3, size=1):

            """
            Count the number of times a list of <count> items with size <size> fit in the groupby object (which is a pandas Series)
            e.g.
            groupby object: pd.Series([10, 8, 3, 3, 5])
            count = 3
            size = 1

            returns 9

            step 0: (3, 3, 5, 8, 10)
            step 1: (3, 3, 4, 7, 9)
            step 2: (3, 3, 3, 6, 8)
            step 3: (2, 3, 3, 5, 7)
            step 4: (2, 2, 3, 4, 6)
            step 5: (2, 2, 2, 3, 5)
            step 6: (1, 2, 2, 2, 4)
            step 7: (1, 1, 1, 2, 3)
            step 8: (0, 1, 1, 1, 2)
            step 9: (0, 0, 0, 1, 1)

            """
            if isinstance(count, (float, int)):
                count = [int(count)]
            
            result = {}
            for c in count:
                result[c] = self.grouped.apply(lambda x: _subsize_count(series=x, count=c, size=size)).values
            result = pd.DataFrame(result, index=self.grouped.groups.keys()) #self.grouped.apply(lambda x: _subsize_count(series=x, count=count, size=size))
            
            if len(count) == 2:
                _dict = {}
                for val in range(int(result.values.min()), int(result.values.max())):

                    under = np.where(val < result.iloc[:,0:2].min(axis=1), result.iloc[:,0:2].min(axis=1) - val, 0)
                    over = np.where(val > result.iloc[:,0:2].max(axis=1), val - result.iloc[:,0:2].max(axis=1), 0)
                    _dict[val] = under + over

                # get the keys with the most zeros
                _o_dict = {key: len([x for x in value if x == 0]) for key, value in _dict.items()}
                most_zeros = _o_dict.get(max(_o_dict, key=_o_dict.get))

                _dict = {key: value for (key, value) in _dict.items() if _o_dict.get(key) == most_zeros}

                # get the smallest sum
                _o_dict = {key: sum(value) for (key, value) in _dict.items()}
                min_val = _o_dict.get(min(_o_dict, key=_o_dict.get))
                _dict = {key: value for (key, value) in _dict.items() if _o_dict.get(key) == min_val}

                # build the optimum series and merge with result
                optimum = tuple(_dict.keys()) if len(_dict.keys()) > 1 else list(_dict.keys())[0]
                optimum = pd.Series(index=result.index, data=[optimum]*result.shape[0], name='optimum')

                result = result.merge(optimum, left_index=True, right_index=True)

            return result

def _subsize_count(series, count=3, size=1):
    series = pd.Series(series)/size
    result = series.sum()*count
    for i in range(count, 0, -1):
        result = min(result, math.floor(series.nsmallest(len(series) - count + i).sum() / i))
    return result

def _subseries_count(series, subseries=None, **kwargs):
    series = pd.Series(series)
    subseries = pd.Series(subseries)
    result=series.sum()*subseries.sum()
    for i in range(len(subseries), 0, -1):
        result = min(result, math.floor(series.nsmallest(len(series) - len(subseries) + i).sum() / subseries.nsmallest(i).sum()))
    return result