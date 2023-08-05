from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='MetaDR',  # 包名
      version='3.0.0',  # 版本号
      description='MetaDR package',
      long_description=long_description,
      author='CHEN Xingjian',
      author_email='xingjchen3-c@my.cityu.edu.hk',
      url='https://github.com/Microbiods/MetaDR',
      install_requires=[
                        'xlrd==1.2.0',
                        'scipy==1.7.1',
                        'pandas==1.3.2',
                        'numpy==1.19.5',
                        'ete3==3.1.2',
                        'tensorflow==2.7.0',
                        'scikit_learn==0.24.2'
      ],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )