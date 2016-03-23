from setuptools import setup

setup(
    name='umbrella',
    version='0.2.0',
    py_modules=['um'],
    include_package_data=True,
    install_requires=[
        'click',
        'PyGithub',
        'excutor'
    ],
    entry_points='''
        [console_scripts]
        um=um:cli
    ''',
)
