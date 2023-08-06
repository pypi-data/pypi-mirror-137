# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ammolite']

package_data = \
{'': ['*']}

install_requires = \
['biotite>=0.28']

setup_kwargs = {
    'name': 'ammolite',
    'version': '0.7.0',
    'description': 'Visualize structure data from Biotite with PyMOL',
    'long_description': ".. image:: https://raw.githubusercontent.com/biotite-dev/ammolite/master/doc/static/assets/ammolite_logo_s.png\n  :alt: Ammolite logo\n  :align: center\n\nAmmolite - From Biotite to PyMOL and back again\n====================================================\n\nThis package enables the transfer of structure related objects\nfrom `Biotite <https://www.biotite-python.org/>`_\nto `PyMOL <https://pymol.org/>`_ for visualization,\nvia PyMOL's Python API:\n\n- Import ``AtomArray`` and ``AtomArrayStack`` objects into *PyMOL* -\n  without intermediate structure files.\n- Convert *PyMOL* objects into ``AtomArray`` and ``AtomArrayStack`` instances.\n- Use *Biotite*'s boolean masks for atom selection in *PyMOL*.\n- Display images rendered with *PyMOL* in *Jupyter* notebooks.\n\nHave a look at `this example <https://ammolite.biotite-python.org/examples/gallery/heme_complex.html>`_:\n\n|\n\n.. image:: https://raw.githubusercontent.com/biotite-dev/ammolite/master/doc/demo/demo.gif\n    :alt: ammolite demo\n\n|\n\n*PyMOL is a trademark of Schrodinger, LLC.*\n",
    'author': 'Patrick Kunzmann',
    'author_email': 'patrick.kunzm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ammolite.biotite-python.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
