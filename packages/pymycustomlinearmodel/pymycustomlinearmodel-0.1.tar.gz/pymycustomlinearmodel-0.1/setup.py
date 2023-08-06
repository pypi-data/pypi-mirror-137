from setuptools import setup, find_packages


setup(
    name='pymycustomlinearmodel',
    packages=find_packages(),
    include_package_data=True,
    version='0.1',
    license='MIT',
    description='Simple Linear Regression Model',
    author="Pallavi Saxena",
    author_email='pallavi.as1127@gmail.com',
    #package_dir={'': 'src'},
    #url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords=['EDA'],
    install_requires=[
          'flask',
          'Flask-Cors',
          'matplotlib',
          'numpy',
          'pandas',
          'pandas-profiling',
          'scikit-learn',
          'seaborn',
          'scipy',
          'statsmodels',
      ],
    classifiers=[
       'Development Status :: 3 - Alpha',
    ],
)