--------------
default recipe
--------------

The default recipe generates a file (option ``output``) from a template using
buildout expansion. The template is specified with either ``url`` (optionally
combined with ``md5sum``) or ``inline``.

Here is a simple buildout::

    >>> base = """
    ... [buildout]
    ... parts = template
    ...
    ... [section]
    ... option = value
    ...
    ... [template]
    ... recipe = slapos.recipe.template
    ... url = template.in
    ... output = template.out
    ... """
    >>> write('buildout.cfg', base)

A simple template::

    >>> write('template.in', '${section:option}')

And the output file has been parsed by buildout itself::

    >>> run_buildout()
    Installing template.
    >>> cat('template.out')
    value

The recipe relies on buildout expansion to pull sections it depends on, which
implies that the rendering (including the download if requested) is done during
the initialization phase.

Options
-------

``md5sum`` - check file integrity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the template is specified with the ``url`` option, an MD5 checksum can be
given to check the contents of the template::

    >>> base += """
    ... md5sum = 1993226f57db37c4a19cb785f826a1aa
    ... """
    >>> write(sample_buildout, 'buildout.cfg', base)
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    >>> cat('template.out')
    value

In such case, updating the part does nothing::

    >>> write('template.out', 'altered')
    >>> run_buildout()
    Updating template.
    >>> cat('template.out')
    altered

In case of checksum mismatch::

    >>> run_buildout('template:md5sum=00000000000000000000000000000000')
    While:
      Installing.
      Getting section template.
      Initializing section template.
    Error: MD5 checksum mismatch for local resource at 'template.in'.

``inline``
~~~~~~~~~~

You may prefer to inline small templates::

    >>> write('buildout.cfg', """
    ... [buildout]
    ... parts = template
    ...
    ... [section]
    ... option = inlined
    ...
    ... [template]
    ... recipe = slapos.recipe.template
    ... inline = ${section:option}
    ... output = template.out
    ... """)
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    >>> cat('template.out')
    inlined

Note that in such case, the rendering is done by buildout itself:
it just creates a file with the value of ``inline``.

``mode`` - specify filesystem permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, executable permissions are set if the content of the output file
looks like an executable script, i.e. it has a shebang that points to an
executable file. This is done by respecting umask::

    >>> import os, stat
    >>> os.access('template.out', os.X_OK)
    False
    >>> run_buildout('section:option=#!/bin/sh')
    Uninstalling template.
    Installing template.
    >>> os.access('template.out', os.X_OK)
    True

File permissions can be forced using the ``mode`` option in octal representation
(no need for 0-prefix)::

    >>> run_buildout('template:mode=627')
    Uninstalling template.
    Installing template.
    >>> print(oct(stat.S_IMODE(os.stat('template.out').st_mode)))
    0627
