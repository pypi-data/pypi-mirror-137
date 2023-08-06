============
Contributing
============

Welcome to ``pydeltasnow`` contributor's guide. This document focuses on
getting you familiarized with the development processes, but
`other kinds of contributions`_ are also appreciated.
All users and contributors are expected to be open, inclusive,
considerate, reasonable, and respectful.


Issue Reports
=============

Bugs or general issues are recorded on the `issue tracker`_. Please feel
free to place an issue report if you encounter a problem.


Documentation Improvements
==========================

You can help improve the documentation by making it more readable and coherent,
or by adding missing information and correcting mistakes.

When working on documentation changes in your local machine, you can
compile them using |tox|_::

    tox -e docs


Code Contributions
==================

The deltasnow model routines are implementetd in the :mod:`.core` module. The 
:mod:`.utils` module holds functions for data validation and missing value
handling. The :mod:`.main` module provides an interface to the deltaSNOW model 
with the :func:`.swe_deltasnow` function.


Create an environment
---------------------

Before you start coding, it is recommended to create an isolated `virtual
environment`_ to avoid any problems with your installed Python packages.
This can easily be done via either |virtualenv|_::

    virtualenv <PATH TO VENV>
    source <PATH TO VENV>/bin/activate

or Miniconda_::

    conda create -n pydeltasnow python=3 six virtualenv pytest pytest-cov
    conda activate pydeltasnow

Clone the repository
--------------------

#. Create an user account on |the repository service| if you do not already have one.
#. Fork the project repository_: click on the *Fork* button near the top of the
   page. This creates a copy of the code under your account on |the repository service|.
#. Clone this copy to your local disk::

    git clone git@github.com:YourLogin/pydeltasnow.git

#. Navigate to the folder to which git downloaded the repository::

    cd pydeltasnow

#. You should run::

    pip install -U pip setuptools -e .

   in order to install ``pydeltasnow`` in editing mode and directly use your local 
   changes.

Implement your changes
----------------------

#. Create a branch to hold your changes::

    git checkout -b my-feature

   and start making changes. Never work on the main branch.

#. Start your work on this branch. Please include tests if you implement new
   functionality and add docstrings_ to new functions, modules and classes,
   especially if they are part of public APIs.

#. Please check that your changes don't break any unit tests with::

    tox

   (after having installed |tox|_ with ``pip install tox``).

   You can also use |tox|_ to run several other pre-configured tasks in the
   repository. Try ``tox -av`` to see a list of the available checks.

#. When you are done editing, use::

    git add <MODIFIED FILES>
    git commit

   to record your changes in git_.


Submit your contribution
------------------------

#. If everything works fine, push your local branch to |the repository service| with::

    git push -u origin my-feature

#. Go to the web page of your fork and click |contribute button|
   to send your changes for review.

Troubleshooting
---------------

The following tips can be used when facing problems to build or test the
package:

#. Make sure to fetch all the tags from the upstream repository_.
   The command ``git describe --abbrev=0 --tags`` should return the version you
   are expecting. If you are trying to run CI scripts in a fork repository,
   make sure to push all the tags.
   You can also try to remove all the egg files or the complete egg folder, i.e.,
   ``.eggs``, as well as the ``*.egg-info`` folders in the ``src`` folder or
   potentially in the root of your project.

#. Sometimes |tox|_ misses out when new dependencies are added, especially to
   ``setup.cfg`` and ``docs/requirements.txt``. If you find any problems with
   missing dependencies when running a command with |tox|_, try to recreate the
   ``tox`` environment using the ``-r`` flag. For example, instead of::

    tox -e docs

   Try running::

    tox -r -e docs

#. Make sure to have a reliable |tox|_ installation that uses the correct
   Python version (e.g., 3.7+). When in doubt you can run::

    tox --version
    # OR
    which tox

   If you have trouble and are seeing weird errors upon running |tox|_, you can
   also try to create a dedicated `virtual environment`_ with a |tox|_ binary
   freshly installed. For example::

    virtualenv .venv
    source .venv/bin/activate
    .venv/bin/pip install tox
    .venv/bin/tox -e all

#. Right now, tox is set up with anaconda. In case you encounter problems with
   the environment creation, you might need to change the envlist parameters in
   ``tox.ini`` from ``pythonX.X`` to ``pyXX``.

#. `Pytest can drop you`_ in an interactive session in the case an error occurs.
   In order to do that you need to pass a ``--pdb`` option (for example by
   running ``tox -- -k <NAME OF THE FALLING TEST> --pdb``).
   You can also setup breakpoints manually instead of using the ``--pdb`` option.


Maintainer tasks
================

Releases
--------


If you have write access to the repository_, the following steps can be used
to release a new version for ``pydeltasnow``:

#. Make sure all unit tests are successful locally and there ar no CI failures.
#. Tag the current commit on the main branch with a release tag, e.g., ``v1.2.3``.
#. Push the new tag to the upstream repository_, e.g., ``git push upstream v1.2.3``
   The CI will then publish to TestPyPi and you can have a look if everythin is
   okay.
#. Create a release on |the repository service| and assiciate it with the tag 
   you just created. 
#. Publish the release on |the repository service|. This will trigger a CI job 
   that builds the package and publishes it to PyPi.




.. <-- strart -->

.. |the repository service| replace:: GitHub
.. |contribute button| replace:: "Create pull request"

.. _repository: https://github.com/joAschauer/pydeltasnow
.. _issue tracker: https://github.com/joAschauer/pydeltasnow/issues
.. <-- end -->


.. |virtualenv| replace:: ``virtualenv``
.. |tox| replace:: ``tox``


.. _black: https://pypi.org/project/black/
.. _CommonMark: https://commonmark.org/
.. _contribution-guide.org: http://www.contribution-guide.org/
.. _creating a PR: https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
.. _descriptive commit message: https://chris.beams.io/posts/git-commit
.. _docstrings: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
.. _first-contributions tutorial: https://github.com/firstcontributions/first-contributions
.. _flake8: https://flake8.pycqa.org/en/stable/
.. _git: https://git-scm.com
.. _GitHub's fork and pull request workflow: https://guides.github.com/activities/forking/
.. _guide created by FreeCodeCamp: https://github.com/FreeCodeCamp/how-to-contribute-to-open-source
.. _Miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _MyST: https://myst-parser.readthedocs.io/en/latest/syntax/syntax.html
.. _other kinds of contributions: https://opensource.guide/how-to-contribute
.. _pre-commit: https://pre-commit.com/
.. _PyPI: https://pypi.org/
.. _PyScaffold's contributor's guide: https://pyscaffold.org/en/stable/contributing.html
.. _Pytest can drop you: https://docs.pytest.org/en/stable/usage.html#dropping-to-pdb-python-debugger-at-the-start-of-a-test
.. _Python Software Foundation's Code of Conduct: https://www.python.org/psf/conduct/
.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _tox: https://tox.readthedocs.io/en/stable/
.. _virtual environment: https://realpython.com/python-virtual-environments-a-primer/
.. _virtualenv: https://virtualenv.pypa.io/en/stable/

.. _GitHub web interface: https://docs.github.com/en/github/managing-files-in-a-repository/managing-files-on-github/editing-files-in-your-repository
.. _GitHub's code editor: https://docs.github.com/en/github/managing-files-in-a-repository/managing-files-on-github/editing-files-in-your-repository
