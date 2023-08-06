# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['online_beast']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79,<2.0', 'typer[all]']

entry_points = \
{'console_scripts': ['online-beast = online_beast.main:app']}

setup_kwargs = {
    'name': 'online-beast',
    'version': '0.3.0',
    'description': '',
    'long_description': '# online-BEAST\n[![PyPi](https://img.shields.io/pypi/v/online-beast.svg)](https://pypi.org/project/online-beast/)\n[![tests](https://github.com/Wytamma/online-beast/actions/workflows/test.yml/badge.svg)](https://github.com/Wytamma/online-beast/actions/workflows/test.yml)\n[![cov](https://codecov.io/gh/Wytamma/online-beast/branch/master/graph/badge.svg)](https://codecov.io/gh/Wytamma/online-beast)\n\nThis command line tool can be used to add sequences to an ongoing analysis in BEAST2 analysis. This framework is called online Bayesian phylodynamic inference (see [Gill et al., 2020](https://academic.oup.com/mbe/article/37/6/1832/5758268?login=false)).\n\n## Install\nInstall `online-beast` with pip (requires python -V >= 3.6.2).\n\n```bash\npip install online-beast\n```\n\n## Usage \n\nGive `online-beast` beast the path to a xml file from an previous BEAST run (i.e. one that have been stopped/killed/crashed) and a fasta of sequence to add to the analysis. Sequences in the fasta file must be aligned and the same length as the other sequences in the XML file. Only new sequences (new descriptors) will be added to the analysis, so new sequences can be append to the fasta file as they are acquired. \n\n```bash\nonline-beast data/testGTR.xml data/samples.fasta\n```\n\n![](images/output.png)\n\nThe new sequences will by added to the XML file and the associated `.state` file (produced automatically by BEAST2).\n\nThe analysis can then be resumed (with the additional sequence data) using the BEAST2 resume flag. \n\n```bash\nbeast -resume testGTR.xml\n```\n\nThe online analysis can be visualised using [Beastiary](https://beastiary.wytamma.com/). The jumps in the trace show where new sequences have been added. \n\n![](images/beastiary.png)\n\nBy default the new sequences will be appended to the input XML and Sate files. Output file names can be specified using the `--output` flag. This will also create a new `.state` file.\n\n```bash\nonline-beast testGTR.xml samples.fasta --output new_testGTR.xml \n```\n\nIf you use the BEAST2 `-statefile` flag to specify the filename of the state (i.e. it is not `xml_filename + .state`). Use the flag `--state-file` to specify the state file path. \n\n```bash\nonline-beast testGTR.xml samples.fasta --state-file beast.state \n```\n\n## Explanation\n\nOnline-beast loosely follows the implementation of [Gill et al., 2020](https://academic.oup.com/mbe/article/37/6/1832/5758268?login=false) for BEAST1. However, most of the implementation of online-beast is handle by the default state system in BEAST2. Sequences are added to the latest tree in the state file. New sequences are added from the fasta file one at a time. The pairwise distance is calculated between the new sequence and all the other sequences in the XML file. The new sequence is grafted onto the tree in the `.state` file half way along the branch of the closest sequence in the XML file. The new sequence is append to the BEAST XML file. \n\n\n\n\n\n\n',
    'author': 'Wytamma Wirth',
    'author_email': 'wytamma.wirth@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
