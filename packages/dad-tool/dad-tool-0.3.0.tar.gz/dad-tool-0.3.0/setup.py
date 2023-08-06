import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

DEV_REQUIREMENTS = [
    'black',
    'coveralls == 3.*',
    'flake8',
    'isort',
    'mypy',
    'pytest == 7.*',
    'pytest-cov == 3.*',
    'types-setuptools',
]

setuptools.setup(
    name='dad-tool',
    version='0.3.0',
    description='Dummy Address Data (DAD) - Real addresses from all around the world.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/Justintime50/dad-python',
    author='Justintime50',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    extras_require={
        'dev': DEV_REQUIREMENTS,
    },
    package_data={
        'dad_tool': [
            'dad/src/addresses/**/*.json',
            'dad/src/other/**/*.json',
            'py.typed',
        ],
    },
    python_requires='>=3.7, <4',
)
