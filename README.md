UNDER DEVELOPMENT

# EasyML

An easy to use framework to generate simple and maintainable machine learning web applications.

### Language

Python 3

### Developement

```sh
git clone https://github.com/gokhangerdan/EasyML
```

Create new nodes and tests of them in core/NodeRepository like the examples: column_filter.py, test_column_filter.py, column_rename.py, test_column_rename.py
In core/NodeRepository/\_\_init\_\_.py import new nodes and tests than append them to \_\_all\_\_

### Test

For testing all nodes

```sh
git clone https://github.com/gokhangerdan/EasyML
cd EasyML/core
python3 test.py
```

For testing specific nodes

```sh
python3 test.py new_node column_filter column_name
```


