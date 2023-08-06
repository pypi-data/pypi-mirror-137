from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

import tree_sitter_python_language

print(tree_sitter_python_language.__file__)


class PostDevelopCommand(develop):
    def run(self):
        super().run()
        tree_sitter_python_language.fetch_and_build_python_language()


class PostInstallCommand(install):
    def run(self):
        super().run()
        tree_sitter_python_language.fetch_and_build_python_language()


setup(
    name="tree-sitter-python-language",
    version="0.0.4",
    packages=find_packages(),
    include_package_data=True,
    requires=["tree_sitter"],
    install_requires=["requests", "tree_sitter"],
    setup_requires=["requests", "tree_sitter"],
    cmdclass={
        "develop": PostDevelopCommand,
        "install": PostInstallCommand,
    },
)
