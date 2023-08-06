from distutils.core import setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, r'README'), encoding='utf-8') as f:
    readme_text = f.read()

# setup function
setup(
    name = 'lppinv',
    packages = ['lppinv'],
    version = '0.3.8',
    license = 'MIT',
    description = '"Hybrid" LS-LP model pseudoinverse-based (SVD-based) solving algorithm',
    long_description=readme_text,
    author = 'econcz',
    author_email = '29724411+econcz@users.noreply.github.com',
    url = 'https://github.com/econcz/lppinv',
    download_url = 'https://github.com/econcz/lppinv/archive/pypi-0_3_8.tar.gz',
    keywords = [
        'least squares', 'linear programming', 'pseudoinverse', 'singular value decomposition',
        'constrained OLS', 'relationship matrix', 'custom',
        'numpy', 'mathematics'
    ],
    install_requires = ['numpy'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
  ],
)