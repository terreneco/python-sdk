from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="Terrene",
    version="0.0.4",
    description="Terrene's Python SDK",
    url="https://docs.terrene.co",
    author="Terrene",
    author_email="developers@terrene.co",
    license='MIT',
    keywords="terrene",
    packages=[
        'terrene.apps',
        'terrene.core'
    ],
    install_requires=reqs,
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
