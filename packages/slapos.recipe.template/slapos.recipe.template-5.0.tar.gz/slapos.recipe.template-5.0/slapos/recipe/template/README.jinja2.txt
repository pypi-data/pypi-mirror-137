----------
``jinja2``
----------

Similar to the default recipe but the template syntax is Jinja2 instead of
buildout. Other significant differences are:

- Rendering, and download if requested, is done during the install phase.
- Dependencies are explicit (see ``context`` option) instead of deduced from
  the template.
- Some extra features (options detailed below).

For backward compatibility, the following old options are still supported:

- The generated file can be specified with ``rendered`` instead of ``output``.
- The template can be specified with ``template`` instead of ``url``/``inline``.
  An inline template is prefixed with ``inline:`` + an optional newline.

Example demonstrating some types::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... url = foo.in
    ... output = foo
    ... context =
    ...     key     bar          section:key
    ...     key     recipe       :recipe
    ...     raw     knight       Ni !
    ...     import  json_module  json
    ...     section param_dict   parameter-collection
    ...
    ... [parameter-collection]
    ... foo = 1
    ... bar = bar
    ...
    ... [section]
    ... key = value
    ... ''')

And according Jinja2 template (kept simple, control structures are possible)::

    >>> write('foo.in',
    ...     '{{bar}}\n'
    ...     'Knights who say "{{knight}}"\n'
    ...     '${this:is_literal}\n'
    ...     '${foo:{{bar}}}\n'
    ...     'swallow: {{ json_module.dumps(("african", "european")) }}\n'
    ...     'parameters from section: {{ param_dict | dictsort }}\n'
    ...     'Rendered with {{recipe}}\n'
    ...     'UTF-8 text: привет мир!\n'
    ...     'Unicode text: {{ "你好世界" }}\n'
    ... )

We run buildout::

    >>> run_buildout()
    Installing template.

And the template has been rendered::

    >>> cat('foo')
    value
    Knights who say "Ni !"
    ${this:is_literal}
    ${foo:value}
    swallow: ["african", "european"]
    parameters from section: [('bar', 'bar'), ('foo', '1')]
    Rendered with slapos.recipe.template:jinja2
    UTF-8 text: привет мир!
    Unicode text: 你好世界

Options
-------

``md5sum``, ``mode``
~~~~~~~~~~~~~~~~~~~~

Same as for the default recipe.

``once`` - avoiding file re-creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Path of a marker file to prevents rendering altogether.

Normally, each time the section is installed/updated the file gets
re-generated. This may be undesirable in some cases.

``once`` allows specifying a marker file, which when present prevents template
rendering::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... inline = dummy
    ... output = foo_once
    ... once = foo_flag
    ... ''')
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    The template install returned None.  A path or iterable os paths should be returned.

Template was rendered::

    >>> cat('foo_once')
    dummy

And canary exists::

    >>> import os
    >>> os.path.exists('foo_flag')
    True

Remove rendered file and re-render::

    >>> os.unlink('foo_once')
    >>> with open('buildout.cfg', 'a') as f:
    ...     f.writelines(['extra = useless'])
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    The template install returned None.  A path or iterable os paths should be returned.
    Unused options for template: 'extra'.

Template was not rendered::

   >>> os.path.exists('foo_once')
   False

Removing the canary allows template to be re-rendered::

    >>> os.unlink('foo_flag')
    >>> with open('buildout.cfg', 'a') as f:
    ...     f.writelines(['moreextra = still useless'])
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    The template install returned None.  A path or iterable os paths should be returned.
    Unused options for template: 'extra'.
    >>> cat('foo_once')
    dummy

