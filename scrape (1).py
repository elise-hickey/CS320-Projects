# project: p3
# submitter: ejhickey3
# partner: none
# hours: 2


from collections import deque
import pandas as pd
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import requests
import urllib.request, urllib.parse, urllib.error


def reveal_secrets(driver, url, travellog):
    #generate a password from the "clues" column of the travellog DataFrame.
    #For example, if travellog is the big DataFrame built after doing BFS (as shown earlier),
    #the password will start with "17138..."
    password = ""
    for val in travellog["clue"]:
        password = password + str(val)
    #visit url with the driver
    driver.get(url)
    #automate typing the password in the box and clicking "GO"
    pswd = driver.find_element("id", "password")
    btn = driver.find_element("id", "attempt-button")
    pswd.send_keys(password)
    btn.click()
    #wait until the pages is loaded (perhaps with time.sleep)
    time.sleep(0.5)
    #click the "View Location" button and wait until the result finishes loading
    loc_btn = driver.find_element("id", "securityBtn")
    loc_btn.click()
    time.sleep(1)
    #save the image that appears to a file named 'Current_Location.jpg' 
    #(use the requests module to do the download, once you get the URL from selenium)
    img = driver.find_element("id", "image")
    image = img.get_attribute("src")
    image_bytes = urllib.request.urlopen(image).read()  #citation: https://runestone.academy/ns/books/published/py4e-int/network/retrievingbinaryfilesoverurllib.html
    with open("Current_Location.jpg", "wb") as f:
        f.write(image_bytes)
    location = driver.find_element("id", "location")  

    return location.text
    

    
    



class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ Record the node value in self.order, and return its children
        param: node
        return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        # 1. clear out visited set and order list
        self.visited = set()
        self.order = []
        # 2. start recursive search by calling dfs_visit
        self.dfs_visit(node)

    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return 
        # 2. mark node as visited by adding it to the set
        self.visited.add(node)
        # 3. call self.visit_and_get_children(node) to get the children
        children = self.visit_and_get_children(node)
        # 4. in a loop, call dfs_visit on each of the children
        for child in children:
            self.dfs_visit(child)
            
            
    def bfs_search(self, node):
        self.order.clear()
        queue = deque([node])
        seen = {node}
        while len(queue) > 0:
            curr_node = queue.popleft()
            children = self.visit_and_get_children(curr_node)
            for child in children:
                if child not in seen:
                    queue.append(child)
                    seen.add(child)

                    
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def visit_and_get_children(self, node):
        # TODO: Record the node value in self.order
        self.order.append(node)
        children = []
        # TODO: use `self.df` to determine what children the node has and append them
        for node, has_edge in self.df.loc[node].items():
            if has_edge  == 1:
                children.append(node)
        return children
    
    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
        
    
    def visit_and_get_children(self, file):
        file = os.path.join('file_nodes', file)
        with open(file) as f:
            value = f.readline()
            self.order.append(value.strip())
            children = f.readline().strip().split(",")
        return children
    
    def concat_order(self):
        string = ""
        for val in self.order:
            string = string + val
        
        return string
    
    
class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.tbs = []
        
        
    def visit_and_get_children(self, url):
        self.order.append(url)
        links = []
        self.driver.get(url)
        for elem in self.driver.find_elements("tag name", "a"):
            links.append(elem.get_attribute("href"))
        self.tbs.append(pd.read_html(self.driver.page_source)[0])
        return links
    
    def table(self):
        return pd.concat(self.tbs, ignore_index=True)
        
        