"""Install arxiv-qa as an importable package."""
from setuptools import setup, find_packages

setup(
    name="arxiv-qa",
    version="0.0.2",
    packages=[f"arxiv.{package}" for package in find_packages("arxiv")],
    zip_safe=False,
    install_requires=["pydantic==1.9.0", "sqlalchemy==1.4.31"],
    include_package_data=True,
)
