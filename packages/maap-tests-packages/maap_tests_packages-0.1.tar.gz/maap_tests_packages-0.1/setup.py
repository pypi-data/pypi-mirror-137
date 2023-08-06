from setuptools import setup, find_packages


setup(
    name='maap_tests_packages',
    version='0.1',
    license='MIT',
    author="Harisha G N",
    author_email='hagn0001@synchronoss.com',
    packages=find_packages('main'),
    package_dir={'': 'main'},
    url='https://stash.synchronoss.net/projects/CCMIMAAP/repos/ccmi-maap-qa-automation/browse',
    keywords='sample setuptools development',
    install_requires=[
          'scikit-learn',
      ],

)