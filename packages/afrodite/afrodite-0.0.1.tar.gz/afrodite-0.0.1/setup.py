from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='afrodite',
    version='0.0.1',
    url='https://github.com/adsmaicon',
    license='MIT License',
    author='Maicon Carvalho',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='caiocarneloz@gmail.com',
    keywords='Pacote',
    description=u'Exemplo de pacote PyPI',
    packages=['afrodite'],
    install_requires=['numpy'],)