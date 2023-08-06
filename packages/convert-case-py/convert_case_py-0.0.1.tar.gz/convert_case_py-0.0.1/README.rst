convert-case-py
================

.. image:: https://badge.fury.io/py/convert-case-py.svg
   :target: https://badge.fury.io/py/convert-case-py

.. image:: https://img.shields.io/pypi/pyversions/convert-case-py.svg
   :target: https://pypi.python.org/pypi/convert-case-py

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black

``convert-case-py`` is a Python package providing utils task to the Git.

Installation
------------

As of 0.0.1, ``convert-case-py`` is compatible with Python 3.7+.

Use ``pip`` to install the latest stable version of ``convert-case-py``:

.. code-block:: console

   $ pip install --upgrade convert-case-py

Command
-------------
Case.camelcase_to_lowercase(
            {'helloWorld': 1, 'helloWorldHuman': 'Value', 'testHelloWorld': {'otherTestHelloWorld': 'value'}})
Case.pascalcase_to_snakecase(
            {'HelloWorld': 1, 'HelloWorldHuman': 'Value', 'TestHelloWorld': {'OtherTestHelloWorld': 'value'}})
Case.camelcase_to_snakecase(
            {'helloWorld': 1, 'helloWorldHuman': 'Value', 'testHelloWorld': {'otherTestHelloWorld': 'value'}})
Case.snakecase_to_camelcase(
            {'hello_world': 1, 'hello_world_human': 'Value', 'test_hello_world': {'other_hello_world': 'value'}})
Case.snakecase_to_lowercase(
            {'hello_world': 1, 'hello_world_human': 'Value', 'test_hello_world': {'other_hello_world': 'value'}})
Case.snakecase_to_pascalcase(
            {'hello_world': 1, 'hello_world_human': 'Value', 'test_hello_world': {'other_hello_world': 'value'}})
