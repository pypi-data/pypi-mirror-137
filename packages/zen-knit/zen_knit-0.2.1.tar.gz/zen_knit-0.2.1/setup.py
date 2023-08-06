# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zen_knit',
 'zen_knit.data_types',
 'zen_knit.executor',
 'zen_knit.formattor',
 'zen_knit.formattor.html_support',
 'zen_knit.organizer',
 'zen_knit.parser',
 'zen_knit.reader']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.6,<4.0.0',
 'SQLAlchemy>=1.4.29,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'ipykernel>=6.0.0',
 'ipython>=7.0',
 'joblib>=1.1.0,<2.0.0',
 'jupyter-client>=7.1.0,<8.0.0',
 'nbconvert>=6.0.0',
 'nbformat>=5.1.3,<6.0.0',
 'oyaml>=1.0,<2.0',
 'pydantic>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['knit = zen_knit.cli:knit']}

setup_kwargs = {
    'name': 'zen-knit',
    'version': '0.2.1',
    'description': 'Zen-Knit is a formal (PDF), informal (HTML) report generator for data analyst and data scientist who wants to use python. Rmarkdown Alternative for Python',
    'long_description': '# About Zen-Knit:\nZen-Knit is a formal (PDF), informal (HTML) report generator for data analyst and data scientist who wants to use python. RMarkdown alternative.\nZen-Knit is good for creating reports, tutorials with embedded python. RMarkdown alternative. Python Markdown Support.\n\n\n[![Download Count](https://static.pepy.tech/personalized-badge/zen-knit?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads)](https://pepy.tech/project/zen-knit)\n[![python](https://img.shields.io/pypi/pyversions/zen-knit.svg?color=green)](https://img.shields.io/pypi/pyversions/zen-knit.svg?color=green)\n[![license](https://img.shields.io/github/license/Zen-Reportz/zen_knit?color=green)](https://img.shields.io/github/license/Zen-Reportz/zen_knit?color=green)\n[![version](https://img.shields.io/pypi/v/zen-knit?color=green&label=pypi%20package)](https://img.shields.io/pypi/v/zen-knit?color=green&label=pypi%20package)\n\n\n# VS Code Plugin:\nDownload VS Plugin from [MarketPlace](https://marketplace.visualstudio.com/items?itemName=ZenReportz.vscode-zen-knit)\n\n\n# Features:\n* Python 3.7+ compatibility\n* Support for IPython magics and rich output.\n* **Execute python code** in the chunks and **capture** input and output to a report.\n* **Use hidden code chunks,** i.e. code is executed, but not printed in the output file.\n* Capture matplotlib graphics.\n* Evaluate inline code in documentation chunks marked using ```{ }``` \n* Publish reports from Python scripts. Similar to R markdown.\n* Interactive Plots using plotly\n* integrate it in your process. It will fit your need rather than you need to adjust for tool.\n* custom CSS support (HTTP(s) and local file)\n* direct sql support \n* chaching executed code for faster report devlopement \n* printing index of chunk or chunk name in console\n  \n# Examples:\nAll example are available [HERE](https://github.com/Zen-Reportz/zen_knit/tree/main/doc/example)\n\n\n## PDF example\n![PDF Code](./doc/example/screenshots/pdf_code.png)\n![PDF Output](./doc/example/screenshots/pdf_output.png)\n\n## PDF example with SQL\n![PDF SQL Code](./doc/example/screenshots/pdf_sql_code.png) \n![PDF SQL Output](./doc/example/screenshots/pdf_sql_output.png) \n\n## HTML example\n![HTML Code](./doc/example/screenshots/html_code.png) \n![HTML Ouput ](./doc/example/screenshots/html_output.png)\n![HTML output 2](./doc/example/screenshots/html_output_2.png)\n\n## HTML example with custom CSS\n![HTML CDN CSS](./doc/example/screenshots/html_cdn_css_code.png) \n![HTML Custom CSS](./doc/example/screenshots/html_custom_css_code.png)\n\n## HTML example with SQL\n![HTML SQL](./doc/example/screenshots/html_sql_code.png) \n![HTML SQL output](./doc/example/screenshots/html_sql_output.png) \n\n\n# Install\n\nFrom PyPi:\n\n  <code> pip install --upgrade zen-knit </code>\n\nor download the source and run::\n\n  <code> python setup.py install </code>\n\n\n## Other Dependency\n\n<code> install pandoc from : https://github.com/jgm/pandoc/releases </code>\n\n<code> install texlive for debian: sudo apt install texlive-full </code>\n\n<code> install texlive for window: https://www.tug.org/texlive/acquire-netinstall.html </code>\n\n<code> install texlive for mac: https://tug.org/texlive/quickinstall.html </code>\n\n\n## License information\n\n\nPermission is hereby granted, free of charge, to any person obtaining\na copy of this software and associated documentation files (the\n"Software"), to deal in the Software without restriction, including\nwithout limitation the rights to use, copy, modify, merge, publish,\ndistribute, sublicense, and/or sell copies of the Software, and to\npermit persons to whom the Software is furnished to do so, subject to\nthe following conditions:\n\nThe above copyright notice and this permission notice shall be\nincluded in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND\nNONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE\nLIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION\nOF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION\nWITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n\n\n## How to Use it\n\n  <code> pip install zen-knit  </code>\n\n  <code> knit -f doc/example/html_example.pyz  -ofd doc/example/output/  </code>\n  \n  <code> knit -f doc/example/pdf_example.pyz  -ofd doc/example/output/  </code>\n\n  <code>  python doc/example/demo.py  </code>\n  \n\n## Arguments \n    ---\n    title: Zen Markdown Demo\n    author: Dr. P. B. Patel\n    date: CURRENT_DATE\n    cache: true\n    output: \n        format: html\n        html: \n            css: skleton\n    ---\n\nAbove code will map on GlobalOption class in in following\n\n    class Input(BaseModel):\n        dir: Optional[str]\n        file_name: Optional[str]\n        matplot: bool = True\n    \n    class latexOuput(BaseModel):\n        header: Optional[str] \n        page_size: Optional[str] = \'a4paper\' #Newely added parameters\n    \n    class htmlOutput(BaseModel):\n        css: str = "bootstrap"\n\n    class Output(BaseModel):\n        fig_dir: str = "figures"\n        format: Optional[str]\n        file_name: Optional[str]\n        dir: Optional[str]\n        latex: Optional[latexOuput]\n        html: Optional[htmlOutput]\n\n    class GlobalOption(BaseModel):\n        title: str\n        author: Optional[str]\n        date: Optional[str]\n        kernal: str = "python3"\n        log_level: str = "debug"\n        cache: Optional[bool] = False\n        output: Output\n        input: Input\n\n        @validator(\'log_level\')\n        def fix_option_for_log(cls, v:str):\n            if v.lower() not in (\'notset\', "debug", \'info\', \'warning\', \'error\', \'critical\'):\n                raise ValueError(\'must contain a space\')\n            return v.title()\n\n',
    'author': 'Zen',
    'author_email': 'zenreportz@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Zen-Reportz/zen_knit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
