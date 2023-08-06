from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='IDEPyAMS',
    version='0.0.4.3',
    description='PyAMS: Python for Analog and Mixed Signals',
    author= 'd.fathi',
    url = 'https://pyams.org',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['','symbols','symbols.basic','symbols.source','symbols.semiconductor','symbols.multimeter','demo.Kirchhoff','demo.Oscillations'],
    keywords=['Creating new symbols ', 'CAD System', 'Simulation circuit','PyAMS'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    py_modules=['IDEPyAMS','SymbolEditor'],
    package_dir={'':'src','symbols':'src/symbols','symbols.basic':'src/symbols/basic','symbols.source':'src/symbols/source',
                 'symbols.semiconductor':'src/symbols/semiconductor','symbols.multimeter':'src/symbols/multimeter',
                 'demo.Kirchhoff':'src/demo/Kirchhoff',
                 'demo.Oscillations':'src/demo/Oscillations'},
    install_requires = [
        'PyQt5',
        'PyQtWebEngine'
    ],
    package_data={'symbols.basic': ['*'],'symbols.source': ['*'],'symbols.semiconductor': ['*'],'symbols.multimeter': ['*'],'demo.Kirchhoff': ['*'],'demo.Oscillations': ['*']},
    include_package_data=True
)

