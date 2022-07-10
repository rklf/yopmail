from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='yopmail',
    version='0.5',
    description="A Python module to get mails from a Yopmail inbox, save them",
    long_description=long_description,
    long_description_content_type='text/markdown',
    readme = "README.md",
    license='MIT',
    author="rklf",
    py_modules=["ym"],
    python_requires='>=3.8',
    url='https://github.com/rklf/yopmail',
    keywords='yopmail get mails retrieve scrap emails',
    install_requires=[
          'bs4',
          'requests',
      ],

)