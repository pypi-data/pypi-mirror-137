from setuptools import setup

name = "types-chevron"
description = "Typing stubs for chevron"
long_description = '''
## Typing stubs for chevron

This is a PEP 561 type stub package for the `chevron` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `chevron`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/chevron. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `62e33cbbd53e55334f5da8870f8f4b3ae8679ac2`.
'''.lstrip()

setup(name=name,
      version="0.14.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/chevron.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['chevron-stubs'],
      package_data={'chevron-stubs': ['__init__.pyi', 'main.pyi', 'metadata.pyi', 'renderer.pyi', 'tokenizer.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
