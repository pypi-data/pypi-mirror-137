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
        return _qds_effort_plot(self, **kwargs)

class Ease():
    """
    Calculate the planning ease
    """
    def __init__(self, series, level=['year', 'week'], **kwargs):
        
        self.series = series
        self.level = level

        self.calculate()

    def calculate(self):

        self.quantity = 1 - bluebelt.data.resolution.GroupByDatetimeIndex(self.series, level=self.level, complete=True).diff_quantity()
        self.distribution = 1 - bluebelt.data.resolution.GroupByDatetimeIndex(self.series, level=self.level, complete=True).diff_distribution()
        if isinstance(self.series, pd.DataFrame):
            self.skills = 1 - bluebelt.data.resolution.GroupByDatetimeIndex(self.series, level=self.level, complete=True).diff_skills()
        else:
            self.skills = pd.Series(index=self.quantity.index, data=np.ones(self.quantity.index.shape[0]), name='skills')

        self.qds = self.quantity * self.distribution * self.skills

    def __repr__(self):
        return (f'{self.__class__.__name__}(n={self.series.shape[0]:1.0f}, qds={self.qds.mean():1.4f}, quantity={self.quantity.mean():1.4f}, distribution={self.distribution.mean():1.4f}, skills={self.skills.mean():1.4f})')
    
    def plot(self, **kwargs):
        return _qds_ease_plot(self, **kwargs)
    
def _qds_effort_plot(_obj, **kwargs):
        
    style = kwargs.pop('style', bluebelt.styles.paper)
    title = kwargs.pop('title', f'planning QDS effort plot')
    group = kwargs.pop('group', None)
    path = kwargs.pop('path', None)
    ylim = kwargs.pop('ylim', (0, 1))
    
    # prepare figure
    fig, axes = plt.subplots(nrows=1, ncols=1, **kwargs)

    _index = bluebelt.core.index.IndexToolkit(_obj.quantity.index[1:]).alt()

    # q
    axes.fill_between(_index, 0, _obj.quantity.values[1:], **style.planning.fill_between_quantity, label=f'quantity ({_obj.quantity.mean()*100:1.1f}%)')
    axes.plot(_index, _obj.quantity.values[1:], **style.planning.plot_quantity)
    
    # d
    axes.fill_between(_index, 0, _obj.distribution.values[1:], **style.planning.fill_between_distribution, label=f'distribution ({_obj.distribution.mean()*100:1.1f}%)')
    axes.plot(_index, _obj.distribution.values[1:], **style.planning.plot_distribution)

    # s
    axes.fill_between(_index, 0, _obj.skills.values[1:], **style.planning.fill_between_skills, label=f'skills ({_obj.skills.mean()*100:1.1f}%)')
    axes.plot(_index, _obj.skills.values[1:], **style.planning.plot_skills)
    
    # qds
    axes.plot(_index, _obj.qds.values[1:], **style.planning.plot_qds, label=f'qds effort ({_obj.qds.mean()*100:1.1f}%)')
    
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

def _qds_ease_plot(_obj, **kwargs):
        
    style = kwargs.pop('style', bluebelt.styles.paper)
    width = kwargs.pop('width', 0.8)
    title = kwargs.pop('title', f'planning QDS ease plot')
    path = kwargs.pop('path', None)
    
    # calculations
    qds = pd.Series({
        'q': _obj.quantity.mean(),
        'd': _obj.distribution.mean(),
        's': _obj.skills.mean(),
    }).reset_index(drop=True)

    vals = qds.cumprod()
    rest = (qds.cumprod().shift(1).fillna(1) - qds.cumprod())

    # prepare figure
    fig, axes = plt.subplots(nrows=1, ncols=1, **kwargs)

    # top
    axes.bar(rest.index, rest.values, bottom=vals.values, width=width, **style.planning.bar_top)
    axes.bar(rest.index, rest.values, bottom=vals.values, width=width, **style.planning.bar_border)
    
    # bottom
    axes.bar(vals.index, vals.values, width=width, **style.planning.bar_bottom)
    axes.bar(vals.index, vals.values, width=width, **style.planning.bar_border)
    
    
    # connectors
    xlim = axes.get_xlim()
    axes.bar((rest.index+0.5), 0, bottom=vals.values, width=1-width, **style.planning.bar_connectors)
    
    axes.set_ylim(0,1.1)
    axes.set_xlim(xlim)
    axes.set_xticks([0,1,2])
    axes.set_xticklabels(['Q','D','S'])
    axes.tick_params(axis="x", bottom=True, top=False, labelbottom=True, labeltop=False)

    for tick in axes.get_xticks():
        axes.text(tick, vals.iloc[tick]+(rest.iloc[tick] / 2), f'{(1-qds.iloc[tick])*100:1.1f}%', **style.planning.value_text)
        axes.text(tick, (vals.iloc[tick] / 2), f'{qds.iloc[tick]*100:1.1f}%', **style.planning.value_text)
        

    # transform yticklabels to percentage, add qds and remove closest to qds
    # yticks = axes.get_yticks().tolist()
    # yticks.remove(min(yticks, key=lambda x:abs(x-qds.cumprod().iloc[-1])))
    # yticks.append(qds.cumprod().iloc[-1])
    yticks = [0, qds.cumprod().iloc[-1], 1]
    axes.set_yticks(yticks)
    axes.set_yticklabels([f'{y:1.0%}' for y in axes.get_yticks()])
    axes.yaxis.tick_right()

    # title
    axes.set_title(title, **style.graphs.line.title)

    if path:
        plt.savefig(path)
        plt.close()
    else:
        plt.close()
        return fig