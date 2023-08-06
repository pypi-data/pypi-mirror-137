# Copyright (C) 2021 Flowdas Inc. & Dong-gweon Oh <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from setuptools import setup

setup_requires = [
]

install_requires = [
    'importlib_metadata;python_version<"3.8"',
    'typeable',
    'uvicorn',
    'falcon>=3.0.0',
    'sentry-sdk',
]

tests_require = [
    'pytest',
    'pytest-cov',
    'tox',
]

dev_require = tests_require + [
    'sphinx',
]

setup(
    name='flowdas.service',
    version=open('VERSION').read().strip(),
    url='https://github.com/flowdas/flowdas.service',
    project_urls={
        "Code": "https://github.com/flowdas/flowdas.service",
        "Issue tracker": "https://github.com/flowdas/flowdas.service/issues",
    },
    description='Flowdas Service: The OpenRPC Framework',
    long_description=open('README.rst').read(),
    author='Flowdas Inc.',
    author_email='propsero@flowdas.com',
    license='MPL 2.0',
    packages=[
        'flowdas.service',
    ],
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require={
        'dev': dev_require,
    },
    scripts=[],
    entry_points={
        'console_scripts': [
            'f=flowdas.service:Main.main',
        ],
    },
    zip_safe=False,
    python_requires=">=3.7",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
