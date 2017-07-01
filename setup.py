from setuptools import setup, find_packages

setup(
    name="vittlify_cli",

    version="0.1",

    description="CLI interface to Vittlify",
    long_description="For a detailed description, see https://github.com/kyokley/vittlify-cli.",

    url="https://github.com/kyokley/vittlify-cli",

    author="Kevin Yokley",
    author_email="kyokley2@gmail.com",

    license="MIT",

    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],

    packages=find_packages(),

    install_requires=[
        'requests',
        'terminaltables',
        'cryptography',
        'colorclass',
    ],
    test_suite='nose.collector',
    tests_require=['nose',
                   'mock',
                   ],

    entry_points={
        "console_scripts": [
            "vt = vt.vt:main",
        ],
    },
)
