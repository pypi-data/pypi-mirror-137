from distutils.core import setup
setup(
  name = 'catalystengine',
  packages = ['catalystengine'],
  version = '0.5.3',
  license='MIT',
  description = 'Terminal based game engine',
  author = 'Azearia',
  author_email = 'azearia5@gmail.com',
  url = 'https://github.com/Azearia/catalystengine',
  download_url = 'https://github.com/Azearia/catalystengine/archive/refs/tags/0.5.3.tar.gz',
  keywords = ['GAMEENGINE', 'TERMINAL'],
  install_requires=[
          'audioplayer',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)