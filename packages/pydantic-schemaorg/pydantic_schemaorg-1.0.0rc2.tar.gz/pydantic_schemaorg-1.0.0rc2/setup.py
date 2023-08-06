# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_schemaorg', 'pydantic_schemaorg.ISO8601']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-schemaorg',
    'version': '1.0.0rc2',
    'description': 'Pydantic classes for Schema.org',
    'long_description': '# pydantic_schemaorg\n\nUse [Schema.org](https://schema.org) types in [pydantic](https://pydantic-docs.helpmanual.io/)! <br> <br>\n**Pydantic_schemaorg** contains all the models defined by schema.org. The pydantic classes are auto-generated from the\nschema.org model definitions that can be found\non [https://schema.org/version/latest/schemaorg-current-https.jsonld](https://schema.org/version/latest/schemaorg-current-https.jsonld)\n\n## Requirements\n\nWorks with python >= 3.7 since the library uses `__future__.annotations`\n\n## How to install\n\n```pip install pydantic_schemaorg```<br><br>\nImport any class you want to use by with the following convention<br>\n```from pydantic_schemaorg.<SCHEMAORG_MODEL_NAME> import <SCHEMAORG_MODEL_NAME>```<br><br>\n\nA full (hierarchical) list of Schema.org model names can be found [here](https://schema.org/docs/full.html)\n\n## Example usages\n\n```\nfrom pydantic_schemaorg.ScholarlyArticle import ScholarlyArticle\n\nscholarly_article = ScholarlyArticle(url=\'https://github.com/lexiq-legal/pydantic_schemaorg\',\n                                    sameAs=\'https://github.com/lexiq-legal/pydantic_schemaorg\',\n                                    copyrightNotice=\'Free to use under the MIT license\',\n                                    dateCreated=\'15-12-2012\')\nprint(scholarly_article.json())\n```\n\n```\n{"@type": "ScholarlyArticle", "url": "https://github.com/lexiq-legal/pydantic_schemaorg", "sameAs": "https://github.com/lexiq-legal/pydantic_schemaorg", "copyrightNotice": "Free to use under the MIT license", "dateCreated": "15-12-2012"}\n```',
    'author': 'Reinoud Baker',
    'author_email': 'reinoud@lexiq.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lexiq-legal/pydantic_schemaorg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
