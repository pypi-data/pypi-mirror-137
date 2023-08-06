from setuptools import setup, find_packages


git_repo = "https://github.com/sliatecinos/br_registrations"

classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

with open('README.rst') as _readme_file:
    readme = _readme_file.read()

setup(
    name='br_registrations',  # Required
    url=git_repo,   # Optional
    version='0.0.0.6',  # Required
    author='Sliatecinos',   # Optional
    author_email='sliatecinos@hotmail.com',   # Optional
    packages=find_packages(),
    license='MIT',
    description=(
        "A simple Python library containing functions that check Brazilian documents values"
    ),
    long_description=readme,
    classifiers=classifiers,
    keywords="cpf,cnpj,br,brazil,brasil,validate",  # Optional
    install_requires=[''] 
)
