import pandas as pd
import numpy as np
import scipy.stats as stats


import bluebelt.datetime.dt

import bluebelt.statistics.std

import bluebelt.data.resolution

import bluebelt.analysis.ci
import bluebelt.statistics.hypothesis_testing
import bluebelt.analysis.pattern
import bluebelt.analysis.forecast
import bluebelt.analysis.planning
import bluebelt.analysis.datetime
import bluebelt.graph.graph
import bluebelt.analysis.performance

import bluebelt.core.decorators
import bluebelt.core.index

@bluebelt.core.decorators.class_methods
@pd.api.extensions.register_series_accessor('blue')
class SeriesToolkit():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        self.index = self.index(self._obj)
        self.statistics = self.statistics(self._obj)
        self.pattern = self.pattern(self._obj)
        self.forecast = self.forecast(self._obj)
        self.planning = self.planning(self._obj)
        self.datetime = self.datetime(self._obj)
        self.data = self.data(self._obj)
        self.graph = self.graph(self._obj)
        self.test = self.test(self._obj)
        self.performance = self.performance(self._obj)

    # first level functions
    
    
    def line(self, **kwargs):
        return bluebelt.graph.graph.line(self._obj, **kwargs)
     
    @bluebelt.core.decorators.class_methods
    class index():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        def to_isodatetimemultiindex(self, level=None, **kwargs):
            index = bluebelt.core.index.IndexToolkit(self._obj.index, **kwargs).to_isodatetimemultiindex(level=level)
            return pd.Series(index=index, data=self._obj.values, dtype=self._obj.dtype, name=self._obj.name)
        iso = to_isodatetimemultiindex

        def to_datetimemultiindex(self, level=None, **kwargs):
            index = bluebelt.core.index.IndexToolkit(self._obj.index, **kwargs).to_datetimemultiindex(level=level)
            return pd.Series(index=index, data=self._obj.values, dtype=self._obj.dtype, name=self._obj.name)
        dt = to_datetimemultiindex

        def groupby(self, **kwargs):
            return bluebelt.data.resolution.GroupByDatetimeIndex(self._obj, **kwargs)      

    
    @bluebelt.core.decorators.class_methods
    class statistics():

        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        # rolling std
        def rolling_std(self, window=7, center=True, **kwargs):
            return bluebelt.statistics.std.RollingStd(self._obj, window=window, center=center, **kwargs)
                
        # standard deviation
        def std_within(self, how=None, observations=2, **kwargs):
            return bluebelt.statistics.std.StdWithin(self._obj, how=how, observations=observations, **kwargs)        

    @bluebelt.core.decorators.class_methods
    class pattern():

        def __init__(self, pandas_obj):
            self._obj = pandas_obj
                
        # patterns
        def polynomial(self, **kwargs):
            return bluebelt.analysis.pattern.Polynomial(self._obj, **kwargs)

        def periodical(self, **kwargs):
            return bluebelt.analysis.pattern.Periodical(self._obj, **kwargs)

    @bluebelt.core.decorators.class_methods
    class forecast():

        def __init__(self, pandas_obj):
            self._obj = pandas_obj
        
        def MAPE(self, **kwargs):
            return bluebelt.analysis.forecast.MAPE(self._obj, **kwargs)

        def WMAPE(self, **kwargs):
            return bluebelt.analysis.forecast.WMAPE(self._obj, **kwargs)

        def SMAPE(self, **kwargs):
            return bluebelt.analysis.forecast.SMAPE(self._obj, **kwargs)

        def MDA(self, **kwargs):
            return bluebelt.analysis.forecast.MDA(self._obj, **kwargs)

        def MPE(self, **kwargs):
            return bluebelt.analysis.forecast.MPE(self._obj, **kwargs)

        mape = MAPE
        wmape = WMAPE
        wMAPE = WMAPE
        smape = SMAPE
        mda = MDA
        mpe = MPE

    @bluebelt.core.decorators.class_methods
    class planning():

        def __init__(self, pandas_obj):
            self._obj = pandas_obj
        
        def effort(self, **kwargs):
            return bluebelt.analysis.planning.Effort(self._obj, **kwargs)

    @bluebelt.core.decorators.class_methods
    class datetime():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        # week day
        def week_day(self, **kwargs):
            return bluebelt.analysis.datetime.WeekDay(self._obj, **kwargs)

        weekday = week_day

        # day of the month
        def month_day(self, **kwargs):
            return bluebelt.analysis.datetime.MonthDay(self._obj, **kwargs)

        day = month_day

        # week of the year
        def week(self, **kwargs):
            return bluebelt.analysis.datetime.Week(self._obj, **kwargs)

        # month of the year
        def month(self, **kwargs):
            return bluebelt.analysis.datetime.Month(self._obj, **kwargs)

        # year
        def year(self, **kwargs):
            return bluebelt.analysis.datetime.Year(self._obj, **kwargs) 

    @bluebelt.core.decorators.class_methods
    class data():

        def __init__(self, pandas_obj):
            self._obj = pandas_obj
                
        def group_index(self, **kwargs):
            return bluebelt.data.resolution.GroupByDatetimeIndex(self._obj, **kwargs)
        
        
    @bluebelt.core.decorators.class_methods
    class graph():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj
        
        def line(self, **kwargs):
            return bluebelt.graph.graph.line(self._obj, **kwargs)

        def scatter(self, **kwargs):
            return bluebelt.graph.graph.scatter(self._obj, **kwargs)

        def area(self, **kwargs):
            return bluebelt.graph.graph.area(self._obj, **kwargs)

        def hist(self, **kwargs):
            return bluebelt.graph.graph.hist(self._obj, **kwargs)
            
        histogram = hist

        def boxplot(self, **kwargs):
            return bluebelt.graph.graph.boxplot(self._obj, **kwargs)
            
    @bluebelt.core.decorators.class_methods
    class test():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        # index
        @property
        def index(self):
            return bluebelt.statistics.hypothesis_testing.index()

        # hypothesis testing
        def normal_distribution(self, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.NormalDistribution(self._obj, alpha=alpha)
        
        normal = normal_distribution

        def dagostino_pearson(self, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.DAgostinoPearson(self._obj, alpha=alpha)
        
        def anderson_darling(self, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.AndersonDarling(self._obj, alpha=alpha)
                
        def one_sample_t(self, popmean=None, confidence=0.95, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.OneSampleT(self._obj, popmean=popmean, confidence=confidence, alpha=alpha, **kwargs)

        def wilcoxon(self, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.Wilcoxon(self._obj, alpha=alpha, **kwargs)
        
    @bluebelt.core.decorators.class_methods
    class performance():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        def summary(self, **kwargs):
            return bluebelt.analysis.performance.Summary(self._obj, **kwargs)
        
        def control_chart(self, **kwargs):
            return bluebelt.analysis.performance.ControlChart(self._obj, **kwargs)
            
        def run_chart(self, alpha=0.05, **kwargs):
            return bluebelt.analysis.performance.RunChart(self._obj, alpha=alpha, **kwargs)

        def process_capability(self, **kwargs):
            return bluebelt.analysis.performance.ProcessCapability(self._obj, **kwargs)
        
        capability = process_capability

        pca = process_capability