from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

from tree_sitter_python_language import fetch_and_build_python_language


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        fetch_and_build_python_language()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        fetch_and_build_python_language()
        
setup(
    name='tree-sitter-python-language',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    requires=['tree_sitter'],
    install_requires=['requests', 'tree_sitter'],
    setup_requires=['requests', 'tree_sitter'],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
