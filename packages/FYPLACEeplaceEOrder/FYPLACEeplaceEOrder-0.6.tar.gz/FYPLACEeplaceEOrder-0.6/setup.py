from setuptools import setup, find_packages


setup(
    name='FYPLACEeplaceEOrder',
    version='0.6',
    license='MIT',
    author="Atmarishi",
    author_email='athmarishi99@gmail.com',
    packages=find_packages('fymojo'),
    package_dir={'': 'fymojo'},
    url='https://github.com/atmarishi/FY',
    keywords='example project',
    install_requires=[
          'requests',
      ]
)