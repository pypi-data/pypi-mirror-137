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
    def __init__(self, series, level=['year', 'week'], **kwargs):
        
        self.series = series
        self.level = level

        self.calculate()

    def calculate(self):

        self.quantity = bluebelt.data.resolution.GroupByDatetimeIndex(self.series, level=self.level, complete=True).diff_quantity()
        self.distribution = bluebelt.data.resolution.GroupByDatetimeIndex(self.series, level=self.level, complete=True).diff_distribution()
        if isinstance(self.series, pd.DataFrame):
            self.skills = bluebelt.data.resolution.GroupByDatetimeIndex(self.series, level=self.level, complete=True).diff_skills()
        else:
            self.skills = pd.Series(index=self.quantity.index, data=np.zeros(self.quantity.index.shape[0]), name='skills')

        self.qds = 1 - ((1 - self.quantity) * (1 - self.distribution) * (1 - self.skills))
    def __repr__(self):
        return (f'{self.__class__.__name__}(n={self.series.shape[0]:1.0f}, qds={self.qds.mean():1.4f}, quantity={self.quantity.mean():1.4f}, distribution={self.distribution.mean():1.4f}, skills={self.skills.mean():1.4f})')
    
    def plot(self, **kwargs):
        
        return _qds_plot(self, **kwargs)

def _qds_plot(_obj, **kwargs):
        
    style = kwargs.pop('style', bluebelt.styles.paper)
    title = kwargs.pop('title', f'planning effort QDS plot')
    
    group = kwargs.pop('group', None)
    path = kwargs.pop('path', None)
    xlim = kwargs.pop('xlim', (None, None))
    ylim = kwargs.pop('ylim', (0, 1))
    
    # prepare figure
    fig, axes = plt.subplots(nrows=1, ncols=1, **kwargs)

    _index = bluebelt.core.index.IndexToolkit(_obj.quantity.index[1:]).alt()

    # q
    axes.fill_between(_index, 0, _obj.quantity.values[1:], **style.planning.fill_between_quantity, label='quantity')
    axes.plot(_index, _obj.quantity.values[1:], **style.planning.plot_quantity)
    
    # d
    axes.fill_between(_index, 0, _obj.distribution.values[1:], **style.planning.fill_between_distribution, label='distribution')
    axes.plot(_index, _obj.distribution.values[1:], **style.planning.plot_distribution)

    # s
    axes.fill_between(_index, 0, _obj.skills.values[1:], **style.planning.fill_between_skills, label='skills')
    axes.plot(_index, _obj.skills.values[1:], **style.planning.plot_skills)
    
    # qds
    axes.plot(_index, _obj.qds.values[1:], **style.planning.plot_qds, label='qds')
    
    # format things
    axes.set_ylim(ylim)

    # set xticks
    bluebelt.helpers.xticks.set_xticks(ax=axes, index=_obj.quantity.index[1:], location=_index[1:], group=group)

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