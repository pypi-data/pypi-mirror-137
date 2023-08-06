from setuptools import setup


def readme_file_contents():
    with open('README.rst') as readme_file:
        data = readme_file.read()
    return data


setup(
    name='cyberpot',
    version='1.0.0',
    description='Simple TCP honeypot',
    long_description=readme_file_contents(),
    packages=['cyberpot'],
    zip_safe=False,
    install_requires=[]
)