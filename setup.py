try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup

    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name = "config_parser",
        version = "0.0.1",
        url = 'https://github.com/mattpaletta/configs',
        packages = find_packages(),
        include_package_data = True,
        install_requires = ["PyYAML>=4.2b1"],
        author = "Matthew Paletta",
        author_email = "mattpaletta@gmail.com",
        description = "Configuration library wrappers",
        long_description=long_description,
        long_description_content_type="text/markdown",
        python_requires='>=3.6',
        license = "GNU GPLv3",
        classifiers = [
            "Development Status :: 3 - Alpha",
            'Intended Audience :: Developers',
            "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
            'Operating System :: OS Independent',
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries",
            "Natural Language :: English",
        ],
)
