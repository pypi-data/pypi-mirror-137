import pandas as pd
import numpy as np
import scipy.stats as stats

import warnings

import matplotlib.pyplot as plt

import bluebelt.helpers.xticks
import bluebelt.core.index
import bluebelt.core.decorators
import bluebelt.graph.helpers

import bluebelt.data.resolution

import bluebelt.styles

@bluebelt.core.decorators.class_methods


class Effort():
    """
    Calculate the planning effort
    """
    def __init__(self, series, how='group', level='week', **kwargs):
        
        self.series = series
        self.how = how
        self.level = level

        # get qds variable columns
        self.quantity = kwargs.pop('quantity', None) or kwargs.pop('q', None)
        self.distribution = kwargs.pop('distribution', None) or kwargs.pop('dist', None) or kwargs.pop('d', None)
        self.skills = kwargs.pop('quality', None) or kwargs.pop('skills', None) or kwargs.pop('s', None)

        self.calculate()

    def calculate(self):

        if self.how == 'group':
            self.quantity = bluebelt.data.resolution.GroupByDatetimeIndex(self.series, level=self.level, complete=True).diff_quantity()
            self.distribution = bluebelt.data.resolution.GroupByDatetimeIndex(self.series, level=self.level, complete=True).diff_distribution()
        

    def __repr__(self):
        return (f'{self.__class__.__name__}(n={self.series.size:1.0f}, quantity={self.quantity.mean():1.4f}, distribution={self.distribution.mean():1.4f})')
    
    def plot(self, **kwargs):
        
        return _qds_plot(self, **kwargs)

def _qds_plot(_obj, **kwargs):
        
    style = kwargs.pop('style', bluebelt.styles.paper)
    title = kwargs.pop('title', f'{_obj.series.name} QDS plot')
    
    group = kwargs.pop('group', None)
    path = kwargs.pop('path', None)
    xlim = kwargs.pop('xlim', (None, None))
    ylim = kwargs.pop('ylim', (0, 1))
    
    # prepare figure
    fig, axes = plt.subplots(nrows=1, ncols=1, **kwargs)

    _index = bluebelt.core.index.IndexToolkit(_obj.quantity.index).alt()
    axes.fill_between(_index, 0, _obj.quantity.values, **style.planning.fill_between_quantity, label='quantity')
    axes.plot(_index, _obj.quantity.values, **style.planning.plot_quantity)

    axes.fill_between(_index, 0, _obj.distribution.values, **style.planning.fill_between_distribution, label='distribution')
    axes.plot(_index, _obj.distribution.values, **style.planning.plot_distribution)

    # format things
    #axes.set_xlim(xlim)
    axes.set_ylim(ylim)

    # set xticks
    bluebelt.helpers.xticks.set_xticks(ax=axes, index=_obj.quantity.index, location=_index, group=group)

    # transform yticklabels to percentage
    axes.set_yticks(axes.get_yticks())
    axes.set_yticklabels([f'{y:1.0%}' for y in axes.get_yticks()])

    # title
    axes.set_title(title, **style.graphs.line.title)

    # legend
    axes.legend(loc='upper left')

    if path:
        plt.savefig(path)
        plt.close()
    else:
        plt.close()
        return fig