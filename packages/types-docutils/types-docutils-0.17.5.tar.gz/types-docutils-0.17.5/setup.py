from setuptools import setup

name = "types-docutils"
description = "Typing stubs for docutils"
long_description = '''
## Typing stubs for docutils

This is a PEP 561 type stub package for the `docutils` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `docutils`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/docutils. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `fc60d02c3ea5ca006d0e8244c556f48d697a7c66`.
'''.lstrip()

setup(name=name,
      version="0.17.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/docutils.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['docutils-stubs'],
      package_data={'docutils-stubs': ['__init__.pyi', 'core.pyi', 'examples.pyi', 'frontend.pyi', 'io.pyi', 'languages/__init__.pyi', 'nodes.pyi', 'parsers/__init__.pyi', 'parsers/null.pyi', 'parsers/recommonmark_wrapper.pyi', 'parsers/rst/__init__.pyi', 'parsers/rst/nodes.pyi', 'parsers/rst/roles.pyi', 'parsers/rst/states.pyi', 'readers/__init__.pyi', 'readers/doctree.pyi', 'readers/pep.pyi', 'readers/standalone.pyi', 'statemachine.pyi', 'transforms/__init__.pyi', 'utils/__init__.pyi', 'writers/__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
