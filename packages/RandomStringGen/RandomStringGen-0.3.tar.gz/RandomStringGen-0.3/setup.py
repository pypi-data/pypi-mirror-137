from distutils.core import setup
setup(
  name = 'RandomStringGen',         # How you named your package folder (MyLib)
  packages = ['RandomStringGen'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Tool to generate strings',   # Give a short description about your library
  author = 'itskekoff',                   # Type in your name
  author_email = 'itskekoff@gmail.com',      # Type in your E-Mail
  url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',   # Provide either the link to your github or to your website
  download_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',    # I explain this later on
  keywords = ['Generator', 'String', 'KeyGen'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'discord_webhook'
      ],
  classifiers=[
    'Programming Language :: Python :: 3.10',
  ],
)