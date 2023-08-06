from setuptools import setup


def readme() -> str:
    """Long description."""
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


setup(
    # Name of your project. When you publish this
    # package to PyPI, this name will be registered for you
    name="bargets",  # Required

    # Version?
    version="0.1.0a0",  # Required

    # What does your project do?
    description="Tiny arsenal of widgets for statusbars",  # Optional

    # Longer description, that users will see when
    # they visit your project at PyPI
    #long_description=readme(),  # Optional

    # Denotes that long description is in Markdown;
    # valid values are: text/plain, text/x-rst, text/markdown.
    # Optional if 'long_description' is written in rst, otherwise
    # required (for plain-text and Markdown)
    long_description_content_type="text/markdown",  # Optional

    # Who owns this project?
    author="Niklas Larsson",  # Optional

    # Project owner's email
    #author_email="",  # Optional

    # More info at: https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature this project is? Common values are:
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",

        # Who your project is intended for?
        # More info at: https://pypi.org/classifiers/
        "Intended Audience :: End Users/Desktop",

        # License?
        # More info at: https://pypi.org/classifiers/
        "License :: OSI Approved :: MIT License",

        # Python versions? These aren't checked by 'pip install'
        # More info at: https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",

    ],

    # What does your project relate to?
    #keywords="",  # Optional

    # Does your project consist of only one or few python files?
    # If that's the case, use this.
    #py_modules=[""],  # Required

    # Is your project larger than just few files?
    # If that's the case, use this instead of 'py_modules'.
    packages=["bargets"],  # Required

    # Which Python versions are supported?
    # e.g. 'pip install' will check this and refuse to install
    # the project if the version doesn't match
    #python_requires=">=3.8",  # Optional

    # Any dependencies?
    #install_requires=[],  # Optional

    # Need to install, for example, man-pages that your project has?
    #data_files=[("man/man1", ["docs/bargets.1"])],  # Optional

    # Any executable scripts?
    # For example, the following would provide a command
    # called 'bargets' which executes the function 'main' from
    # file 'main' from package 'bargets', when invoked:
    entry_points={  # Optional
        "console_scripts": [
            "bargets-cpu=bargets.cpu:main",
            "bargets-battery=bargets.battery:main",
        ]
    },

    # More info at: https://setuptools.pypa.io/en/latest/userguide/datafiles.html
    include_package_data=True,  # Optional

    # More info at: https://setuptools.pypa.io/en/latest/userguide/miscellaneous.html
    zip_safe=False,  # Optional

    # Additional URLs that are relevant to your project
    project_urls={  # Optional
        #"Bug Reports": "https://github.com...",
        #"Source": "https://github.com..."
    }
)
