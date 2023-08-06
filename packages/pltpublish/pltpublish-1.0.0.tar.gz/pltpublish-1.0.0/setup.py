# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pltpublish']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0']

setup_kwargs = {
    'name': 'pltpublish',
    'version': '1.0.0',
    'description': 'Utility package that takes care of configuring Matplotlib for publication-ready figures!',
    'long_description': '# pltpublish\n\nUtility package that takes care of configuring Matplotlib for publication-ready figures!\n\n## Easy to use\n\n**Before**\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003**After**\n\n```python\n                                                  > import pltpublish as pub\n                                                  > pub.setup()\n# your plot code                                  > # your plot code \nplt.savefig("my_fig.eps")                         > pub.save_fig("my_fig.eps")\n```\n\n|**Without `pltpublish`**|**With `pltpublish`**|\n|-|-|\n| <img src="https://github.com/Theomat/pltpublish/raw/main/examples/images/classic.png" width="400" height="300">|<img src="https://github.com/Theomat/pltpublish/raw/main/examples/images/pltpublish.png" width="400" height="300"> |\n\n## All Features\n\n- `setup` calls all `setup_*` methods\n- `setup_colorblind` configures matplotlib to use a colorblind palette\n- `setup_latex_fonts` configures matplotlib to use LaTeX fonts\n- `save_fig` acts like `pyplot.save_fig` but guarantees a minimum dpi, that the grid is on and removes outer white space\n- `extract_legend_as_figure` extracts the legend of your figure and plots it on another new figure\n- `layout_for_subplots` finds automatically a good layout given the number of plots you have to plot on the same figure\n',
    'author': 'Théo Matricon',
    'author_email': 'theomatricon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Theomat/pltpublish',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
