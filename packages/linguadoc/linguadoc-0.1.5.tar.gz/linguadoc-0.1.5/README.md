# Installation

```
pip3 install --verbose linguadoc 
```

# Usage

Please refer to [api docs](https://qishe-nlp.github.io/linguadoc/).

### Execute usage

* Convert json into docx
```
gen_lingua_docx --sourcejson [source.json] --lang [en/de/es] --destdocx [output.docx] --title [test_title]
```

### Package usage
```

```

# Development

### Clone project
```
git clone https://github.com/qishe-nlp/linguadoc.git
```

### Install [poetry](https://python-poetry.org/docs/)

### Install dependencies
```
poetry update
```

### Test
```
poetry run pytest -rP --capture=sys
```
which run tests under `tests/*`


### Execute
```
poetry run gen_lingua_docx --help
```

### Create sphinx docs
```
poetry shell
cd apidocs
sphinx-apidoc -f -o source ../linguadoc
make html
python -m http.server -d build/html
```

### Host docs on github pages
```
cp -rf apidocs/build/html/* docs/
```

### Build
* Change `version` in `pyproject.toml` and `linguadoc/__init__.py`
* Build python package by `poetry build`

### Git commit and push

### Publish from local dev env
* Set pypi test environment variables in poetry, refer to [poetry doc](https://python-poetry.org/docs/repositories/)
* Publish to pypi test by `poetry publish -r test`

### Publish through CI 
* Github action build and publish package to [test pypi repo](https://test.pypi.org/)

```
git tag [x.x.x]
git push origin master
```

* Manually publish to [pypi repo](https://pypi.org/) through [github action](https://github.com/qishe-nlp/linguappt/actions/workflows/pypi.yml)

