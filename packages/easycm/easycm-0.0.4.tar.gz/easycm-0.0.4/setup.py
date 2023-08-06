import setuptools

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='easycm',
    version='0.0.4',
    author='Victor Henrique Alves Ribeiro',
    description='A simple python package to plot confusion matrices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['easycm'],
    license='BSD-3',
    url='https://github.com/vhrique/easycm',
    project_urls={
        'Source': 'https://github.com/vhrique/easycm',
        'Tracker': 'https://github.com/vhrique/easycm/issues',
    }
)
