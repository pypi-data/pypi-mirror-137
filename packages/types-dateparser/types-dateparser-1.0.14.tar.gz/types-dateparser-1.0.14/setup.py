from setuptools import setup

name = "types-dateparser"
description = "Typing stubs for dateparser"
long_description = '''
## Typing stubs for dateparser

This is a PEP 561 type stub package for the `dateparser` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `dateparser`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/dateparser. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `fc60d02c3ea5ca006d0e8244c556f48d697a7c66`.
'''.lstrip()

setup(name=name,
      version="1.0.14",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/dateparser.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['dateparser-stubs', 'dateparser_data-stubs'],
      package_data={'dateparser-stubs': ['__init__.pyi', 'calendars/__init__.pyi', 'calendars/hijri.pyi', 'calendars/hijri_parser.pyi', 'calendars/jalali.pyi', 'calendars/jalali_parser.pyi', 'conf.pyi', 'data/__init__.pyi', 'data/languages_info.pyi', 'date.pyi', 'date_parser.pyi', 'freshness_date_parser.pyi', 'languages/__init__.pyi', 'languages/dictionary.pyi', 'languages/loader.pyi', 'languages/locale.pyi', 'languages/validation.pyi', 'parser.pyi', 'search/__init__.pyi', 'search/detection.pyi', 'search/search.pyi', 'search/text_detection.pyi', 'timezone_parser.pyi', 'timezones.pyi', 'utils/__init__.pyi', 'utils/strptime.pyi', 'METADATA.toml'], 'dateparser_data-stubs': ['__init__.pyi', 'settings.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
