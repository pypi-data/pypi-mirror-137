from setuptools import setup, find_packages
from src.converter.settings import VERSION

setup(
    name='JPET-format-converter',
    version=VERSION,
    author='Mateusz Kruk, Rafał Masalek',
    description='This is a interfile to dicom converter created by Mateusz Kruk and Rafal Maselek.',
    long_description='file: README.md',
    long_description_content_type= 'text/markdown',
    url = 'https://github.com/JPETTomography/j-pet-format-converter',
    packages=find_packages(),
    install_requires=["setuptools>=42",
                      "wheel",
                      "numpy",
                      "pyDicom",
                      "pylint",
                      "python-coveralls"],
    keywords=['JPET','interfile','dicom','format','converter'],
    classifiers =[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent']
)
