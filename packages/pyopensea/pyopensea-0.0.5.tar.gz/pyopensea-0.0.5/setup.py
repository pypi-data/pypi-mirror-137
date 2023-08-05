from distutils.core import setup
setup(
    name='pyopensea',
    version='0.0.5',
    author='Gavin Newcomer',
    author_email='gjnprivate@gmail.com',
    description='OpenSea Python SDK',
    url='https://github.com/gavinnewcomer/OpenPython',
    download_url='https://github.com/gavinnewcomer/OpenPython/archive/refs/tags/v0.0.5.tar.gz',
    license='MIT',
    packages=['pyopensea'],
    install_requires=[
        'requests'
    ]
)
