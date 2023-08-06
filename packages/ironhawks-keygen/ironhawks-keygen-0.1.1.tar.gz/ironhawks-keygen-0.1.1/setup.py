from setuptools  import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description_text = (this_directory / "README.md").read_text()

setup(
  name = 'ironhawks-keygen',
  packages = ['ironhawkskeygen'],
  version = '0.1.1',
  license='MIT',
  description = 'Effortlessly generate random passwords of custom lengths.',
  long_description_content_type = "text/markdown",
  long_description  = long_description_text,
  author = 'Praveen K',
  author_email = 'hartbrkrlegacy@gmail.com',
  url = 'https://github.com/hartbrkr3399/ironhawks-keygen',
  download_url = 'https://github.com/hartbrkr3399/ironhawks-keygen/archive/' + 
                 'refs/tags/v0.1.1.tar.gz',
  keywords = ['password', 'keygen', 'random'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)