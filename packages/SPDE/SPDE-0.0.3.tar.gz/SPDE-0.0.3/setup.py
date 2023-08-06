from distutils.core import setup,Extension
from Cython.Build import cythonize

sourcefiles = ['src/spde.pyx', 'src/TurboOptimizer.cpp']

extensions = [Extension("SPDE", sourcefiles,language='c++')]


setup(name="SPDE",
	  version="0.0.3",
		author = 'Nicolas Desassis and Didier Renard',
		author_email = 'nicolas.desassis@gmail.com',
		url = 'https://github.com/NDesassis/spde', 
    ext_modules = cythonize(extensions)
)

