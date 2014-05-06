Riemann Client
==============

A command-line tool for [Riemann](http://github.com/aphyr/riemann) based on the [bernhard](https://github.com/banjiewen/bernhard) python API.

Installation
------------

    $ git clone https://github.com/satterly/python-riemann-client.git
    $ python setup.py install

Usage
-----

    $ riemann-client query 'service=~"%"'

    Event #0:
      time = 1399389487 - Tue May  6 15:18:07 2014
      state = ok
      service = riemann netty execution-handler queue size
      host = vagrant-ubuntu-raring-64
      description =
      ttl = 20000.0
      metric_sint64 = 0
      metric_d = 0
      metric_f = 0.0

License
-------

Copyright (c) 2013 Nick Satterly. Available under the MIT License.
