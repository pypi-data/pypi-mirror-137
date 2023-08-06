import setuptools

# setup the package
setuptools.setup(
    name="artipy",
    version="1.0.6",
    author="daniel tal",
    author_email="daniel@dtsoft.co.il",
    requires=["setuptools"],
    install_requires=["cython"],
    description="lib for adding artifact creation setup options",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: MIT",
        "Operating System :: OS Independent",
    ],
)
