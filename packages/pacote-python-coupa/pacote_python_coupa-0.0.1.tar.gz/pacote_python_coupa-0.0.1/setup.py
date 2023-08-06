from setuptools import setup

setup(name='pacote_python_coupa',
    version='0.0.1',
    license='MIT License',
    author='Danilo Oliveira',
    author_email='danilo.o.r.santos@gmail.com',
    keywords='Pacote',
    description=u'Meu exemplo de pacote PyPI',
    packages=['pacote_python_coupa'],
    install_requires=['numpy', 'pandas', 'PySimpleGUI', 'scalpl', 'humanfriendly', 'requests'],)