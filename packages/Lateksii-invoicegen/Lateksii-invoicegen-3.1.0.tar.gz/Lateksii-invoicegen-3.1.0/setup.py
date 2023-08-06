from setuptools import setup, find_packages

setup(
    name='Lateksii-invoicegen',
    version='3.1.0',
    packages = find_packages(),
    package_data = {"Templates":["*.tex"],"Templates":["*.png"]},
    author='antto',
    install_requires=["PySimpleGUI","pdflatex","tk"," importlib_resources ; python_version<'3.7'"],)