It's also possible to use the same file for ``rendered`` and ``once``::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... inline = initial content
    ... output = rendered
    ... once = ${:output}
    ... ''')
    >>> run_buildout() # doctest: +ELLIPSIS
    Uninstalling template.
    Installing template.
    The template install returned None.  A path or iterable os paths should be returned.

Template was rendered::

    >>> cat('rendered')
    initial content

When buildout options are modified, the template will not be rendered again::

    >>> with open('buildout.cfg', 'a') as f:
    ...     f.writelines(['inline = something different'])

    >>> run_buildout()
    Uninstalling template.
    Installing template.
    The template install returned None.  A path or iterable os paths should be returned.

Even though we used a different template, the file still contain the first template::

    >>> cat('rendered')
    initial content

``context`` - template variables and section dependency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Jinja2 context specification, one variable per line, with 3 whitespace-separated
parts: type, name and expression. Available types are described below. "name" is
the variable name to declare. Expression semantic varies depending on the type.

Available types:

``raw``
  Immediate literal string.

``key``
  Indirect literal string.

``import``
  Import a python module.

``section``
  Make a whole buildout section available to template, as a dictionary.

Indirection targets are specified as: [section]:key .
It is possible to use buildout's buit-in variable replacement instead instead
of ``key`` type, but keep in mind that different lines are different
variables for this recipe. It might be what you want (factorising context
chunk declarations), otherwise you should use indirect types.

You can use other part of buildout in the template. This way this parts
will be installed as dependency::

    >>> write('buildout.cfg', '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... inline = {{bar}}
    ... output = foo
    ... context = key bar dependency:foobar
    ...
    ... [dependency]
    ... foobar = dependency content
    ... recipe = zc.buildout:debug
    ... ''')

    >>> run_buildout()
    Uninstalling template.
    Installing dependency.
      foobar='dependency content'
      recipe='zc.buildout:debug'
    Installing template.

This way you can get options which are computed in the ``__init__`` of
the dependent recipe.

Let's create a sample recipe modifying its option dict::

    >>> write('setup.py',
    ... '''
    ... from setuptools import setup
    ...
    ... setup(name='samplerecipe',
    ...       entry_points = {
    ...           'zc.buildout': [
    ...                'default = main:Recipe',
    ...           ],
    ...       }
    ...      )
    ... ''')
    >>> write('main.py',
    ... '''
    ... class Recipe(object):
    ...
    ...     def __init__(self, buildout, name, options):
    ...         options['data'] = 'foobar'
    ...
    ...     def install(self):
    ...         return []
    ... ''')

Let's just use ``buildout.cfg`` using this egg::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... develop = .
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... inline =
    ...   {{bar}}
    ... output = foo
    ... context = key bar sample:data
    ...
    ... [sample]
    ... recipe = samplerecipe
    ... ''')
    >>> run_buildout()
    Develop: '/sample-buildout/.'
    Uninstalling template.
    Uninstalling dependency.
    Installing sample.
    Installing template.
    >>> cat('foo')
    foobar

``extensions`` - Jinja2 extensions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Jinja2 extensions to enable when rendering the template,
whitespace-separated. By default, none is loaded.

::

    >>> write('foo.in',
    ... '''{% set foo = ['foo'] -%}
    ... {% do foo.append(bar) -%}
    ... {{ foo | join(', ') }}''')
    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... develop = .
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... url = foo.in
    ... output = foo
    ... context = key bar buildout:parts
    ... # We don't actually use all those extensions in this minimal example.
    ... extensions = jinja2.ext.do jinja2.ext.loopcontrols
    ...   jinja2.ext.with_
    ... ''')
    >>> run_buildout()
    Develop: '/sample-buildout/.'
    Uninstalling template.
    Uninstalling sample.
    Installing template.

    >>> cat('foo')
    foo, template

``import-delimiter``, ``import-list`` - template imports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``import-delimiter`` specifies the delimiter character for in-temlate imports.
Defaults to ``/``.


``import-list`` is a list of import paths. Format is similar to ``context``.
"name" becomes import's base name. Available types:

``rawfile``
  Literal path of a file.

``file``
  Indirect path of a file.

``rawfolder``
  Literal path of a folder. Any file in such folder can be imported.

``folder``
  Indirect path of a folder. Any file in such folder can be imported.

Here is a simple template importing an equaly-simple library::

    >>> write('template.in', '''
    ... {%- import "library" as library -%}
    ... {{ library.foo() }}
    ... ''')
    >>> write('library.in', '{% macro foo() %}FOO !{% endmacro %}')

