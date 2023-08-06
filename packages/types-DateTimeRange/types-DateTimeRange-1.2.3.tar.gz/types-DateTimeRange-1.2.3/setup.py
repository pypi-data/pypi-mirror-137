from setuptools import setup

name = "types-DateTimeRange"
description = "Typing stubs for DateTimeRange"
long_description = '''
## Typing stubs for DateTimeRange

This is a PEP 561 type stub package for the `DateTimeRange` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `DateTimeRange`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/DateTimeRange. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `494481a0aed2ef0e00bbe190476ace0b8261bce6`.
'''.lstrip()

setup(name=name,
      version="1.2.3",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/DateTimeRange.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-python-dateutil'],
      packages=['datetimerange-stubs'],
      package_data={'datetimerange-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
