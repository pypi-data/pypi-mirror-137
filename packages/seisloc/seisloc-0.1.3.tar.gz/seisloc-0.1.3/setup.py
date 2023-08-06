from setuptools import setup,find_packages

with open("README.md",'r') as fh:
    long_description = fh.read()

setup(
    name="seisloc",
    author="Hardy ZI",
    version="0.1.3",
    author_email='zijinping@hotmail.com',
    description = 'Tool package for earthquake location',
    long_description = long_description,
    license = "MIT",
    packages = find_packages(),
    install_requires=[
    'obspy',
    'tqdm==4.48.0',
    'jupyter',
    'scipy>=1.4.1',
    'numpy==1.21.0',
    'numba',
    'pandas',
    'pillow'
    'seisloc'
    ],
    python_requires = "==3.7",
    setup_requires=['numpy==1.21.0']
)
