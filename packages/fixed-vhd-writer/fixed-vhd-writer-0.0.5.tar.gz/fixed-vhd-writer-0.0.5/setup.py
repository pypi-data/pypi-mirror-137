import os

from setuptools import setup

from fixed_vhd_writer.version import __version__

# What packages are required for this module to be executed?
requires = [
    'click',
]

root = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
with open(os.path.join(root, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='fixed-vhd-writer',
        version=__version__,
        url='https://github.com/fujiawei-dev/fixed-vhd-writer',
        packages=['fixed_vhd_writer'],
        description='Fixed VHD writer.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='MIT',
        author='Rustle Karl',
        author_email='fu.jiawei@outlook.com',
        install_requires=requires,

        entry_points={
            'console_scripts': [
                'vhdwriter=fixed_vhd_writer.cmd:fixed_vhd_writer',
            ],
        },

        classifiers=[
            'Intended Audience :: Developers',
            'Environment :: Console',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
)
