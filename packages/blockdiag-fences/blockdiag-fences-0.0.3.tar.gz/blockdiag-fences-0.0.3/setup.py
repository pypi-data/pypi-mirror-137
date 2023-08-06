# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blockdiag_fences']

package_data = \
{'': ['*']}

install_requires = \
['actdiag>=3.0.0,<4.0.0',
 'blockdiag>=3.0.0,<4.0.0',
 'nwdiag>=3.0.0,<4.0.0',
 'seqdiag>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'blockdiag-fences',
    'version': '0.0.3',
    'description': 'Inline blockdiag images for Markdown with SuperFences',
    'long_description': '# blockdiag for SuperFences\n\nThis provides [blockdiag](http://blockdiag.com/en/blockdiag/index.html) rendering for [Python Markdown](http://pythonhosted.org/Markdown/) through the [SuperFences extension](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/).\n\nIt is based on <https://github.com/gisce/markdown-blockdiag>.\n\n## Install\n\n```shell\npip install blockdiag-fences\n```\n\n## Use\n\nWrap your diagram in a code block, tagged with the name of the tool to convert it:\n\n\n\t```blockdiag\n\tblockdiag {\n\t\tA -> B -> C -> D;\n\t\tA -> E -> F -> G;\n\t}\n\t```\n\n## MkDocs Integration\n\nIn your `mkdocs.yml` add this to `markdown_extensions`.\n\n```yaml\nmarkdown_extensions:\n  - pymdownx.superfences:\n    custom_fences:\n      - name: actdiag\n        class: actdiag\n        format: !!python/name:blockdiag_fences.blockdiag.fence_img_format\n      - name: blockdiag\n        class: blockdiag\n        format: !!python/name:blockdiag_fences.blockdiag.fence_img_format\n      - name: nwdiag\n        class: nwdiag\n        format: !!python/name:blockdiag_fences.blockdiag.fence_img_format\n      - name: packetdiag\n        class: packetdiag\n        format: !!python/name:blockdiag_fences.blockdiag.fence_img_format\n      - name: rackdiag\n        class: rackdiag\n        format: !!python/name:blockdiag_fences.blockdiag.fence_img_format\n      - name: seqdiag\n        class: seqdiag\n        format: !!python/name:blockdiag_fences.blockdiag.fence_img_format\n```\n',
    'author': 'Oliver Salzburg',
    'author_email': 'oliver.salzburg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oliversalzburg/markdown-blockdiag.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
