from setuptools import setup, find_packages

setup(
    name="fraud",
    version="0.01",
    packages=find_packages(),
    install_requires=["pandas", "numpy", ""],
    entry_points={
        "console_scripts": [
            "fraud = fraud.__main__:main"
        ]
    },
    package_data={
        "fraud.assets.model": ["*"],
        "fraud.assets.controller": ["*"],
        "fraud.assets.config": ["config.json"],
        "fraud.assets.images": ["app_icon.ico"],
        "fraud.assets.packages": ["*"],
        "fraud.assets.view": ["*"],
    },
)
