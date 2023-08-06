from setuptools import setup

name = "types-mock"
description = "Typing stubs for mock"
long_description = '''
## Typing stubs for mock

This is a PEP 561 type stub package for the `mock` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `mock`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/mock. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `fc60d02c3ea5ca006d0e8244c556f48d697a7c66`.
'''.lstrip()

setup(name=name,
      version="4.0.10",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/mock.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['mock-stubs'],
      package_data={'mock-stubs': ['__init__.pyi', 'mock.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
