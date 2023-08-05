from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pyspeakflow',
  version='0.0.1',
  description='This a very simple speak fucntion packege to make voice assistant etc. ',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Raghav Rajput',
  author_email='pythoncode0101@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='pyttsx3 speak sapi5', 
  packages=find_packages(),
  install_requires=[''] 
)
