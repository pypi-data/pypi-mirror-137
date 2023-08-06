from setuptools import setup, find_packages
import os

version = '5.0'
name = 'slapos.recipe.template'
long_description = '\n'.join((open(path).read() for path in (
    "README.rst",
    os.path.join('slapos', 'recipe', 'template', "README.txt"),
    os.path.join('slapos', 'recipe', 'template', "README.jinja2.txt"),
    "CHANGELOG.rst")))

setup(name=name,
      version=version,
      description="Templating recipe with remote resource support.",
      long_description=long_description,
      classifiers=[
          "Framework :: Buildout :: Recipe",
          "Programming Language :: Python",
      ],
      keywords='slapos recipe',
      license='GPLv3',
      namespace_packages=['slapos', 'slapos.recipe'],
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'setuptools', # namespaces
          'six',
          'zc.buildout', # plays with buildout
          'jinja2>=2.7',
      ],
      tests_require=[
          'zope.testing',
      ],
      zip_safe=True,
      entry_points={
          'zc.buildout': [
              'default = slapos.recipe.template:Recipe',
              'jinja2 = slapos.recipe.template.jinja2_template:Recipe',
      ]},
      test_suite = "slapos.recipe.template.tests.test_suite",
)
