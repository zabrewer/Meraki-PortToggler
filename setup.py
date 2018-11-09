from setuptools import setup

setup(
    name='PortToggler',
    version='0.1',
    py_modules=['PortToggler'],
    install_requires=[
        'Click','requests','click_config_file',
    ],
    entry_points='''
        [console_scripts]
        PortToggler=PortToggler:cli
    ''',
)

