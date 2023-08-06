from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pdtoolbox',
    version='0.0.1',
    author='Pete Davies',
    author_email='pedrostanton@gmail.com',
    description='Initial setup and installation of package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/pedrostanton/toolbox',
    project_urls={
        "Bug Tracker": "https://github.com/pedrostanton/toolbox/issues"
    },
    license='MIT',
    packages=find_packages(),
    install_requires=['cbpro', 'pika'],
)