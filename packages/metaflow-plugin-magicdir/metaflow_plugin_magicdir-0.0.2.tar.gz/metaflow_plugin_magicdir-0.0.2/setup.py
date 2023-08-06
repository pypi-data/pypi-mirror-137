from setuptools import setup, find_namespace_packages

def get_long_description() -> str:
    with open("README.md") as fh:
        return fh.read()

setup(
    name='metaflow_plugin_magicdir',
    version='0.0.2',
    description='Pass directories between metaflow steps.',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author='Hamel Husain',
    author_email='hamel.husain@gmail.com',
    license='Apache Software License',
    packages=find_namespace_packages(include=['metaflow_extensions.*']),
    py_modules=[
        "metaflow_extensions",
    ],
    install_requires=["metaflow>=2.5.0"],
)

