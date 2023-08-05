from distutils.core import setup

with open('README.md') as read_me:
    long_description = read_me.read()

setup(
  name = 'lettersPoints',
  packages = ['lettersPoints'],
  version = '0.7',
  license = 'MIT',
  description = 'This library can be used to generate points that, when plotted, form letters. The height and spacing can be set.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Jean-Paul Mitra',
  author_email = 'jeanmitra77@gmail.com',
  url = 'https://github.com/MitraMitraMitra/letters-plot',
  download_url = 'https://github.com/MitraMitraMitra/letters-plot/archive/refs/tags/v_05.tar.gz',  
  keywords = ['plotting', 'letters'],
  install_requires = [
           
      ],
  classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)