import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import bluebelt.graph.defaults
import bluebelt.core.helpers
import bluebelt.graph.helpers

import warnings

def _get_frame(_obj, **kwargs):

    columns = kwargs.get('columns', None)

    if isinstance(_obj, pd.DataFrame) and isinstance(columns, (str, list)):
        return _obj[columns]
    elif isinstance(_obj, pd.Series):
        return pd.DataFrame(_obj)
    else:
        return _obj

def _get_name(_obj, **kwargs):

    if isinstance(_obj, pd.Series):
        return _obj.name
    elif isinstance(_obj, pd.DataFrame):
        names = []
        for col in _obj.columns:
            names.append(col)
        return bluebelt.core.helpers._get_nice_list(names)
    else:
        return None
    
def line(_obj, **kwargs):
    """
    Make a line plot for a pandas Series or a pandas Dataframe
        arguments
        _obj: pandas.Series or pandas.Dataframe
        style: bluebelt style
            default value: bluebelt.styles.paper
        title: string
            default value: pandas Series name or pandas Dataframe column names
        path: string
            the full path to save the plot (e.g. 'results/plot_001.png')
            default value: None
        xlim: tuple
            a tuple with the two limits for the x-axis (e.g. (0, 100) or (None, 50))
            default value: (None, None)
        ylim: tuple
            a tuple with the two limits for the y-axis (e.g. (0, None) or (100, 200))
            default value: (None, None)
        **kwargs: all additional kwargs will be passed to matplotlib.pyplot.subplots()
    """

    style = kwargs.pop('style', bluebelt.styles.paper)
    _func = _obj._blue_function + ' ' if hasattr(_obj, '_blue_function') else ''
    title = kwargs.pop('title', f'{_get_name(_obj)} {_func}line plot')
    group = kwargs.pop('group', None)
    
    path = kwargs.pop('path', None)
    xlim = kwargs.pop('xlim', (None, None))
    ylim = kwargs.pop('ylim', (None, None))
    
    frame = _get_frame(_obj, **kwargs)

    # prepare figure
    fig, axes = plt.subplots(nrows=1, ncols=1, **kwargs)

    # get alt indices
    _index = bluebelt.core.index.IndexToolkit(_obj.index).alt()

    for col in frame:
        # _obj.plot(kind='line', ax=fig.gca())
        # bluebelt.graph.graph.line(series=frame[col], ax=axes, style=style)
        axes.plot(_index, frame[col].values, **style.graphs.line.plot, label=col)
        
    # set xticks
    bluebelt.helpers.xticks.set_xticks(ax=axes, index=frame.index, location=_index, group=group)
    
    # format things
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)
    
    # legend
    if isinstance(_obj, pd.DataFrame):
        if _obj.shape[1] > 1:
            axes.legend(loc='best')
    # title
    axes.set_title(title, **style.graphs.line.title)

    if path:
        plt.savefig(path)
        plt.close()
    else:
        plt.close()
        return fig

def scatter(_obj, **kwargs):
    """
    Make a scatter plot for a pandas Series or a pandas Dataframe
        arguments
        _obj: pandas.Series or pandas.Dataframe
        style: bluebelt style
            default value: bluebelt.styles.paper
        title: string
            default value: pandas Series name or pandas Dataframe column names
        path: string
            the full path to save the plot (e.g. 'results/plot_001.png')
            default value: None
        xlim: tuple
            a tuple with the two limits for the x-axis (e.g. (0, 100) or (None, 50))
            default value: (None, None)
        ylim: tuple
            a tuple with the two limits for the y-axis (e.g. (0, None) or (100, 200))
            default value: (None, None)
        **kwargs: all additional kwargs will be passed to matplotlib.pyplot.subplots()
    """
    style = kwargs.pop('style', bluebelt.styles.paper)
    _func = _obj._blue_function + ' ' if hasattr(_obj, '_blue_function') else ''
    
    path = kwargs.pop('path', None)
    xlim = kwargs.pop('xlim', (None, None))
    ylim = kwargs.pop('ylim', (None, None))
    
    frame = _get_frame(_obj, **kwargs)

    if frame.shape[1] >= 2:
        title = kwargs.pop('title', f'{_get_name(frame.iloc[:,:2])}  {_func}scatter plot')
        index_name = frame.columns[0]
        frame = pd.DataFrame(data={frame.columns[1]: frame.iloc[:,1].values}, index=frame.iloc[:,0].values)
        frame.index.name = index_name
    else:
        title = kwargs.pop('title', f'{_get_name(_obj)}  {_func}scatter plot')
    
    
    # prepare figure
    fig, axes = plt.subplots(nrows=1, ncols=1, **kwargs)

    bluebelt.graph.defaults.scatter(series=frame, ax=axes, style=style)
        
    # format things
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)
    
    # title
    axes.set_title(title, **style.graphs.scatter.title)

    if path:
        plt.savefig(path)
        plt.close()
    else:
        plt.close()
        return fig

