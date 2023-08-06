from setuptools import setup, find_packages

setup(
    name='Lateksii-invoicegen',
    version='3.1.2',
    packages = find_packages(),
    packege_dir = {"":"InvoiceGen"},
    author='antto',
    include_package_data = True,
    install_requires=["PySimpleGUI","pdflatex","tk"," importlib_resources ; python_version<'3.7'"],)