To import a template from rendered template, you need to specify what can be
imported::

    >>> write('buildout.cfg', '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... url = template.in
    ... output = bar
    ... import-list = rawfile library library.in
    ... ''')
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    >>> cat('bar')
    FOO !

Just like context definition, it also works with indirect values::

    >>> write('buildout.cfg', '''
    ... [buildout]
    ... parts = template
    ...
    ... [template-library]
    ... path = library.in
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... url = template.in
    ... output = bar
    ... import-list = file library template-library:path
    ... ''')
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    >>> cat('bar')
    FOO !

This also works to allow importing from identically-named files in different
directories::

    >>> write('template.in', '''
    ... {%- import "dir_a/1.in" as a1 -%}
    ... {%- import "dir_a/2.in" as a2 -%}
    ... {%- import "dir_b/1.in" as b1 -%}
    ... {%- import "dir_b/c/1.in" as bc1 -%}
    ... {{ a1.foo() }}
    ... {{ a2.foo() }}
    ... {{ b1.foo() }}
    ... {{ bc1.foo() }}
    ... ''')
    >>> mkdir('a')
    >>> mkdir('b')
    >>> mkdir(join('b', 'c'))
    >>> write(join('a', '1.in'), '{% macro foo() %}a1foo{% endmacro %}')
    >>> write(join('a', '2.in'), '{% macro foo() %}a2foo{% endmacro %}')
    >>> write(join('b', '1.in'), '{% macro foo() %}b1foo{% endmacro %}')
    >>> write(join('b', 'c', '1.in'), '{% macro foo() %}bc1foo{% endmacro %}')

All templates can be accessed inside both folders::

    >>> write('buildout.cfg', '''
    ... [buildout]
    ... parts = template
    ...
    ... [template-library]
    ... path = library.in
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... url = template.in
    ... output = bar
    ... import-list =
    ...     rawfolder dir_a a
    ...     rawfolder dir_b b
    ... ''')
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    >>> cat('bar')
    a1foo
    a2foo
    b1foo
    bc1foo

It is possible to override default path delimiter (without any effect on final
path)::

    >>> write('template.in', r'''
    ... {%- import "dir_a\\1.in" as a1 -%}
    ... {%- import "dir_a\\2.in" as a2 -%}
    ... {%- import "dir_b\\1.in" as b1 -%}
    ... {%- import "dir_b\\c\\1.in" as bc1 -%}
    ... {{ a1.foo() }}
    ... {{ a2.foo() }}
    ... {{ b1.foo() }}
    ... {{ bc1.foo() }}
    ... ''')
    >>> write('buildout.cfg', r'''
    ... [buildout]
    ... parts = template
    ...
    ... [template-library]
    ... path = library.in
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... url = template.in
    ... output = bar
    ... import-delimiter = \
    ... import-list =
    ...     rawfolder dir_a a
    ...     rawfolder dir_b b
    ... ''')
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    >>> cat('bar')
    a1foo
    a2foo
    b1foo
    bc1foo

``update`` - force rerendering on update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, and like the default recipe, nothing is done on update if the
template is known in advance to be the same, either because it's inline or
a md5sum is given::

    >>> write('buildout.cfg',
    ... '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... inline = {{ os.environ['FOO'] }}
    ... output = foo
    ... context = import os os
    ... ''')
    >>> os.environ['FOO'] = '1'
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    >>> cat('foo')
    1
    >>> os.environ['FOO'] = '2'
    >>> run_buildout()
    Updating template.
    >>> cat('foo')
    1

But Jinja2 is such that the output may depend on other things than buildout
data and it may be wanted to force update in such case::

    >>> with open('buildout.cfg', 'a') as f:
    ...     f.writelines(['update = true'])
    >>> run_buildout()
    Uninstalling template.
    Installing template.
    >>> cat('foo')
    2
    >>> os.environ['FOO'] = '1'
    >>> run_buildout()
    Updating template.
    >>> cat('foo')
    1
    >>> del os.environ['FOO']

``encoding``
~~~~~~~~~~~~

Encoding for input template and output file.
Defaults to ``utf-8``.

FAQ
---

Q: How do I generate ${foo:bar} where foo comes from a variable ?

A: ``{{ '${' ~ foo_var ~ ':bar}' }}``
   This is required as jinja2 fails parsing "${{{ foo_var }}:bar}". Though,
   jinja2 succeeds at parsing "${foo:{{ bar_var }}}" so this trick isn't
   needed for that case.

Errors in template
------------------

::

    >>> write('template.in', '''\
    ... foo
    ... {%
    ... bar
    ... ''')
    >>> write('buildout.cfg', '''
    ... [buildout]
    ... parts = template
    ...
    ... [template]
    ... recipe = slapos.recipe.template:jinja2
    ... url = template.in
    ... output = foo
    ... ''')
    >>> 0; run_buildout() # doctest: +ELLIPSIS
    0...
    While:
      Installing template.
    ...
    Traceback (most recent call last):
      ...
      File "template.in", line 3, in template
        bar
    ...TemplateSyntaxError: Encountered unknown tag 'bar'.