def area(_obj, **kwargs):
    """
    Make an area plot for a pandas Series or a pandas Dataframe
        arguments
        _obj: pandas.Series or pandas.Dataframe
        style: bluebelt style
            default value: bluebelt.styles.paper
        title: string
            default value: pandas Series name or pandas Dataframe column names
        path: string
            the full path to save the plot (e.g. 'results/plot_001.png')
            default value: None
        xlim: tuple
            a tuple with the two limits for the x-axis (e.g. (0, 100) or (None, 50))
            default value: (None, None)
        ylim: tuple
            a tuple with the two limits for the y-axis (e.g. (0, None) or (100, 200))
            default value: (None, None)
        **kwargs: all additional kwargs will be passed to matplotlib.pyplot.subplots()
    """
    
    frame = _get_frame(_obj, **kwargs)

    style = kwargs.pop('style', bluebelt.styles.paper)
    _func = _obj._blue_function + ' ' if hasattr(_obj, '_blue_function') else ''
    title = kwargs.pop('title', f'{_get_name(_obj)} {_func}area plot')
    group = kwargs.pop('group', None)
    
    path = kwargs.pop('path', None)
    xlim = kwargs.pop('xlim', (None, None))
    ylim = kwargs.pop('ylim', (None, None))
    
    # get alt indices
    _index = bluebelt.core.index.IndexToolkit(_obj.index).alt()
    
    # prepare figure
    fig, axes = plt.subplots(nrows=1, ncols=1, **kwargs)

    for col in frame:
        axes.stackplot(_index, frame[col].values, **style.graphs.area.stackplot)
        axes.plot(_index, frame[col].values, label=col, **style.graphs.area.plot, **kwargs)
        
    # set xticks
    bluebelt.helpers.xticks.set_xticks(ax=axes, index=frame.index, location=_index, group=group)
    
    # format things
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)
    
    # legend
    if isinstance(_obj, pd.DataFrame):
        if _obj.shape[1] > 1:
            axes.legend(loc='best')
    
    # title
    axes.set_title(title, **style.graphs.area.title)

    if path:
        plt.savefig(path)
        plt.close()
    else:
        plt.close()
        return fig

def hist(_obj, **kwargs):
    """
    Make a histogram plot for a pandas Series or a pandas Dataframe
        arguments
        _obj: pandas.Series or pandas.Dataframe
        style: bluebelt style
            default value: bluebelt.styles.paper
        title: string
            default value: pandas Series name or pandas Dataframe column names
        path: string
            the full path to save the plot (e.g. 'results/plot_001.png')
            default value: None
        fit: boolean
            fit a normal distribution
            default value: False
        xlim: tuple
            a tuple with the two limits for the x-axis (e.g. (0, 100) or (None, 50))
            default value: (None, None)
        ylim: tuple
            a tuple with the two limits for the y-axis (e.g. (0, None) or (100, 200))
            default value: (None, None)
        **kwargs: all additional kwargs will be passed to matplotlib.pyplot.subplots()
    """
    
    frame = _get_frame(_obj, **kwargs)

    style = kwargs.pop('style', bluebelt.styles.paper)
    _func = _obj._blue_function + ' ' if hasattr(_obj, '_blue_function') else ''
    title = kwargs.pop('title', f'{_get_name(_obj)} {_func}histogram')
    
    path = kwargs.pop('path', None)
    xlim = kwargs.pop('xlim', (None, None))
    ylim = kwargs.pop('ylim', (None, None))
    
    # prepare figure
    fig, axes = plt.subplots(nrows=1, ncols=1, **kwargs)

    for col in frame:
        # .get_level_values(-1) hack to get last level
        axes.hist(frame[col], label=col, **style.default.hist) 
                
    # format things
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)
    
    # title
    axes.set_title(title, **style.graphs.area.title)

    if path:
        plt.savefig(path)
        plt.close()
    else:
        plt.close()
        return fig

histogram = hist

