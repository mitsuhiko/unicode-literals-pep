from distutils.core import setup
from unicode_unprefix.installhook import build_py_strip_unicode

setup(
    py_modules=['unicodetest'],
    cmdclass={'build_py': build_py_strip_unicode}
)
