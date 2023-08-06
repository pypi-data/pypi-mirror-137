# ML Bricks
A package for reusing functions that repeat during machine learning and data science related works

[![Tests](https://github.com/jerinka/ml_bricks/actions/workflows/main.yml/badge.svg)](https://github.com/jerinka/ml_bricks/actions/workflows/main.yml)

[![pypi](https://github.com/jerinka/ml_bricks/actions/workflows/python-publish.yml/badge.svg)](https://github.com/jerinka/ml_bricks/actions/workflows/python-publish.yml)

# Install from Pypi
```pip install ml_bricks```

# Local install
```git clone https://github.com/jerinka/ml_bricks```\
```pip3 install -e ml_bricks```

# Test and Coverage
```coverage run --source=ml_bricks/ -m pytest -v test/ && coverage report -m```\
```coverage html -d coverage_html```

# build
```pip install wheel```\
```python setup.py sdist bdist_wheel```

# testpypi
```twine upload --repository testpypi dist/* ```\
```pip install -i https://test.pypi.org/simple/ ml_bricks ```

# pypi
```twine upload dist/*```\
```pip install -U ml_bricks```

# Quick usage
```import ml_bricks as pk1```\
```pk1.subpackage1.moduleA.fun_a()```


# Reference
[https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56](https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56)









