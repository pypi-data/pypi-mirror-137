"""
Locate ArcPy and add it to the path
Created on 13 Feb 2015
@author: Jamesramm

Avoid using fstrings as code needs to be able to run using python27 and 3
"""
import os
import sys
import struct
import inspect
import logging
import pkgutil

try:
    import importlib.util  # noqa: F401 see comment below re: why this is here
except ImportError:
    import importlib
"""
importlib.util: is not used by this lib, but rather downstream by:
<pro install dir>\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\lib\site-packages\arcgisscripting\__init__.py # noqa: E501

The syntax for using import.util (line 96 from file above) requires the import
of 'importlib.util'.  The init above ^^^ doesn't do that, it only imports
importlib.  Suspect that when using a conda env anther module is likely
importing importlib.util, and therefor when the code above is executed the
importlib.util namespace has already been populated.  When run with a non
conda env an error occurs.
"""

try:
    import _winreg
except ImportError:
    import winreg as _winreg

LOGGER = logging.getLogger(__name__)


def get_python_bitness():
    """Return bit size of active python interpreter (ie. 32, 64)"""
    bitness = struct.calcsize("P") * 8
    LOGGER.debug("bit: {0}".format(bitness))
    return bitness


def get_installed_arc_bitness(pro=False):
    """Return 32 or 64 bit nature of ArGIS binaries."""
    # Pro is always 64bit
    if pro:
        return [64]
    install_dir = locate_arcgis()
    LOGGER.debug(install_dir)
    supportedBits = []
    if os.path.exists(os.path.join(install_dir, "bin64")):
        supportedBits.append(64)
    if os.path.exists(os.path.join(install_dir, "bin")):
        supportedBits.append(32)
    return supportedBits


def verify_bit_match(pro=False):
    """Return true if python interpreter and ArcGIS bitness match each other"""
    pybits = get_python_bitness()
    arcbits = get_installed_arc_bitness(pro)
    LOGGER.debug("pybits: arcbits - {0} : {1}".format(pybits, arcbits))
    #match = pybits == arcbits
    if pybits not in arcbits:
        msg = '*** Error: python and arcgis 32/64bit mismatch: Py: ' + \
              "{0}, Arc:{1}".format(pybits, arcbits)
        raise Exception(msg)


def verify_conda_meta_dir():
    """Issue warning if conda-meta folder does not exist

    Arcpy checks folder exists regardless of whether actually using conda.
    (https://github.com/JamesRamm/archook/issues/22#issuecomment-624262435)
    """
    cmeta = os.path.join(sys.exec_prefix, "conda-meta")
    if not os.path.exists(cmeta):
        errStr = 'ImportError("arcpy needs to run within an active ArcGIS ' + \
                 'Conda environment")'
        msg = "unable to find the conda-meta directory, may get error: " + \
              "{0}, expected dir: {1}"
        msg = msg.format(errStr, cmeta)
        LOGGER.warning(msg)


def locate_arcgis(pro=False):
    """
    Find the path to the ArcGIS Desktop installation, or the ArcGIS Pro
    installation

    if `pro` argument is True.

    Keys to check:

    ArcGIS Pro: HKLM/SOFTWARE/ESRI/ArcGISPro 'InstallDir'

    HLKM/SOFTWARE/ESRI/ArcGIS 'RealVersion' - will give the version, then we
    can use that to go to
    HKLM/SOFTWARE/ESRI/DesktopXX.X 'InstallDir'. Where XX.X is the version

    We may need to check HKLM/SOFTWARE/Wow6432Node/ESRI instead
    """
    try:
        if pro:
            pro_key = get_pro_key()
            install_dir = _winreg.QueryValueEx(pro_key, "InstallDir")[0]
            LOGGER.debug("installdir: {0}".format(install_dir))
        else:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                                  r"SOFTWARE\Wow6432Node\ESRI\ArcGIS", 0)
            LOGGER.debug("arckey: {0}".format(key))
            version = _winreg.QueryValueEx(key, "RealVersion")[0][:4]
            LOGGER.debug("version: {0}".format(version))

            key_string = r"SOFTWARE\Wow6432Node\ESRI\Desktop{0}".format(
                         version)
            LOGGER.debug("key_string: {0}".format(key_string))

            desktop_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                                          key_string, 0)
            LOGGER.debug("desktop_key: {0}".format(desktop_key))


            install_dir = _winreg.QueryValueEx(desktop_key, "InstallDir")[0]
            LOGGER.debug("install_dir: {0}".format(install_dir))
        return install_dir
    except WindowsError:
        msg = "Could not locate the ArcGIS directory on this machine"
        raise ImportError(msg)


