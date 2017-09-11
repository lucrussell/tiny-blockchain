from setuptools import setup, find_packages


setup(
    name='tinyblockchain',
    version='1.0.0',
    description='Blockchain playground',
    author='Luc Russell',
    license='',
    classifiers=[
        'Programming Language :: Python :: 3.4'
    ],
    keywords='',
    packages=find_packages(exclude=['contrib', 'docs', 'spec*']),
    install_requires=[
        'docopt',
        'falcon>=1.0',
        'gunicorn>=19.4.5',
        'requests',
        'pyyaml'
    ],
    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
            'tinyblockchain = tinyblockchain.app:main'
        ],
    },
)
