from setuptools import setup

setup(
    name='umbrella',
    version='0.3.1',
    py_modules=['um'],
    include_package_data=True,
    install_requires=[
        'click',
        'PyGithub',
        'executor',
        'jenkinsapi',
    ],
    entry_points='''
        [console_scripts]
        um=um:cli
    ''',
)
