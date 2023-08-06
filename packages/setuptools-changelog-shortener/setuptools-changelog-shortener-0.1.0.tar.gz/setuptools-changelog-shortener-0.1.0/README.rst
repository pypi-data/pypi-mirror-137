setuptools-changelog-shortener
==============================

This setuptools plugin allows shortening the number of changelog entries to use for the ``long_description`` metadata in Python packages.


Usage
-----

First, ensure that ``setuptools_changelog_shortener`` is present in your build requirements.

.. code:: toml

    # pyproject.toml
    [build-system]
    requires = ["setuptools>=45", "wheel", "setuptools_changelog_shortener"]

To enable changelog shortening, add the following section to your ``pyproject.toml``:

.. code:: toml

    # pyproject.toml
    [tool.setuptools_changelog_shortener]
    read_from = "CHANGELOG.rst"
    write_to = "CHANGELOG.short.rst"

Then you use the ``CHANGELOG.short.rst`` file for your ``long_description`` metadata field.

Additional options are:

``count``
    The number of changelog entries to include.
    Defaults to ``5``.

``delimiter``
    The delimiter to look for in each entry.
    Defaults to the ``^--+`` regular expression to find docutils titles using ``-`` characters.

``title``
    The title to add to the top of the shortened CHANGELOG file.
    Defaults to ``Changelog\n=========``.
