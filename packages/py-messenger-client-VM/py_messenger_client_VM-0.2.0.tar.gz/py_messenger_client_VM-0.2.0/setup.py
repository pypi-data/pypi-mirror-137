from setuptools import setup, find_packages

setup(
    name='py_messenger_client_VM',
    version='0.2.0',
    description='Mess Client',
    author='Vikulov M',
    author_email='vikulov.1991@mail.ru',
    packages=find_packages(),
    install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
)
