skeleton-says
=============

|code_ci| |docs_ci| |coverage| |pypi_version| |license|

A talking skeleton, just what everyone needs. It exists to illustrate the
principles of dls-python3-skeleton_ in story form. Look through the git
commit history to see the evolution of the ideas.

.. _dls-python3-skeleton: https://dls-controls.github.io/dls-python3-skeleton

============== ==============================================================
PyPI           ``pip install skeleton-says``
Source code    https://github.com/thomascobb/skeleton-says
Documentation  https://thomascobb.github.io/skeleton-says
Releases       https://github.com/thomascobb/skeleton-says/releases
============== ==============================================================

Primarily useful from the commandline::

    $ skeleton-says Hello

     -------
    ( Hello )
     -------
      \
       \  .-.
        \(o.o)
          |=|
         __|__
       //.=|=.\\
      // .=|=. \\
      \\ .=|=. //
       \\(_=_)//
        (:| |:)
         || ||
         () ()
         || ||
         || ||
    l42 ==' '==

Although it can also be embedded into an application.

.. code:: python

    from skeleton_says.say import say

    art = say("Hello")    


.. |code_ci| image:: https://github.com/thomascobb/skeleton-says/workflows/Code%20CI/badge.svg?branch=master
    :target: https://github.com/thomascobb/skeleton-says/actions?query=workflow%3A%22Code+CI%22
    :alt: Code CI

.. |docs_ci| image:: https://github.com/thomascobb/skeleton-says/workflows/Docs%20CI/badge.svg?branch=master
    :target: https://github.com/thomascobb/skeleton-says/actions?query=workflow%3A%22Docs+CI%22
    :alt: Docs CI

.. |coverage| image:: https://codecov.io/gh/thomascobb/skeleton-says/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/thomascobb/skeleton-says
    :alt: Test Coverage

.. |pypi_version| image:: https://img.shields.io/pypi/v/skeleton-says.svg
    :target: https://pypi.org/project/skeleton-says
    :alt: Latest PyPI version

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache License

..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

See https://thomascobb.github.io/skeleton-says for more detailed documentation.
