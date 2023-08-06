from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='datablender',
    version='0.1',
    description='Data Blender makes it easy to import and manage data through a database.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ARTM-dev/datablender.git',
    author='ARTM-dev',
    license='Apache 2.0',
    packages=find_packages(),
    zip_safe=False,
    test_suite="tests",
    install_requires =[
        'pandas',
        'unidecode',
        'sqlalchemy',
        'psycopg2',
        'pyodbc',
        'numpy'
    ]
)