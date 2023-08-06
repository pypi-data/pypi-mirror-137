"""
    This package is in his 1.0
    version. It will be improved in the future,
    so please be patient if it does not 
    what you expect it to do.
    
    This package is a template for you
    to create your own bot using Python.
    
    In order to do that, you don't need to use 
    each method each time you create a new bot.
    The datas you collect using the 'get_hypertexts_links'
    are saved in a folder called 'datas.json'. You are free 
    to modify the path or the name, but I do not reccomend 
    this method.
    
    Copyright : Antonin GENELOT, 2022
    Contact for help : jaimelesfraisesbleues@gmail.com
"""


import json
import requests
from bs4 import BeautifulSoup

class MainBot:
    def __init__(self, url):
        self.url = url     
        if type(self.url) == 'string':
            raise TypeError('Your URL must be a string !')
        self.response = requests.get(self.url)
        self.html_code = BeautifulSoup(self.response.text, 'lxml')
        self.links = {}

    def get_hypertexts_links(self, url):
        """
            Get all the hypertexts links 
            of the given URL.
        """
        self.url = url
        self.link = self.html_code.findAll("a")
        self.link = str(self.link)
        self.links["all-links"] = self.link.split(",")
        links_data = json.dumps(self.links, indent=4)
        
        with open("datas.json", "w") as file:
            file.write(links_data + "\n")
        print(f"The datas have been saved in the file 'json_datas/main_bot_test/links.json'.")

    def get_response_from(self, url):
        """
            Get the server's response
            from the URL.
        """
        if type(url) != 'string':
            url = str(url)
        global response
        if self.response.ok:
            print("Connection successful !\b")
        return url

    def get_title_from_page(self):
        """
            Get the title
            of the page.
        """
        global html_code
        title = self.html_code.find("title")
        print(f"The title of the page is : {title.text} \b")
        
    def get_element_by_HTML_markup(self, element):
        """
            Get any element
            by its HTML markup. This method 
            returns the text which 
            is contained in the HTML code of the 
            element that you are looking for.
        """
        global html_code
        self.element = self.html_code.find(element)
        if self.element is None:
            raise NameError("The element you are trying to access does not exist on this page. Make sure the name is correct.")
        print(f"The element '{self.element.text}' exists and is on the HTML source code of this page.")
        