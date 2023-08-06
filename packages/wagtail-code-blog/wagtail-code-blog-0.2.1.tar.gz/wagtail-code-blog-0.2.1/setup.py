# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_code_blog', 'wagtail_code_blog.migrations']

package_data = \
{'': ['*'],
 'wagtail_code_blog': ['static/wagtail_code_blog/*',
                       'static/wagtail_code_blog/css/*',
                       'static/wagtail_code_blog/images/*',
                       'templates/wagtail_code_blog/*']}

install_requires = \
['beautifulsoup4==4.8',
 'django-json-ld>=0.0.4,<0.0.5',
 'django-model-utils>=4.2.0,<5.0.0',
 'readtime>=1.1.1,<2.0.0',
 'wagtail-metadata>=3.0.0,<4.0.0',
 'wagtail>=2.10,<3.0']

setup_kwargs = {
    'name': 'wagtail-code-blog',
    'version': '0.2.1',
    'description': 'A wagtail code blog',
    'long_description': '# A code blog for wagtail\n\nBuilt with wagtail-code-blog:\n\n- [Findwork.dev/blog](https://findwork.dev/blog)\n',
    'author': 'Dani Hodovic',
    'author_email': 'dani.hodovic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/honeylogic-io/wagtail-code-blog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
