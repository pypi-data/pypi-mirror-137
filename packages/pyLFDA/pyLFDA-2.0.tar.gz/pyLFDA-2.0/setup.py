from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'pyLFDA',
  packages = ['pyLFDA'],
  version = '2.0',
  license='MIT',
  description = 'pyLFDA is a tool which allows analysis of pairwise lipid force distribution along with other functions such as curvature and diffusion.',
  author = 'Bhavay Aggarwal',
  author_email = 'bhavayaggarwal07@gmail.com',
  url = 'https://github.com/Chokerino',
  download_url = 'https://github.com/RayLabIIITD/pyLFDA/archive/refs/tags/v_2.0.tar.gz',
  keywords = ['Python', 'Lipidomics', 'Analysis'],
  install_requires=[
          'numpy',
          'matplotlib',
          'MDAnalysis',
          'scipy',
          'membrane_curvature',
      ],
  classifiers=[
    'Development Status :: 4 - Beta', 
    'Intended Audience :: Developers', 
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
  long_description=long_description,
  long_description_content_type='text/markdown'
)