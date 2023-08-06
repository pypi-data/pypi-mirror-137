from pathlib import Path
from setuptools import setup, find_packages

#The directory containing this file
HERE = Path(__file__).parent

#The text of the README file
README = (HERE/ "README.md").read_text()

#The text of the instal requirements
def list_reqs(fname='requirements.txcdt'):
    with open(fname) as fd:
        return fd.read().splitlines()

INSTALL_REQUIRES = list_reqs(fname='requirements.txt')

#meta-data
setup(
    name='cfg2qr',
    version='0.1.8',
    license='MIT',
    author="Kristina",
    description = "Small personal project to learn about Python packaging.",
    long_description=README,
    long_description_content_type='text/markdown',
    # author_email='email@example.com',
    # package_dir={"": "cfg2qr"},
    packages=find_packages(),
    url='https://github.com/kristin54/qr-code',
    keywords='qr-code project',
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': ['cfg2qr=cfg2qr.main:main'],
    },
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only'
    ]

)

# #Laurent Boucaud
# entry_points={
#         'console_scripts': ['qr2png=qr2png.main:main'],
#     }