import io
import logging
import pathlib
import re
import sys
import types

from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from nbformat import read

log = logging.getLogger(__name__)


def find_imports(code: str):
    """Match imports

    This code matches
    >>> import abc
    >>> from abc import ABC
    for the beginning of a new line
    """
    return re.search(r"(^|\r|\n|\r\n)(import|from)", code)


def find_functions(code: str):
    """Match functions

    This code matches everything that contains "def"
    """
    return re.search("def ", code)


def find_classes(code: str):
    """Match classes

    This  code matches everything that contains "class"
    """
    return re.search("class ", code)


def find_decorators(code: str):
    """Match decorators

    This code matches everything that contains @<str>
    """
    return re.search(r"@[a-zA-Z]+", code)


class NotebookLoader:
    """Module Loader for Jupyter Notebooks

    References
    ----------
    Modified version of the example from
    jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html

    """

    def __init__(self, file):
        self.shell = InteractiveShell.instance()
        self.file = pathlib.Path(file).with_suffix(".ipynb")

    def load_module(
        self,
        run_imports=True,
        run_functions=True,
        run_classes=True,
        run_decorators=True,
        run_all=False,
    ):
        """import a notebook as a module

        Attributes
        ----------
        run_imports: bool, default=True
            Use exec on all matched import statements
        run_functions: bool, default=True
            Use exec on all matched function definitions
        run_classes: bool, default=True
            Use exec on all matched class defintions
        run_decorators:  bool, default=True
            Use exec on all matched decrorators
        run_all: bool, default=False
            Ignore regex and run everything
        """

        log.debug(f"importing Jupyter notebook from {self.file}")

        # load the notebook object
        with io.open(self.file, "r", encoding="utf-8") as f:
            nb = read(f, 4)

        # create the module and add it to sys.modules
        # if name in sys.modules:
        #    return sys.modules[name]
        mod = types.ModuleType(self.file.stem)
        mod.__file__ = self.file.as_posix()
        mod.__loader__ = self
        mod.__dict__["get_ipython"] = get_ipython
        sys.modules[self.file.stem] = mod

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        try:
            for cell in nb.cells:
                if cell.cell_type == "code":
                    # transform the input to executable Python
                    code = self.shell.input_transformer_manager.transform_cell(
                        cell.source
                    )
                    run_code = run_all
                    if run_imports and find_imports(code):
                        log.debug(f"Found import statement in \n{code}")
                        run_code = True
                    if run_functions and find_functions(code):
                        log.debug(f"Found function definition in \n{code}")
                        run_code = True
                    if run_classes and find_classes(code):
                        log.debug(f"Found class definition in \n{code}")
                        run_code = True
                    if run_decorators and find_decorators(code):
                        log.debug(f"Found decorator in \n{code}")
                        run_code = True

                    if run_code:
                        # run the code in the module to get e.g. all imports correctly
                        exec(code, mod.__dict__)
        finally:
            self.shell.user_ns = save_user_ns
        return mod
