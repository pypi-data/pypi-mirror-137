from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='lucapackage',
  version='0.0.1',
  description='A very basic Python Package',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Luca Mezger',
  author_email='lucamezger88@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='python' "package", 
  packages=find_packages(),
  install_requires=[''] 
)