from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: End Users/Desktop',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: Apache Software License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='zikasort',
  version='0.0.7',
  description='Sorter for files.',
  py_modules=["command_line"],
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  entry_points = {
      'console_scripts': ['zikasort=command_line:main'],
  },  
  url='',  
  author='Zika Walter',
  author_email='example@example.com',
  license='APACHE', 
  classifiers=classifiers,
  keywords='sorter', 
  packages=find_packages(),
  install_requires=['']  
)
