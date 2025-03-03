<!--- Vim: set foldlevel=1: -->
# Contributing
## Implementation

`pdf-yaml-bookmark` consists of three parts:

1. A conversion from `.bkm` to `.yaml` (`src/pdf_yaml_bookmark/bkm_to_yaml.py`).
Parses the original `.bkm` format and converts it into YAML. This is a line-by-line process, with no global state except for `offset`.

2. A conversion from `.yaml` to `.gs` (`src/pdf_yaml_bookmark/yaml_to_gs.py`).
PyYAML parses the YAML, converts it into a Python object, and then generates Ghostscript commands.

3. Execution of Ghostscript (`src/pdf_yaml_bookmark/run_gs.py`).
Calls `gs` as an external command. It uses Adobe [`pdfmark`](https://opensource.adobe.com/dc-acrobat-sdk-docs/library/pdfmark/pdfmark_Basic.html#bookmarks-out).

The first process is the most important. It delegates the most technically complex task—indentation parsing—to PyYAML. All indentation in the `.bkm` file, whether whitespace or tabs, remains unchanged in the first process. PyYAML is then responsible for interpreting this indentation.

## Installation for development

We recommend the following steps for development:

1. Clone the repository:
   ```console
   $ git clone git@github.com:yutayamamoto/pdf-yaml-bookmark.git
   $ cd pdf-yaml-bookmark
   ```

2. Set up a virtual environment:
   ```console
   $ python -m venv venv
   $ source venv/bin/activate
   ```

3. Install dependencies:
   ```console
   $ pip install -e .
   ```

Make sure to install in editable mode (`-e`), which is necessary for tests to function as intended.

## Running tests

We use `unittest` for testing. Run the following command at the root of the project:

```console
$ python -m unittest discover tests

Ran 2 tests in 0.003s
OK
```

Make sure to run tests manually, whether they are existing ones or newly added. All tests must pass in any pull request (PR), although they do not necessarily need to pass for each individual commit (it is good to write tests such that they *fail* before making changes to the source).
