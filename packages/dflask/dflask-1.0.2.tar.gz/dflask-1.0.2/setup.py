from setuptools import setup, find_packages
setup(
    name='dflask',
    version='1.0.2',
    license='MIT',
    author='Elisha Hollander',
    author_email='just4now666666@gmail.com',
    description="Use responses for Flask directly",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/donno2048/Direct-Flask',
    project_urls={
        'Documentation': 'https://github.com/donno2048/Direct-Flask#readme',
        'Bug Reports': 'https://github.com/donno2048/Direct-Flask/issues',
        'Source Code': 'https://github.com/donno2048/Direct-Flask',
    },
    python_requires='>=3.0',
    packages=find_packages(),
    install_requires=["Flask>=2.0.1"],
    classifiers=['Programming Language :: Python :: 3']
)
