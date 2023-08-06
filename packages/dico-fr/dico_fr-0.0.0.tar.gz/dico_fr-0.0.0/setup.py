from distutils.core import setup
setup(
  name = 'dico_fr',         # How you named your package folder (MyLib)
  packages = ['dico_fr'],   # Chose the same as "name"
  version = '',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Dictionnaire français',   # Give a short description about your library
  author = 'BicodeCosmique',                   # Type in your name
  author_email = 'gabriel.merville@franklinparis.com',      # Type in your E-Mail
  keywords = ['Dictionnaire', 'Français', 'BICORNE'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  python_requires=">=3.6",
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license

  ],
)
