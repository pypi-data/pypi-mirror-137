"""
Utility functions for pywbem testing
"""

from __future__ import absolute_import, print_function

import sys
import os
import types
try:
    from http.client import BadStatusLine
except ImportError:
    # Python 2
    from httplib import BadStatusLine
import urllib3
import six
import pytest
import requests
from ply import yacc, lex
from packaging.version import parse as parse_version


def skip_if_moftab_regenerated():
    """
    Skip the testcase if we run against an installed version of pywbem (as
    indicated by the TEST_INSTALLED environment variable), and the testcase
    would re-generate the MOF parsing table files.

    This function should be used by test cases that parse MOF files, so the
    test case is skipped in that case.

    Background:

    Pywbem uses the `ply` package to parse CIM MOF files and part of a pywbem
    installation are parsing table files named _mofparsetab.py and _moflextab.py
    that are generated by `ply`. Before pywbem 0.14.5, the version of `ply`
    module that was used to build the pywbem distribution archive needed to be
    compatible with the version of `ply` installed in the Python environment,
    otherwise `ply` attempted to re-generate these parse table files in the
    `pywbem` installation directory. Thus, if the `pywbem` installation
    directory is in the system Python, a normal user will typically encounter
    a permission denied error.

    If the installed version of `pywbem` is 0.14.5 or higher, it has tolerance
    against mismatches between these `ply` versions, by having `ply`
    re-generate the parsing tables in memory if needed, but no longer writing
    them out to the pywbem installation directory.
    """

    test_installed = os.getenv('TEST_INSTALLED')

    pywbem = import_installed('pywbem')

    try:
        # pylint: disable=import-outside-toplevel
        from pywbem import _mofparsetab, _moflextab
    except ImportError:
        if test_installed:
            # The _mofparsetab and _moflextab files should not be auto-generated
            # in this case.
            pytest.fail("Cannot run this MOF testcase against an installed "
                        "pywbem (version {0}, installed at {1}) "
                        "because that installation does not contain the "
                        "_mofparsetab.py or _moflextab.py files".
                        format(pywbem.__version__, pywbem.__file__))
        else:
            # The _mofparsetab and _moflextab files will be auto-generated.
            return

    pywbem_not_tolerant = parse_version(pywbem.__version__) <= \
        parse_version('0.14.4')  # This causes 0.14.5.devN to be tolerant

    # pylint: disable=protected-access
    mofparsetab_version = _mofparsetab._tabversion
    moflextab_version = _moflextab._tabversion
    # pylint: enable=protected-access

    mofparsetab_mismatch = parse_version(mofparsetab_version) != \
        parse_version(yacc.__tabversion__)
    moflextab_mismatch = parse_version(moflextab_version) != \
        parse_version(lex.__tabversion__)

    if test_installed and pywbem_not_tolerant and \
            (mofparsetab_mismatch or moflextab_mismatch):
        pytest.skip("Cannot run this MOF testcase against an installed "
                    "pywbem (version {0}, installed at {1}) because that "
                    "pywbem version does not tolerate table version mismatches "
                    "between the current ply package and the generated pywbem "
                    "mof*tab files: yacc table version: current ply: {2}, "
                    "_mofparsetab.py: {3}, lex table version: current ply: "
                    "{4}, _moflextab.py: {5}".
                    format(pywbem.__version__, pywbem.__file__,
                           yacc.__tabversion__, mofparsetab_version,
                           lex.__tabversion__, moflextab_version))


def import_installed(module_name):
    """
    Import a Python module/package, controlling whether it is loaded from the
    normal Python module search path, or from an installed version (excluding
    the module in the current directory).

    The TEST_INSTALLED environment variable controls this as follows:

      * If not set or empty, the normal Python module search path is used.
        Because that search path contains the current directory in front of the
        list, this will cause a module directory in the current directory to
        have precedence over any installed versions of the module.

      * If non-empty, the current directory is removed from the Python module
        search path, and an installed version of the module is thus used, even
        when a module directory exists in the current directory. This can be
        used for testing an OS-installed version of the module.

    Example usage, e.g. in a pywbem test program::

        from ...utils import import_installed
        pywbem = import_installed('pywbem')  # pylint: disable=invalid-name
        from pywbem import ...

    The number of dots in `from ..utils` depends on where the test program
    containing this code is located, relative to the tests/utils.py file.
    """
    test_installed = os.getenv('TEST_INSTALLED')
    if test_installed:

        # Remove '' directory.
        dirpath = ''
        try:
            ix = sys.path.index(dirpath)
        except ValueError:
            ix = None
        if ix is not None:
            if test_installed == 'DEBUG':
                print("Debug: Removing {0} at index {1} from module search "
                      "path".format(dirpath, ix))
            del sys.path[ix]

        # Move CWD to end. Reason is that when testing with an editable
        # installation, the CWD is needed, but when testing with a non-editable
        # installation, the package should not be found inthe CWD.
        # Note that somehow the CWD gets inserted at the begin of the search
        # path every time, so we need a loop.
        dirpath = os.getcwd()
        while True:
            try:
                ix = sys.path.index(dirpath)
            except ValueError:
                if test_installed == 'DEBUG':
                    print("Debug: Appending {0} to end of module search "
                          "path".format(dirpath))
                sys.path.append(dirpath)
                break
            if ix == len(sys.path) - 1:
                # it exists once at the end
                break
            if test_installed == 'DEBUG':
                print("Debug: Removing {0} at index {1} from module search "
                      "path".format(dirpath, ix))
            del sys.path[ix]

    if module_name not in sys.modules:
        module = __import__(module_name, level=0)  # only absolute imports
        if test_installed == 'DEBUG':
            print("Debug: {0} module newly loaded from: {1}".
                  format(module_name, module.__file__))
    else:
        module = sys.modules[module_name]
        if test_installed == 'DEBUG':
            print("Debug: {0} module was already loaded from: {1}".
                  format(module_name, module.__file__))
    return module


