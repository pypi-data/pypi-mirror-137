from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    #metadata here
    name="JSEStocks",
    long_description=long_description,
    long_description_content_type='text/markdown',
    version="0.0.2",
    author="Ashlin Darius Govindasamy",
    author_email="adg@adgstudios.co.ZA",
    url="https://www.adgstudios.co.za",
    description="a module that returns all the stock data in JSE",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #license here
    license='MIT', 
    #modules here
    install_requires=["numpy","yfinance"]
)
