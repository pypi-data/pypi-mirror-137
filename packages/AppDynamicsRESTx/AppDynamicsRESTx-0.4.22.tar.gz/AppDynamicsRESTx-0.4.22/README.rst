============================
AppDynamics REST API Library
============================

Current version: 0.4.22


Introduction
------------

AppDynamicsRESTx is a library that provides a clean Python interface to the
REST API of an AppDynamics controller.

AppDynamicsRESTx is developed using Python 2.7.6 on Mac OSX. It is known to
work on most Linux distributions and on Windows, with your choice of Python 2.6, 2.7,
3.3, 3.4, 3.5, 3.6, 3.7, or 3.8.


Installation
------------

Install via ``pip``::

    $ pip install AppDynamicsRESTx

Install from source::

    $ git clone https://github.com/homedepot/AppDynamicsRESTx.git
    $ cd AppDynamicsRESTx
    $ python setup.py install


Prerequisites
-------------

 * `requests <https://pypi.python.org/pypi/requests>`_
 * `argparse <https://pypi.python.org/pypi/argparse>`_
 * `nose <https://pypi.python.org/pypi/nose>`_ (for running unit tests)
 * `tzlocal <https://pypi.python.org/pypi/tzlocal>`_ and
   `lxml <https://pypi.python.org/pypi/lxml>`_ (used by some of the example scripts)
 * `jinja2 <https://pypi.python,org/pypi/jinja2>`_ (used by the audit report example)


Documentation
-------------

The documentation is hosted online at readthedocs.org_.


A Quick Example
---------------

Here's a simple example that retrieves a list of business applications
from a controller on localhost, and prints them out:

.. code:: python

    from appd.request import AppDynamicsClient

    c = AppDynamicsClient('http://localhost:8090', 'user1', 'password', 'customer1', verbose=True)
    for app in c.get_applications():
        print app.name, app.id


Testing
-------

If you have cloned the repo, you can run the unit tests from ``setup.py``::

    python setup.py test

Or, if you have ``nose`` installed, you can use that::

    nosetests


For More Information
--------------------

The main source repo is on Github_.



.. _AppDynamics: http://www.appdynamics.com/
.. _Github: https://github.com/homedepot/AppDynamicsRESTx
.. _readthedocs.org: http://AppDynamicsREST.readthedocs.org/en/latest/
