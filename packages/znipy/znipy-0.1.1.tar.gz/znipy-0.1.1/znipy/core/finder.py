import os
import sys

from znipy.core.loader import NotebookLoader


def register():
    sys.meta_path.append(NotebookFinder())


def find_notebook(fullname, path=None):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.

    References
    -----------
    jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html

    """
    name = fullname.rsplit(".", 1)[-1]
    if not path:
        path = [""]
    for d in path:
        nb_path = os.path.join(d, name + ".ipynb")
        if os.path.isfile(nb_path):
            return nb_path
        # let import Notebook_Name find "Notebook Name.ipynb"
        nb_path = nb_path.replace("_", " ")
        if os.path.isfile(nb_path):
            return nb_path


class NotebookFinder:
    """Module finder that locates Jupyter Notebooks

    References
    -----------
    jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html
    """

    def __init__(self):
        self.loaders = {}

    def find_module(self, fullname, path=None):
        nb_path = find_notebook(fullname, path)
        if not nb_path:
            return

        key = path
        if path:
            # lists aren't hashable
            key = os.path.sep.join(path)

        if key not in self.loaders:
            self.loaders[key] = NotebookLoader(path)
        return self.loaders[key]
