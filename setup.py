from distutils.core import setup
import py2exe
import sys

from glob import glob

sys.path.append("C:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")
data_files = [("Microsoft.VC90.CRT", glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]
setup(
    data_files=data_files,
    console=['patiotiler.py']
  )
  
