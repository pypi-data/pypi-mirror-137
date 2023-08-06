import pathlib

from setuptools import find_packages, setup

lib_name = "ce_machine_learning"
with open(f"{lib_name}/requirements.txt") as f:
    required = f.read().splitlines()

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name=lib_name.replace("_", "-"),
    packages=find_packages(exclude=("test*",)),
    include_package_data=True,
    # package_data={"ce_machine_learning": ["*.pyi"]},
    version="0.0.2",
    description="Python client for Machine Learning features of Crédito Express",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Crédito Express",
    author_email="contato@creditoexpress.com.br",
    install_requires=required,
)
