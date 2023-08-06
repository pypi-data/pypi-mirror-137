try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='twitcent',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    version='0.0.2',
    description='A package for analyzing twitter sentiments based on keyword and number of tweets',
    license='MIT',
    author='Nicolus Rotich',
    author_email='nicholas.rotich@gmail.com',
    install_requires=[
    	"setuptools>=57",
    	"wheel",
    	"tweepy>=4.0.0"
    ],
    url='https://nkrtech.com',
    download_url='https://github.com/moinonin/twitcent/archive/refs/heads/main.zip',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
