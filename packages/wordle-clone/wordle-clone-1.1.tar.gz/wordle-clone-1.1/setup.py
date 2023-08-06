from distutils.core import setup
setup(
  name = 'wordle-clone',         
  packages = ['wordle-clone'],   
  version = '1.1',
  license='MIT',
  description = 'Simple Wordle clone',
  author = 'Alan Koterba',
  author_email = 'alankoterba12321@gmail.com',
  url = 'https://github.com/alannxq/wordle-clone',
  download_url = 'https://github.com/alannxq/wordle-clone/archive/refs/tags/v1.1.tar.gz',    # I explain this later on
  keywords = ['Wordle', 'game', 'color'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
