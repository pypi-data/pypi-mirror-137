from setuptools import setup
from lambdatest_tunnel import __version__

setup(
    name='lambdatest_tunnel',
    version=__version__,
    description='Plugin to start / stop LambdaTest Tunnel for local testing',
    long_description=open('README.txt').read(),
    author='Nigel Uprichard',
    author_email='uprichard@users.noreply.github.com',
    url='https://github.com/uprichard/lambdatest-tunnel-manager',
    packages=['lambdatest_tunnel'],
    python_requires='>=3.6',
    keywords=['testing', 'selenium', 'driver', 'test automation', 'lamdatest'],
    install_requires=[
        'requests'
    ],
    license='MIT',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ]
)
