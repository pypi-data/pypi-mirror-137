import bluebelt.styles.defaults as defaults

# main plot | pyplot.plot
plot_quantity = {
    'color': defaults.black,
    'linestyle': 'solid',
    'linewidth': 1,
    'zorder': 90,
}
# main plot | pyplot.fill_between
fill_between_quantity = {
    'color': None,
    'hatch': '////',
    'linestyle': 'dashed',
    'linewidth': 0.5,
    'zorder': 50,
}

# main plot | pyplot.plot
plot_distribution = {
    'color': defaults.blue,
    'linestyle': 'solid',
    'linewidth': 1,
    'zorder': 89,
}

# main plot | pyplot.fill_between
fill_between_distribution = {
    'color': None,
    'edgecolor': defaults.blue,
    'hatch': '\\\\\\\\',
    'linestyle': 'dashed',
    'linewidth': 0.5,
    'zorder': 49,
}

plot_skills = {
    'color': defaults.green,
    'linestyle': 'solid',
    'linewidth': 1,
    'zorder': 88,
}
# main plot | pyplot.fill_between
fill_between_skills = {
    'color': None,
    'edgecolor': defaults.green,
    'hatch': '||||',
    'linestyle': 'dashed',
    'linewidth': 0.5,
    'zorder': 48,
}

# main plot | pyplot.plot
plot_qds = {
    'color': defaults.red,
    'linestyle': 'solid',
    'linewidth': 1,
    'zorder': 100,
}

# plot title | pyplot.set_title
title = {
    'loc': 'left',
}