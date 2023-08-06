from setuptools import setup,find_packages
setup(
    name='figcow',
    version='1.0.3',
    description='Python cowsay that looks like a figlet',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/donno2048/figcow',
    packages=find_packages(),
    license='MIT',
    author='Elisha Hollander',
    classifiers=['Programming Language :: Python :: 3'],
    entry_points={ 'console_scripts': [ 'figcow=figcow.__main__:main' ] }
)
