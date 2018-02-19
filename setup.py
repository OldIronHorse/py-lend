from setuptools import setup

setup(
  name='pylend',
  version='0.1',
  description='Loan order book.',
  url='https://github.com/oldironhorse/py-lend',
  download_url='https://github.com/oldironhorse/py-lend/archive/0.1.tar.gz',
  author='Simon Redding',
  author_email='s1m0n.r3dd1ng@gmail.com',
  license='GPL 3.0',
  packages=['pylend'],
  install_requires=[
  ],
  test_suite='nose.collector',
  tests_require=['nose'],
  zip_safe=False)
