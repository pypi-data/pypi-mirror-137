import setuptools


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('requirements_dev.txt') as f:
    dev_requirements = f.read().splitlines()[1:]

with open('README.md') as f:
    README = f.read()


setuptools.setup(
    name='bisi',
    version='0.0.1',
    description='A Python based runner for docker images.',
    long_description=README,
    python_requires='>=3.6.0',
    packages=setuptools.find_packages(where="src", include='bisi.*'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements
    },
    entry_points={
        'console_scripts': [
            'bisi = bisi.cli.main:cli'
        ]
    }
)
