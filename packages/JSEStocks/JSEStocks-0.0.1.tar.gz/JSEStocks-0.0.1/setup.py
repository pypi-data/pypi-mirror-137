from setuptools import setup, find_packages

setup(
    #metadata here
    name="JSEStocks",
    version="0.0.1",
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
