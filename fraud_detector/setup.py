from setuptools import setup

setup(
    name='fraud',
    version='0.01',
    author='David Perez',
    author_email='david.5697.9@gmail.com',
    packages=['fraud'],
    install_requires = ['pandas', 'numpy'],
    entry_points =  {
        "consoles_scripts":[
            'fraud = fraud.__main__:main'
            ]
    }   
)