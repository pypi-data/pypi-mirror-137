from setuptools import setup, find_packages


VERSION = '1.0.0'
DESCRIPTION = 'Tools that are useful for building web-scraping automated bots.'
LONG_DESCRIPTION = """This package is a template for you
    to create your own bot using Python.
    
    In order to do that, you don't need to use 
    each method each time you create a new bot.
    The datas you collect using the 'get_hypertexts_links'
    are saved in a folder called 'datas.json'. You are free 
    to modify the path or the name, but I do not reccomend 
    this method."""

# Setting up
setup(
    name="web_scraping_bot_template",
    version=VERSION,
    author="Antonin GENElot<",
    author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'bs4'],
    keywords=['python', 'bot', 'automated', 'web-scraping', 'python bot'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)