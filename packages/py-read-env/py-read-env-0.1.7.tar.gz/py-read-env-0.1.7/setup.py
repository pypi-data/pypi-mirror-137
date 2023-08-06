"""Setup for read env"""
from setuptools import setup

requirements = [
    'python-dotenv~=0.19.2',
]

setup(
    name='py-read-env',
    version='0.1.7',
    license='MIT',
    description='py read env for cross OS environment include windows',
    author='liuspatt',
    author_email='liuspatt@readenv.com',
    url='https://github.com/liuspatt/py-read-env',
    keywords=['env', 'python', 'windows', 'environment variables', 'deployments', 'settings', 'env',
              'configurations', 'python'],
    install_requires=requirements,
    python_requires=">=3.5",
    packages=['readenv'],
    package_dir={'': 'src'},
    package_data={
        'readenv': ['py.typed'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Environment :: Web Environment',
    ],
)