def get_pro_paths():
    """Return 2 lists, for adding to Windows PATH and python sys.path"""
    P = locate_arcgis(pro=True)
    C = locate_pro_conda()

    LOGGER.debug("propath: {0}".format(P))
    LOGGER.debug("condapath: {0}".format(C))

    # P = r"C:\Program Files\ArcGIS\Pro"
    # C = r"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3"
    PRO_WIN_PATHS = inspect.cleandoc(
        r"""
        {C}
        {C}\Library\mingw-w64
        {C}\Library\usr\bin
        {C}\Library\bin
        {C}\Scripts
        {P}\Python\Scripts
        {P}\bin
        """.format(
            C=C, P=P
        )
    )
    PRO_SYSPATHS = inspect.cleandoc(
        r"""
        {C}
        {C}\python36.zip
        {C}\DLLs
        {C}\lib
        {C}\lib\site-packages
        {P}\bin
        {P}\Resources\ArcPy
        {P}\Resources\ArcToolbox\Scripts
        """.format(
            C=C, P=P
        )
    )
    winpaths = PRO_WIN_PATHS.splitlines()
    syspaths = PRO_SYSPATHS.splitlines()
    return [winpaths, syspaths]


def get_arcpy(pro=False):
    """
    Allows arcpy to imported on 'unmanaged' python installations (i.e. python
    installations arcgis is not aware of).
    Gets the location of arcpy and related libs and adds it to sys.path
    Looks for ArcGIS Pro if `pro` argument is True.
    """
    install_dir = locate_arcgis(pro)

    if pro:
        verify_bit_match(pro)
        verify_conda_meta_dir()
        # pro_conda_dir = locate_pro_conda()

        winpaths, syspaths = get_pro_paths()
        # update Windows PATH
        wp = os.environ["PATH"].split(";")  # save incoming path
        [wp.insert(0, x) for x in winpaths]  # prepend our new syspath
        os.environ["PATH"] = ";".join(wp)  # write back to environment
        # update sys.path
        [sys.path.insert(0, x) for x in syspaths]

    else:
        verify_bit_match()
        arcpy = os.path.join(install_dir, "arcpy")
        # Check we have the arcpy directory.
        if not os.path.exists(arcpy):
            raise ImportError(
                "Could not find arcpy directory in {0}".format(install_dir)
            )

        pybits = get_python_bitness()
        if pybits == 64:
            bin_dir = os.path.join(install_dir, "bin64")
        else:
            bin_dir = os.path.join(install_dir, "bin")

        # Update Python's path
        dirs = ["", arcpy, bin_dir, "ArcToolbox/Scripts"]
        for p in dirs:
            sys.path.insert(0, os.path.join(install_dir, p))

        # check for numpy, and add path to local install if not part of the
        # virtualenv
        # -- only gets executed if python27
        numpyloader = pkgutil.find_loader('numpy')
        LOGGER.debug("numpyloader: {0}".format(numpyloader))
        if not numpyloader:
            pythonPath = os.path.join(sys.base_prefix,
                                  'Lib\site-packages')
            msg = "adding the site-packages from prefix install to try to " + \
                  "resolve the required numpy dependency: {0}".format(
                  pythonPath)
            LOGGER.info(msg)
            sys.path.append(pythonPath)
        numpyloader = pkgutil.find_loader('numpy')
        if not numpyloader:
            msg = 'cannot find numpy and is a dependency for arcpy.  Have ' + \
                  'searched for it in both the base install and the  ' + \
                  'virtualenv if you are using a virtualenv try ' + \
                  "installing numpy 'pip install numpy' to resolve this issue"
            LOGGER.error(msg)
            raise ImportError(msg)



    #E:\sw_nt\Python27\ArcGIS10.8\Lib\site-packages\numpy




def locate_pro_conda():
    """
    Returns the path to the ArcGIS Pro-managed conda environment.
    """
    try:
        pro_key = get_pro_key()
        conda_root = _winreg.QueryValueEx(pro_key, "PythonCondaRoot")[0]
        conda_env = _winreg.QueryValueEx(pro_key, "PythonCondaEnv")[0]
        conda_path = os.path.join(conda_root, "envs", conda_env)
        LOGGER.debug("conda_path: {0}".format(conda_path))
        if not os.path.exists(conda_path):
            msg = "Could not find Conda environment {0} in root directory {1}"
            msg = msg.format(conda_env, conda_root)
            raise ImportError(msg)
        LOGGER.debug("conda_path: {0}".format(conda_path))
        return conda_path
    except WindowsError:
        msg = "Could not locate the Conda directory on this machine"
        raise ImportError(msg)


def get_pro_key():
    """
    Returns ArcGIS Pro's registry key.
    """
    pro_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                              r"SOFTWARE\ESRI\ArcGISPro")
    LOGGER.debug("prokey: {0}".format(pro_key))
    return pro_key
