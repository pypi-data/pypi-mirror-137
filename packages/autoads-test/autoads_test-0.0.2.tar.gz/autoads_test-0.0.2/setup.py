from setuptools import find_packages, setup

with open("requirements.txt",'r+') as f:
    lines = f.readlines()

requirements = [str(x).strip() for x in lines]

setup(
    version='0.0.2',
    name='autoads_test',
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=requirements,
    keywords="AutoAds",
    # url="https://github.com/Bonobo791/rl-trade/",
    description="Easy to use Ads library",
    long_description="AutoAds is a Easy to use Ads library",
)