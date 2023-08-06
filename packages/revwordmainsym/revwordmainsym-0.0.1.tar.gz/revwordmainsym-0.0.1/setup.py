from setuptools import setup 

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='revwordmainsym',
	version='0.0.1',
	license='MIT',
	description="A python script that reverse a user's input but keeps any symbol at it's original position after the reverse",
	author="Emmanuel Owusu",
	author_email="emmowu10@gmail.com",
	url = 'https://github.com/coding-rev', 
	package_dir={'':'src'},
	keywords = ['REVERSE', 'STRING', 'MANIPULATION'], 
	classifiers=[
	    'Development Status :: 3 - Alpha',      
	    'Intended Audience :: Developers',      
	    'License :: OSI Approved :: MIT License',   
	    'Programming Language :: Python :: 3',      
	    'Programming Language :: Python :: 3.4',
	    'Programming Language :: Python :: 3.5',
	    'Programming Language :: Python :: 3.6',
  ],
  long_description=long_description,
  long_description_content_type="text/markdown" 
)