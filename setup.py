from setuptools import setup, find_packages


setup(
    name='wello',
    url='https://github.com/Vayel/wello',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SocketIO',
        'pyserial',
        'signalslot',
        'SQLAlchemy',
        'SQLAlchemy-Defaults',
        'SQLAlchemy-Utils',
        'Twisted',
        'WTForms',
        'WTForms-Alchemy',
    ],
)
