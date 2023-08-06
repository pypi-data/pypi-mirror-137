from setuptools import setup
from simple_file_user import __version__, read
import os

script_folder = os.path.dirname(__file__)

setup(name = 'simple_file_user',
      version = __version__,
      description = 'Package for easy working with files.',
      packages = ['simple_file_user'],
      author_email = 'internetstalcker@yandex.ru',
      include_package_data = True,
      zip_safe = False,
      long_description = read(os.path.join(script_folder, "README.html")),
      long_description_content_type = 'text/markdown',
      project_urls = {"Homepage": "https://github.com/InternetStalker/Simple_file_user"},
      keywords = 'files file',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ],
      license = 'MIT')
