import json
from operator import sub
from termcolor import colored
import os
import sys
import re

class Postman():
    """Postman parser class
    """
    def __init__(self, collection_path="", collection_name="TEST_collection"):
        self.collection_path = collection_path
        self.collection = self._load_collection(path=self.collection_path)
        script_dir = os.getcwd()
        self.abs_file_path = os.path.join(script_dir, collection_name)
        self.path = self.abs_file_path.replace('/injection_warrior', '')
        self.base_path = self.abs_file_path.replace('/injection_warrior', '')
        if not os.path.exists(self.base_path):
            os.mkdir(self.abs_file_path.replace('/injection_warrior', ''))
        self.filename = ""
        self.f = ""
        self.top_directory = None
        self.count = 0
        self.sub_directory = None
        
    def _load_collection(self, path=""):
        try:
            postman_file = open(path, 'r')
            return json.load(postman_file)
        except FileNotFoundError as e:
            print(colored("load_collection error: ".format(e), "red"))
    
    def __parse_params(self, params):
        for key,value in params.items():
            new_params = {}
            if key == "body" and value.get('raw') != None and value.get('raw') != '':
                raw_value = value.get('raw')
                raw_value = json.loads(raw_value)
                params['body'] = raw_value
            if isinstance(params[key], list):
                for r in params[key]:
                    if not isinstance(r, str):
                        new_params[r.get('key')] =r.get('value')
                        params[key] = new_params
            elif isinstance(params[key], dict):
                self.__parse_params(params[key])      
        return params
    
    def parse_collection(self, collection):
        """method parse postman v2.1 collection creating file/folder tree structure

        Args:
            collection ([type]): [description]
        """
        json_file = ""
        
        for key, value in collection.items():   
            if key == "item" and "request" not in collection:
                if isinstance(value, list):
                    for x in value:
                        self.parse_collection(x)   
                self.base_path = self.abs_file_path.replace('/injection_warrior', '') 
        
            elif key == "name" and 'request' not in collection: 
                is_subfolder = collection.get('_postman_isSubFolder')
                if is_subfolder != None and is_subfolder == True:
                    print(colored("|", "blue"))
                    print(colored("|--Create subdirectory {}".format(value), "blue"))
                    print(colored("   |", "blue"))
                    print(colored("   ----", "blue"))
                    self.sub_directory = self.top_directory + "/" +value
                    braces = re.findall(r'\{[^{}]+\}', self.sub_directory)
                    if len(braces) > 0:
                        new_dir = self.sub_directory.replace("/"+braces[0], '')
                        self.sub_directory = new_dir
                    if not os.path.exists(self.sub_directory):
                        os.mkdir(self.sub_directory)
                    self.path = self.sub_directory
                    self.base_path = self.path
                else:
                    print(colored("Create directory {}".format(value), "cyan"))
                    self.top_directory = self.base_path+"/"+value
                    braces = re.findall(r'\{[^{}]+\}', self.top_directory)
                    if len(braces) > 0:
                        new_dir = self.top_directory.replace("/"+braces[0], '')
                        self.top_directory = new_dir
                    if not os.path.exists(self.top_directory):
                        os.mkdir(self.top_directory)
                    self.path = self.top_directory
                    self.base_path = self.path
                
            elif key == "name" and value in collection['name'] and 'request' in collection:
                if self.base_path == self.abs_file_path.replace('/injection_warrior', ''):
                    self.path = self.base_path
                self.filename = value
                
            elif key == "request":
                if len(self.filename) > 0:
                    print("\t|----",self.filename)
                    os.chdir(self.path)
                    json_file = self.filename+".json"
                    json_file = json_file.replace(" ", "_").replace("/", "_")
                    data = self.__parse_params(value)
                    data |= {'payloads':[]}
                    if not os.path.isfile(self.filename): 
                        self.f = open(json_file, 'w')
                        json_format = json.dumps(data, indent=4)
                        self.f.write(json_format)
                    self.filename = None


