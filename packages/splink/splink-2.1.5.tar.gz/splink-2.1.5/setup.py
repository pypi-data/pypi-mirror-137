# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splink']

package_data = \
{'': ['*'],
 'splink': ['files/*',
            'files/chart_defs/*',
            'files/external_js/*',
            'files/templates/*',
            'jars/*']}

install_requires = \
['jsonschema>=3.2,<4.0', 'sqlglot>=1.18.0,<2.0.0', 'typeguard>=2.10.0,<3.0.0']

setup_kwargs = {
    'name': 'splink',
    'version': '2.1.5',
    'description': "Implementation of Fellegi-Sunter's canonical model of record linkage in Apache Spark, including EM algorithm to estimate parameters",
    'long_description': "![image](https://user-images.githubusercontent.com/7570107/85285114-3969ac00-b488-11ea-88ff-5fca1b34af1f.png)\n\n[![Coverage Status](https://coveralls.io/repos/github/moj-analytical-services/splink/badge.svg?branch=master)](https://coveralls.io/github/moj-analytical-services/splink?branch=master)\n![issues-status](https://img.shields.io/github/issues-raw/moj-analytical-services/splink)\n![python-version-dependency](https://img.shields.io/badge/python-%3E%3D3.6-blue)\n\n# splink: Probabilistic record linkage and deduplication at scale\n\n`splink` implements Fellegi-Sunter's canonical model of record linkage in Apache Spark, including the EM algorithm to estimate parameters of the model.\n\nIt:\n\n- Works at much greater scale than current open source implementations (100 million records+).\n\n- Runs quickly - with runtimes of less than an hour.\n\n- Has a highly transparent methodology; match scores can be easily explained both graphically and in words\n\n- Is highly accurate\n\nIt is assumed that users of Splink are familiar with the probabilistic record linkage theory, and the Fellegi-Sunter model in particular. A [series of interactive articles](https://www.robinlinacre.com/probabilistic_linkage/) explores the theory behind Splink.\n\nThe statistical model behind `splink` is the same as that used in the R [fastLink package](https://github.com/kosukeimai/fastLink). Accompanying the fastLink package is an [academic paper](http://imai.fas.harvard.edu/research/files/linkage.pdf) that describes this model. This is the best place to start for users wanting to understand the theory about how `splink` works.\n\n[Data Matching](https://link.springer.com/book/10.1007/978-3-642-31164-2), a book by Peter Christen, is another excellent resource.\n\n## Installation\n\n`splink` is a Python package. It uses the Spark Python API to execute data linking jobs in a Spark cluster. It has been tested in Apache Spark 2.3, 2.4 and 3.1.\n\nInstall splink using:\n\n`pip install splink`\n\nNote that Splink requires `pyspark` and a working Spark installation. These are not specified as explicit dependencies becuase it is assumed users have an existing pyspark setup they wish to use.\n\n## Interactive demo\n\nYou can run demos of `splink` in an interactive Jupyter notebook by clicking the button below:\n\n[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/moj-analytical-services/splink_demos/master?urlpath=lab/tree/index.ipynb)\n\n## Documentation\n\nThe best documentation is currently a series of demonstrations notebooks in the [splink_demos](https://github.com/moj-analytical-services/splink_demos) repo.\n\n## Other tools in the Splink family\n\n### Splink Graph\n\n[`splink_graph`](https://github.com/moj-analytical-services/splink_graph) is a graph utility library for use in Apache Spark. It computes graph metrics on the outputs of data linking. The repo is [here](<(https://github.com/moj-analytical-services/splink_graph)>)\n\n- Quality assurance of linkage results and identifying false positive links\n- Computing quality metrics associated with groups (clusters) of linked records\n- Automatically identifying possible false positive links in clusters\n\n\n### Splink Comparison Viewer\n\n[`splink_comparison_viewer`](https://github.com/moj-analytical-services/splink_comparison_viewer) produces interactive dashboards that help you rapidly understand and quality assure the outputs of record linkage.    A tutorial video is available [here](https://www.youtube.com/watch?v=DNvCMqjipis).\n\n### Splink Cluster Studio\n\n[`splink_cluster_studio`](http://github.com/moj-analytical-services/splink_cluster_studio) creates an interactive html dashboard from Splink output that allows you to visualise and analyse a sample of clusters from your record linkage. The repo is [here](http://github.com/moj-analytical-services/splink_cluster_studio).\n\n### Splink Synthetic Data\n\nThis [code](https://github.com/moj-analytical-services/splink_synthetic_data) is able to generate realistic test datasets for linkage using the WikiData Query Service.\n\nIt has been used to [performance test the accuracy of various Splink models](https://www.robinlinacre.com/comparing_splink_models/).\n\n### Interactive settings editor with autocomplete\n\nWe also provide an interactive `splink` settings editor and example settings [here](https://moj-analytical-services.github.io/splink_settings_editor/).\n\n### Starting parameter generation tools\n\nA tool to generate custom `m` and `u` probabilities can be found [here](https://www.robinlinacre.com/m_u_generator/).\n\n## Blog\n\nYou can read a short blog post about `splink` [here](https://robinlinacre.com/introducing_splink/).\n\n## Videos\n\nYou can find a short video introducing `splink` and running though an introductory demo [here](https://www.youtube.com/watch?v=_8lV2Lbd6Xs&feature=youtu.be&t=1295).\n\nA 'best practices and performance tuning' tutorial can be found [here](https://www.youtube.com/watch?v=HzcqrRvXhCE).\n\n## Acknowledgements\n\nWe are very grateful to [ADR UK](https://www.adruk.org/) (Administrative Data Research UK) for providing funding for this work as part of the [Data First](https://www.adruk.org/our-work/browse-all-projects/data-first-harnessing-the-potential-of-linked-administrative-data-for-the-justice-system-169/) project.\n\nWe are also very grateful to colleagues at the UK's Office for National Statistics for their expert advice and peer review of this work.\n",
    'author': 'Robin Linacre',
    'author_email': 'robinlinacre@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moj-analytical-services/splink',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
