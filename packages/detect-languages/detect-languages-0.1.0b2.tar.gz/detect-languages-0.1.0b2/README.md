# detect-languages

[![Latest PyPI version](https://img.shields.io/pypi/v/detect-languages.svg)](https://pypi.python.org/pypi/detect-languages) [![GitHub Actions status](https://github.com/alexgracianoarj/detect-languages/workflows/Tests/badge.svg)](https://github.com/alexgracianoarj/detect-languages/actions?query=workflow%3ATests) [![Python versions](https://img.shields.io/pypi/pyversions/detect-languages.svg)](https://pypi.python.org/pypi/detect-languages) [![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black) [![License](https://img.shields.io/github/license/alexgracianoarj/detect-languages)](https://github.com/alexgracianoarj/detect-languages/blob/main/LICENSE)

This module discover the programming languages from a project/repository.

## Usage

-   **Module**

    > test.py
    >
    > ``` python
    > from detect_languages.detect import DetectLanguages
    >
    > detect_languages = DetectLanguages(debug=False, path=".", language_types=["programming"], exclude_dirs=[".venv", ".tox", "samples"], exclude_dirs_recursively=False)
    >
    > print("Main language: ", detect_languages.main_language)
    > print("All languages: ", detect_languages.all_languages)
    > ```
    >     $ python test.py
    >
    > Output:
    >
    >     Main language:  Python
    >     All languages:  {'Python': {'size': 50799, 'percentage': 100.0}}

-   **CLI**

    > Help:
    >
    >     $ detect-languages --help
    >
    > Output:
    >
    >     Usage: detect-languages [OPTIONS] COMMAND [ARGS]...
    >
    >     Options:
    >       --help  Show this message and exit.
    >
    >     Commands:
    >       all
    >       main
    >
    > Main language help:
    >
    >     detect-languages main --help
    >
    > Output:
    >
    >     Usage: detect-languages main [OPTIONS]
    >     
    >     Options:
    >       -d, --debug / --no-debug        Debug  [default: no-debug]
    >       -p, --path PATH                 Path to project  [default: .]
    >       -lt, --language-types TEXT      Language types  [default: programming, 
    >                                       prose, data, markup]
    >       -ed, --exclude-dirs TEXT        Exclude dirs
    >       -edr, --exclude-dirs-recursively / --no-exclude-dirs-recursively       
    >                                       Exclude dirs recursively  [default: no-
    >                                       exclude-dirs-recursively]
    >       -o, --output [json|tabulate]    Output format  [default: tabulate]     
    >       --help                          Show this message and exit.
    >
    > All languages help:
    >
    >     detect-languages all --help
    >
    > Output:
    >
    >     Usage: detect-languages all [OPTIONS]
    >     
    >     Options:
    >       -d, --debug / --no-debug        Debug  [default: no-debug]
    >       -p, --path PATH                 Path to project  [default: .]
    >       -lt, --language-types TEXT      Language types  [default: programming, 
    >                                       prose, data, markup]
    >       -ed, --exclude-dirs TEXT        Exclude dirs
    >       -edr, --exclude-dirs-recursively / --no-exclude-dirs-recursively       
    >                                       Exclude dirs recursively  [default: no-
    >                                       exclude-dirs-recursively]
    >       -o, --output [json|tabulate]    Output format  [default: tabulate]     
    >       --help                          Show this message and exit.
    >
    > Main language example:
    >
    >     detect-languages main -ed .venv -ed .tox -ed .github -ed .pytest_cache -ed .vscode -ed samples -p . -o json
    >
    > Output:
    >
    >     {'Python': {'size': 52455, 'percentage': 63.51}}
    >
    > All languages example:
    >
    >     detect-languages all -ed .venv -ed .tox -ed .github -ed .pytest_cache -ed .vscode -ed samples -p . -o json
    >
    > Output:
    >
    >     {'Python': {'size': 52455, 'percentage': 63.46}, 'JSON': {'size': 24481, 'percentage': 29.62}, 'Markdown': {'size': 4728, 'percentage': 5.72}, 'INI': {'size': 725, 'percentage': 0.88}, 'TOML': {'size': 271, 'percentage': 0.33}}
    >
    > Debug:
    >
    >     detect-languages all -ed .venv -ed .tox -ed .github -ed .pytest_cache -ed .vscode -ed samples -p . -o json -d
    >
    > Output:
    >
    >     DEBUG: Detecting languages...
    >     DEBUG: Language types: ['programming', 'prose', 'data', 'markup']
    >     DEBUG: no lexer for filename '.gitignore' found
    >     DEBUG: file: './.gitignore', language: 'None', size: 111
    >     DEBUG: no lexer for filename 'LICENSE' found
    >     DEBUG: file: './LICENSE', language: 'None', size: 1074
    >     DEBUG: file: './README.md', language: 'Markdown', size: 7648
    >     DEBUG: file: './Pipfile.lock', language: 'JSON', size: 24481
    >     DEBUG: file: './setup.py', language: 'Python', size: 1166
    >     DEBUG: file: './tox.ini', language: 'INI', size: 160
    >     DEBUG: file: './requirements.txt', language: 'Text only', size: 426
    >     DEBUG: file: './.bumpversion.cfg', language: 'INI', size: 532
    >     DEBUG: file: './Pipfile', language: 'TOML', size: 271
    >     DEBUG: file: './detect_languages.egg-info/top_level.txt', language: 'Text only', size: 17
    >     DEBUG: file: './detect_languages.egg-info/dependency_links.txt', language: 'Text only', size: 1
    >     DEBUG: file: './detect_languages.egg-info/entry_points.txt', language: 'Text only', size: 63
    >     DEBUG: file: './detect_languages.egg-info/SOURCES.txt', language: 'Text only', size: 378
    >     DEBUG: file: './detect_languages.egg-info/requires.txt', language: 'Text only', size: 63
    >     DEBUG: no lexer for filename 'PKG-INFO' found
    >     DEBUG: file: './detect_languages.egg-info/PKG-INFO', language: 'None', size: 8378
    >     DEBUG: file: './tests/test_cli.py', language: 'Python', size: 726
    >     DEBUG: file: './tests/test_detect.py', language: 'Python', size: 1608
    >     DEBUG: file: './detect_languages/languages.py', language: 'Python', size: 37666
    >     DEBUG: file: './detect_languages/cli.py', language: 'Python', size: 3009
    >     DEBUG: file: './detect_languages/detect.py', language: 'Python', size: 6852
    >     DEBUG: Detected main language: Python
    >     DEBUG: Detected languages: ['Python', 'JSON', 'Markdown', 'INI', 'TOML']
    >     {'Python': {'size': 51027, 'percentage': 60.66}, 'JSON': {'size': 24481, 'percentage': 29.1}, 'Markdown': {'size': 7648, 'percentage': 9.09}, 'INI': {'size': 692, 'percentage': 0.82}, 'TOML': {'size': 271, 'percentage': 0.32}}
    >

## Installation

    $ pip install detect-languages

### Requirements

-   [Python 3.7+](https://www.python.org/downloads/)
-   [pygments](https://pypi.org/project/Pygments/)
-   [jmespath](https://pypi.org/project/jmespath/)
-   [click](https://pypi.org/project/click/)
-   [tabulate](https://pypi.org/project/tabulate/)

## Credits/Inspirations
-   [aymen-mouelhi](https://gist.github.com/aymen-mouelhi/82c93fbcd25f091f2c13faa5e0d61760)
-   [douban](https://github.com/douban/linguist)

## Licence

[MIT](https://github.com/alexgracianoarj/detect-languages/blob/main/LICENSE)

## Author

[Alex Graciano](mailto:alexgracianoarj@gmail.com)
