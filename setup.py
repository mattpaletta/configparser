import inspect
import os
import subprocess
import sys
from distutils.command.build import build
from setuptools.command.install import install

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup

    ez_setup.use_setuptools()
    from setuptools import setup, find_packages


class BuildCommand(build):
    def run(self):
        build.run(self)


class InstallCommand(install):
    def run(self):
        if not self._called_from_setup(inspect.currentframe()):
            # Run in backward-compatibility mode to support bdist_* commands.
            install.run(self)
        else:
            install.do_egg_install(self)  # OR: install.do_egg_install(self)


setup(
        name = "config_parser",
        version = "0.0.1",
        url = 'https://github.com/mattpaletta/configparser',
        packages = find_packages(),
        include_package_data = True,
        install_requires = ["PyYAML==3.13"],
        author = "Matthew Paletta",
        author_email = "mattpaletta@gmail.com",
        description = "Configuration library wrappers",
        license = "BSD",
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Communications',
        ],
        cmdclass = {
            'build'  : BuildCommand,
            'install': InstallCommand,
        },
)
