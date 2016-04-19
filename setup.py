import setuptools

setuptools.setup(
    name="pyof",
    version="0.1.0",
    url="https://github.com/jflbr/pyof",

    author="Jeyfel Brandauer",
    author_email="jeyfelbrandauer@gmail.com",

    description="A simple and generic object factory implementation",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
