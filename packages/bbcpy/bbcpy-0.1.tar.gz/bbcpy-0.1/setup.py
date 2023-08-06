from setuptools import setup

setup(name='bbcpy',
      version='0.1',
      description='A novel Python BCI toolbox',
      url='https://github.com/bbcpy/bbcpy',
      author='Neurotechnology Group TU Berlin',
      author_email='bbcpy@tu-berlin.de',
      license='MIT',
      packages=['bbcpy'],
      install_requires=[
          'scikit-learn','pyriemann'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)