def is_inherited_from(member_name, derived_class, base_class):
    """
    Return whether the specified member of a derived class was inherited from
    a base class without being overwritten in between.

    This can be used in situations where a derived class is used to test the
    (inherited) members of an abstract base class, to assert that the member
    that is used in the test is actually the inherited base class member.

    The member can be any of:

    * an instance method,
    * a static method (i.e. a method decorated with @staticmethod),
    * a property (i.e. a getter method decorated with @property).

    Data attributes are not supported at this point.

    Note that the base class may have inherited the member from a further base
    class; but that is irrelevant for this check.

    If the derived class or base class does not expose a member with the
    specified name, AttributeError is raised.
    If the type of member is not supported, TypeError is raised.

    Parameters:

      member_name (string): The name of the class member to be checked.

      derived_class (class): The derived class to be used for the check.

      base_class (class): The base class to be used for the check.

    Returns:

      bool: Boolean indicating whether the derived class member was inherited
        from the base class.
    """

    assert isinstance(member_name, six.string_types)
    assert isinstance(base_class, type)
    assert isinstance(derived_class, type)

    derived_member = getattr(derived_class, member_name)
    base_member = getattr(base_class, member_name)

    if derived_member.__class__.__name__ == 'cython_function_or_method' and \
            base_member.__class__.__name__ == 'cython_function_or_method':
        derived_code = derived_member.func_code
        base_code = base_member.func_code
    elif isinstance(derived_member, types.MethodType) and \
            isinstance(base_member, types.MethodType):
        # instance method
        derived_code = derived_member.__func__.__code__
        base_code = base_member.__func__.__code__
    elif isinstance(derived_member, types.FunctionType) and \
            isinstance(base_member, types.FunctionType):
        # static method
        derived_code = derived_member.__code__
        base_code = base_member.__code__
    elif isinstance(derived_member, property) and \
            isinstance(base_member, property):
        # property
        derived_code = derived_member.fget.__code__
        base_code = base_member.fget.__code__
    else:
        raise TypeError(
            "The type of class member {} is not an instance method, static "
            "method, or a property, but is {} in derived class {} and {} in "
            "base class {}".
            format(member_name, type(derived_member), derived_class.__name__,
                   type(base_member), base_class.__name__))

    return derived_code.co_filename == base_code.co_filename and \
        derived_code.co_firstlineno == base_code.co_firstlineno


def post_bsl(url, headers, data, timeout=4):
    """
    Post to a URL using the 'requests' package, and retry once in case of the
    BadStatusLine exception.

    Retrying in case of the BadStatusLine exception works around Python issue
    https://bugs.python.org/issue43912 (originally pywbem issue #2659). Once
    that issue is solved, the retry is no longer needed.

    Raises:
      requests.exceptions.RequestException - all errors besides a single
        occurrence of the BadStatusLine exception.
    """
    # TODO: Check resolution of Python issue 43912 and remove workaround here
    debug = True
    try:
        response = requests.post(
            url, headers=headers, data=data, timeout=timeout)
    except requests.exceptions.ConnectionError as exc:
        org_exc = exc.args[0]  # pylint: disable=no-member
        if debug:
            print("Debug: ConnectionError: args[0]={!r}".format(org_exc))
        if isinstance(org_exc, urllib3.exceptions.ProtocolError):
            org_org_exc = org_exc.args[1]  # pylint: disable=no-member
            if debug:
                print("Debug: ProtocolError: args[1]={!r}".format(org_org_exc))
            if isinstance(org_org_exc, BadStatusLine):
                # We do just one retry.
                if debug:
                    print("Debug: BadStatusLine: Retrying")
                response = requests.post(
                    url, headers=headers, data=data, timeout=timeout)
            else:
                raise
        else:
            raise
    return response
