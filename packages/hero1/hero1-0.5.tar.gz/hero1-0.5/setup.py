from distutils.core import setup
setup(
  name = 'hero1',
  packages = ['hero1'],
  version = '0.5',
  license='MIT',
  description = 'Hero',
  author = 'Hoewon Kim',
  author_email = 'hoewon.kim@gmail.com',
  url = 'https://github.com/danielhwkim/Hero1',
  download_url = 'https://github.com/danielhwkim/Hero1/archive/refs/tags/v_0_5.tar.gz',
  keywords = ['hero1'],
  install_requires=[
          'zeroconf'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
