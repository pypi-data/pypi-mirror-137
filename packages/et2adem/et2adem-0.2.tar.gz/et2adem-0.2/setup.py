from distutils.core import setup
setup(
  name = 'et2adem',         # How you named your package folder (MyLib)
  packages = ['et2adem'],   # Chose the same as "name"
  package_dir={'et2adem': 'et2adem'},
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A more fun version of tqdm',   # Give a short description about your library
  author = 'Mohamed Abdelhack',                   # Type in your name
  author_email = 'mohamed.abdelhack.37a@kyoto-u.jp',      # Type in your E-Mail
  url = 'https://mabdelhack.github.io/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/mabdelhack/et2adem/archive/refs/tags/v_02.tar.gz',    # I explain this later on
  keywords = ['tqdm', 'fun'],   # Keywords that define your package best
  package_data={'et2adem': ['data/*.wav']},
  data_files = [('', ['et2adem/data/et2adem.wav'])],
  install_requires=[            # I get to this in a second
          'tqdm',
          'playsound==1.2.2',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)