def boxplot(_obj, **kwargs):
    """
    Make a boxplot for a pandas Series or a pandas Dataframe
        arguments
        _obj: pandas.Series or pandas.Dataframe
        style: bluebelt style
            default value: bluebelt.styles.paper
        title: string
            default value: pandas Series name or pandas Dataframe column names
        path: string
            the full path to save the plot (e.g. 'results/plot_001.png')
            default value: None
        xlim: tuple
            a tuple with the two limits for the x-axis (e.g. (0, 100) or (None, 50))
            default value: (None, None)
        ylim: tuple
            a tuple with the two limits for the y-axis (e.g. (0, None) or (100, 200))
            default value: (None, None)
        **kwargs: all additional kwargs will be passed to matplotlib.pyplot.subplots()
    """
    
    style = kwargs.pop('style', bluebelt.styles.paper)
    _func = _obj._blue_function + ' ' if hasattr(_obj, '_blue_function') else ''
    title = kwargs.pop('title', f'{_get_name(_obj)} {_func}boxplot')
    
    path = kwargs.pop('path', None)
    xlim = kwargs.pop('xlim', (None, None))
    ylim = kwargs.pop('ylim', (None, None))
    
    frame = _get_frame(_obj, **kwargs)

    # prepare figure
    fig, axes = plt.subplots(nrows=1, ncols=1, **kwargs)

    bluebelt.graph.defaults.boxplot(series=frame.values, ax=axes, style=style)
        
    # format things
    axes.set_xticklabels(frame.columns)
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)
            
    # title
    axes.set_title(title, **style.graphs.boxplot.title)

    if path:
        plt.savefig(path)
        plt.close()
    else:
        plt.close()
        return fig
    

def waterfall(series, **kwargs):

    if not isinstance(series, pd.Series):
        raise ValueError('Waterfall charts need a pandas.Series')
    
    style = kwargs.pop('style', bluebelt.styles.paper)
    title = kwargs.pop('title', f'{_get_name(series)} waterfall')
    
    path = kwargs.pop('path', None)
    width = kwargs.pop('width', 0.6)
    
    format_yticks = kwargs.pop('format_yticks', None)
    
    measure = pd.Series(kwargs.pop('measure', ['relative'] * series.shape[0]))

    # are the totals ok?
    if ('total' in measure.unique()) and not (series.where((measure=='relative').values).cumsum().shift().where((measure=='total').values).fillna(0) == series.where((measure=='total').values).fillna(0)).all():
        warnings.warn('The totals values are not the totals of the preceeding values. This will be adjusted.', Warning)
        series = series.where((measure=='relative').values).cumsum().shift().where((measure=='total').values, series).fillna(0)

    # calculations
    bottom = series.where((measure=='relative').values).fillna(0).cumsum() - series
    index = np.arange(series.index.shape[0])

    ylim = kwargs.pop('ylim', ((bottom).min() * 1.05, (series+bottom).max() * 1.05))
    
    fig, ax = plt.subplots(nrows=1, ncols=1)
   
    # totals
    ax.bar(index, series.where((measure=='total').values).values, bottom=bottom, width=width, **style.graphs.waterfall.total)
    ax.bar(index, series.where((measure=='total').values).values, bottom=bottom, width=width, **style.graphs.waterfall.border)

    # increasing
    ax.bar(index, series.where((series>=0) & ((measure=='relative').values)).values, bottom=bottom, width=width, **style.graphs.waterfall.increasing)
    ax.bar(index, series.where((series>=0) & ((measure=='relative').values)).values, bottom=bottom, width=width, **style.graphs.waterfall.border)

    # decreasing
    ax.bar(index, series.where((series<0) & ((measure=='relative').values)).values, bottom=bottom, width=width, **style.graphs.waterfall.decreasing)
    ax.bar(index, series.where((series<0) & ((measure=='relative').values)).values, bottom=bottom, width=width, **style.graphs.waterfall.border)

    # connectors
    ax.bar((index+0.5)[:-1], 0, bottom=(bottom + series)[:-1], width=1-width, **style.graphs.waterfall.connectors)
    ax.set_ylim(0,600)

    # xticks
    ax.set_xticks(index)
    ax.set_xticklabels(series.index.values)

    # yticks
    if format_yticks == '%':
        # transform yticklabels to percentage
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels([f'{y:1.0%}' for y in ax.get_yticks()])

    # ylim
    ax.set_ylim(ylim)

    # title
    ax.set_title(title, **style.graphs.waterfall.title)

    if path:
        plt.savefig(path)
        plt.close()
    else:
        plt.close()
        return fig