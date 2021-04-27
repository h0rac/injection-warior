# Author h0rac
from injection_warrior import common
import hashlib
import requests
import sys
import itertools
from bs4 import BeautifulSoup
import aiohttp
from aiohttp import FormData
import sys
import asyncio
import time
import hashlib
import requests
import zipfile
import json
from bs4 import BeautifulSoup
from termcolor import colored
from urllib.parse import urlparse
from prettytable import PrettyTable
import io
import zipfile
import gzip
from yarl import URL
import urllib
import re

class Injector(common.Common):
    """Main class of the framework
    """

    def __init__(self, proxy=None, debug=False, allow_redirects=True, safe_url_chars=""):
        """AI is creating summary for __init__

        Args:
            proxy ([type], optional): [description]. Defaults to None.
            debug (bool, optional): [description]. Defaults to False.
        """
        self.proxy = proxy
        self.debug = debug
        self.allow_redirects = allow_redirects
        self.resp_json = False
        self.req_json = False
        self.json_resp = None
        self.html = False
        self.elapsed = None
        self.params = None
        self.reflection_color_value = "red"
        self.reflection_color_key = "cyan"
        self.reflection_attr = "bold"
        self.req_counter = 0
        self.counter = 0
        self.header_param = {}
        self.body_param = {}
        self.cookie = {}
        self.url_param = {}
        self.resp_body = True
        self.input_payload = {}
        self.excluded = []
        self.safe_url_chars = safe_url_chars


    def _params_converted(self, payloads=[], params={}):
        if isinstance(params, aiohttp.FormData):
            return [params]
        dict_params = {}
        try:
            if len(payloads) == 0:
                payloads = [""]
            params_list = []
            for p in payloads:
                data = json.dumps(params)
                data = data.replace("%$%", str(p))
                dict_params = json.loads(data)
                params_list.append(dict_params)
            if self.debug:
                print(
                    colored("[*] Params converted: {}".format(params_list), "white"))
            return params_list
        except ValueError as e:
            print(colored("[-] Error _params_converted: {}".format(e), "red"))
            sys.exit(0)

   

    async def _fetch(self, http_method="get", session=None, url=None, html=False, injection_point="url", body_param={}, req_json=False, resp_json=False, cookie=None, url_param={}, header_param={}):
        # START HANDLERS FOR HEADER
        try:
            self.resp_json = resp_json
            self.html = html
            self.req_json = req_json
            new_param = ""
            body_url_encode_param =""
            if len(url_param.keys()) > 0:
                new_param = urllib.parse.urlencode(url_param, safe=self.safe_url_chars)
                url = URL(url+"?"+new_param)
            if len(body_param.keys()) > 0:
                body_url_encode_param = urllib.parse.urlencode(body_param, safe=self.safe_url_chars)
                    
            self.req_counter += 1
            if injection_point == "header" and len(header_param.keys()) > 0 and req_json and http_method == "get":
                async with session.get(url, proxy=self.proxy, cookies=cookie,  headers=header_param, data=body_url_encode_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
            
            elif injection_point == "header" and len(header_param.keys()) > 0 and http_method == "get" and not req_json:
                async with session.get(url, proxy=self.proxy, cookies=cookie, data=body_url_encode_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
    
            elif injection_point == "header" and len(header_param.keys()) > 0 and req_json and http_method == "post":
                async with session.post(url, proxy=self.proxy, cookies=cookie, json=body_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
            
            elif injection_point == "header" and len(header_param.keys()) > 0 and not req_json and http_method == "post":
                async with session.post(url, proxy=self.proxy, cookies=cookie, data=body_url_encode_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
                
            elif injection_point == "header" and len(header_param.keys()) > 0 and http_method == "put" and not req_json:
                async with session.put(url, proxy=self.proxy, cookies=cookie, data=body_url_encode_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "header" and len(header_param.keys()) > 0 and req_json and http_method == "put":
                async with session.put(url, proxy=self.proxy, cookies=cookie, json=body_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "header" and len(header_param.keys()) > 0 and http_method == "patch" and not req_json:
                async with session.patch(url, proxy=self.proxy, cookies=cookie, data=body_url_encode_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "header" and len(header_param.keys()) > 0 and req_json and http_method == "patch":
                async with session.patch(url, proxy=self.proxy, cookies=cookie, json=body_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
        
            elif injection_point == "header" and len(header_param.keys()) > 0 and http_method == "delete" and not req_json:
                async with session.delete(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
            
            elif injection_point == "header" and len(header_param.keys()) > 0 and req_json and http_method == "delete":
                async with session.delete(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "header" and len(header_param.keys()) > 0 and req_json and http_method == "head":
                async with session.head(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "header" and len(header_param.keys()) > 0 and http_method == "head" and not req_json:
                async with session.head(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "header" and len(header_param.keys()) > 0 and req_json and http_method == "options":
                async with session.options(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "header" and len(header_param.keys()) > 0 and http_method == "options" and not req_json:
                async with session.options(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            # END HANDLERS FOR HEADER
            # START HANDLERS FOR URL
            elif injection_point == "url" and http_method == "get":
                async with session.get(url , proxy=self.proxy, cookies=cookie, headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "url" and http_method == "post" and req_json:
                async with session.post(url, proxy=self.proxy, cookies=cookie, json=body_param,  headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "url" and http_method == "post" and not req_json:
                async with session.post(url, proxy=self.proxy, cookies=cookie, data=body_url_encode_param,  headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "url" and http_method == "put" and req_json:
                async with session.put(url, proxy=self.proxy, cookies=cookie, json=body_param,  headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "url" and http_method == "put" and not req_json:
                async with session.put(url, proxy=self.proxy, cookies=cookie, data=body_url_encode_param,  headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "url" and http_method == "patch" and req_json:
                async with session.patch(url, proxy=self.proxy, cookies=cookie, data=body_url_encode_param,  headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "url" and http_method == "patch" and not req_json:
                async with session.patch(url, proxy=self.proxy, cookies=cookie, json=body_param,  headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "url" and http_method == "delete":
                async with session.delete(url, proxy=self.proxy, cookies=cookie,  headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "url" and http_method == "options":
                async with session.options(url, proxy=self.proxy, cookies=cookie,  headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "url" and http_method == "head":
                async with session.head(url, proxy=self.proxy, cookies=cookie,  headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            # END HANDLERS FOR URL

            # START HANDLERS FOR COOKIE

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and req_json and http_method == "get":
                async with session.get(url, proxy=self.proxy, cookies=cookie,  headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and not req_json and http_method == "get":
                async with session.get(url, proxy=self.proxy, cookies=cookie,  headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and req_json and http_method == "post":
                async with session.post(url, proxy=self.proxy, cookies=cookie, json=body_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and not req_json and http_method == "post":
                async with session.post(url, proxy=self.proxy, cookies=cookie, data=body_url_encode_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and req_json and http_method == "put":
                async with session.put(url, proxy=self.proxy, cookies=cookie, json=body_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
            
            elif injection_point == "cookie" and len(cookie.keys()) > 0 and not req_json and http_method == "put":
                async with session.put(url, proxy=self.proxy, cookies=cookie, data=body_url_encode_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
            
            elif injection_point == "cookie" and len(cookie.keys()) > 0 and req_json and http_method == "patch":
                async with session.patch(url, proxy=self.proxy, cookies=cookie, json=body_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and not req_json and http_method == "patch":
                async with session.patch(url, proxy=self.proxy, cookies=cookie, data=body_url_encode_param, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and req_json and http_method == "delete":
                async with session.delete(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and not req_json and http_method == "delete":
                async with session.delete(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and req_json and http_method == "options":
                async with session.options(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and not req_json and http_method == "options":
                async with session.options(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and req_json and http_method == "head":
                async with session.head(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and not req_json and http_method == "head":
                async with session.head(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "cookie" and len(cookie.keys()) > 0 and http_method == "get" and not req_json:
                async with session.get(url, proxy=self.proxy, cookies=cookie,  headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
        # END HANDLERS FOR COOKIE

        # START HANDLERS FOR BODY

            elif injection_point == "body" and not req_json and http_method == "post":
                async with session.post(url, proxy=self.proxy, data=body_url_encode_param, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "body" and req_json and http_method == "post":
                async with session.post(url, proxy=self.proxy, json=body_param, cookies=cookie, headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
                
            elif injection_point == "body" and not req_json and http_method == "put":
                async with session.put(url, proxy=self.proxy, data=body_url_encode_param, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "body" and req_json and http_method == "put":
                async with session.put(url, proxy=self.proxy, json=body_param, cookies=cookie, headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
            
            elif injection_point == "body" and not req_json and http_method == "patch":
                async with session.patch(url, proxy=self.proxy, data=body_url_encode_param, cookies=cookie, headers=header_param, allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "body" and req_json and http_method == "patch":
                async with session.patch(url, proxy=self.proxy, json=body_param, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
            
            elif injection_point == "body" and not req_json and http_method == "head":
                async with session.head(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "body" and req_json and http_method == "head":
                async with session.head(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "body" and not req_json and http_method == "options":
                async with session.options(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "body" and req_json and http_method == "options":
                async with session.options(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "body" and not req_json and http_method == "delete":
                async with session.delete(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)

            elif injection_point == "body" and req_json and http_method == "delete":
                async with session.delete(url, proxy=self.proxy, cookies=cookie, headers=header_param,  allow_redirects=self.allow_redirects) as response:
                    return await self._display(response=response, body_param=body_param, html=html, resp_json=resp_json, cookie_param=cookie, url_param=url_param, header_param=header_param)
            
        except Exception as e:
            print("[-] Exception in _fetch: {}".format(e))
            sys.exit(0)
        # END HANDLERS FOR BODY

    async def _display(self, response=None, body_param={}, html=False, resp_json=None, cookie_param={}, url_param={}, header_param={}):
        multiplier = 60 
        resp = response
        parsed_url = urlparse(str(resp.url))
        question_mark = "?"
        
        if len(body_param.keys()) > 0:
            self.input_payload = body_param    
        elif len(cookie_param.keys()) > 0:
            self.input_payload = cookie_param    
        elif len(url_param.keys()) > 0:
             self.input_payload = url_param    
        elif len(header_param.keys()) > 0:
            self.input_payload = header_param

        print("\r\n")
        print(colored("-"*multiplier+"REQUEST {} HEADERS".format(self.counter)+"-"*multiplier, "blue"))
        print("\r\n")
        question_mark = "?"
        print(colored("[+] {} {}{}{} HTTP/1.1".format(resp.method.upper(), parsed_url.path if parsed_url.path != '' else "/" , question_mark if resp.url.query_string else '',
                                                        resp.url.query_string if resp.url.query_string != None else None), "yellow"))
        if 'Host' not in resp.request_info.headers:
            print(
                colored("[+] Host: {}".format(parsed_url.netloc), "yellow"))
        for k, v in resp.request_info.headers.items():
            print(colored("[+] {}: {}".format(k, v), "yellow"))
           
        if resp.method != "GET":
            if self.req_json:
                print("\r\n")
                print(colored("-"*multiplier +
                            "REQUEST {} BODY".format(self.counter)+"-"*multiplier, "blue"))
                print("\r\n")
                print(json.dumps(body_param, indent=2))
            else:
                print("\r\n")
                print(colored("-"*multiplier+"REQUEST BODY"+"-"*multiplier, "blue"))
                print("\r\n")
                if isinstance(body_param, aiohttp.FormData):
                    for param in body_param._fields:
                        for p in param:
                            print(p)
                else:
                    print(body_param) 
    
        print("\r\n")
        print(colored("-"*multiplier +
                        "RESPONSE {} HEADERS".format(self.counter)+"-"*multiplier, "blue"))
        print("\r\n")
        print(colored("[+] HTTP/1.1 {}".format(resp.status), "cyan"))
        for k, v in resp.headers.items():
            print(colored("[+] {}: {}".format(k, v), "cyan"))
        checked = ""
        if html:
            resp = await response.text()
            self.json_resp = None
            self.soup = BeautifulSoup(resp, "html.parser")
            if self.resp_body:
                checked = self._check_reflected_params(input_payload=self.input_payload, response = self.soup.prettify())
                print("\r\n")
                print(colored("-"*multiplier +
                                "RESPONSE {} BODY".format(self.counter)+"-"*multiplier, "blue"))
                print("\r\n")
                print(checked)
            return {"json_resp": self.json_resp, "raw_response": response, "soup":self.soup, "cookie": cookie_param, "url_param": url_param, "header_param": header_param, "body_param": body_param, "elapsed": self.elapsed}
        elif not html and resp_json:
            self.json_resp = await response.json(content_type=None)
            if self.resp_body:
                if self.resp_json:
                    string_response = json.dumps(self.json_resp, indent=2)
                    checked = self._check_reflected_params(input_payload=self.input_payload, response=string_response)
                    print("\r\n")
                    print(colored("-"*multiplier +
                                    "RESPONSE {} BODY".format(self.counter)+"-"*multiplier, "blue"))
                    print("\r\n")
                    print(checked)
            return {"json_resp": self.json_resp, "raw_response": response, "soup": None, "cookie": cookie_param, "url_param": url_param, "header_param": header_param, "body_param": body_param, "elapsed": self.elapsed}
        return {"json_resp": None, "raw_response": response, "soup": None, "cookie": cookie_param, "url_param": url_param, "header_param": header_param, "body_param": body_param, "elapsed": self.elapsed}
        

    def _check_reflected_params(self, input_payload={}, response=""):
        colored_resp = response
        for k,v in input_payload.items():
            if isinstance(k, str):
                results = re.findall(k, response)
                for r in results:
                    if r in response:
                        colored_resp = colored_resp.replace(k, colored(r, self.reflection_color_key, attrs=[self.reflection_attr]))
            if isinstance(v, dict):
                colored_resp = self._check_reflected_params(v, colored_resp)
            elif isinstance(v, list):
                for item in v:
                    colored_resp = self._check_reflected_params(item, colored_resp)
            elif v in response and k not in self.excluded:
                colored_resp = colored_resp.replace(v, colored(v, self.reflection_color_value, attrs=[self.reflection_attr]))
        return colored_resp
                

    async def _on_request_start(self, session, trace_config_ctx, params):
        print(colored("[+] Starting request...", "magenta"), end='\r')
        start_time = time.time()
        trace_config_ctx.start = start_time

    async def _on_request_end(self, session, trace_config_ctx, params):
        self.counter +=1
        end_time = time.time()
        self.elapsed = end_time - trace_config_ctx.start
        
    async def _fetch_all(self, http_method="get", urls=[], html=False, injection_point="url", body_params=[], req_json=False, resp_json=False, cookie_params=[], url_params=[], header_params=[]):

        trace_config = aiohttp.TraceConfig()
        trace_config.on_request_start.append(self._on_request_start)
        trace_config.on_request_end.append(self._on_request_end)

        if injection_point == "url" and len(urls) > 1:
            async with aiohttp.ClientSession(trace_configs=[trace_config], connector=aiohttp.TCPConnector(ssl=False)) as session:
                tasks = []
                for i in range(0, len(urls)):
                    tasks.append(
                        self._fetch(
                            http_method=http_method,
                            session=session,
                            url=urls[i],
                            html=html,
                            injection_point=injection_point,
                            body_param=body_params,
                            req_json=req_json,
                            resp_json=resp_json,
                            cookie=cookie_params,
                            url_param=url_params[i],
                            header_param=header_params,
                        )
                    )
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                return responses

        elif injection_point == "url":
            async with aiohttp.ClientSession(trace_configs=[trace_config], connector=aiohttp.TCPConnector(ssl=False)) as session:
                tasks = []
                for i in range(0, len(url_params)):
                    tasks.append(
                        self._fetch(
                            http_method=http_method,
                            session=session,
                            url=urls[0],
                            html=html,
                            injection_point=injection_point,
                            body_param=body_params,
                            req_json=req_json,
                            resp_json=resp_json,
                            cookie=cookie_params,
                            url_param=url_params[i],
                            header_param=header_params,
                        )
                    )
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                return responses

        elif injection_point == "body":
            async with aiohttp.ClientSession(trace_configs=[trace_config], connector=aiohttp.TCPConnector(ssl=False)) as session:
                tasks = []
                for i in range(0, len(body_params)):
                    tasks.append(
                        self._fetch(
                            http_method=http_method,
                            session=session,
                            url=urls[0],
                            html=html,
                            body_param=body_params[i],
                            header_param=header_params,
                            injection_point=injection_point,
                            req_json=req_json,
                            resp_json=resp_json,
                            cookie=cookie_params,
                        )
                    )
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                return responses
        elif injection_point == "cookie":
            async with aiohttp.ClientSession(trace_configs=[trace_config], connector=aiohttp.TCPConnector(ssl=False)) as session:
                tasks = []
                for i in range(0, len(cookie_params)):
                    tasks.append(
                        self._fetch(
                            http_method=http_method,
                            session=session,
                            url=urls[0],
                            html=html,
                            body_param=body_params,
                            injection_point=injection_point,
                            header_param=header_params,
                            url_param=url_params,
                            req_json=req_json,
                            resp_json=resp_json,
                            cookie=cookie_params[i],
                        )
                    )
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                return responses

        elif injection_point == "header":
            async with aiohttp.ClientSession(trace_configs=[trace_config], connector=aiohttp.TCPConnector(ssl=False)) as session:
                tasks = []
                for i in range(0, len(header_params)):
                    tasks.append(
                        self._fetch(
                            http_method=http_method,
                            session=session,
                            url=urls[0],
                            html=html,
                            body_param=body_params,
                            injection_point=injection_point,
                            header_param=header_params[i],
                            url_param=url_params,
                            req_json=req_json,
                            resp_json=resp_json,
                            cookie=cookie_params,
                        )
                    )
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                return responses

    def _run(self, http_method="get", urls=[], html=False, injection_point="url", body_params={}, req_json=False, resp_json=False, cookie_params=[], url_params=[], header_params=[], resp_body=None):
        """AI is creating summary for _run

        Args:
            http_method (str, optional): [description]. Defaults to "get".
            url (str, optional): [description]. Defaults to "".
            html (bool, optional): [description]. Defaults to False.
            injection_point (str, optional): [description]. Defaults to "url".
            body_params (dict, optional): [description]. Defaults to {}.
            req_json (bool, optional): [description]. Defaults to False.
            resp_json (bool, optional): [description]. Defaults to False.
            cookie_params (list, optional): [description]. Defaults to [].
            url_params (list, optional): [description]. Defaults to [].
            header_params (list, optional): [description]. Defaults to [].

        Returns:
            list]: async HTTP responses list
        """
        self.resp_body = resp_body
        responses = asyncio.run(self._fetch_all(http_method=http_method, urls=urls, html=html, injection_point=injection_point,
                                                body_params=body_params, req_json=req_json, resp_json=resp_json, cookie_params=cookie_params, url_params=url_params, header_params=header_params))
        # print(colored(
        #     "[+] Total executed requests: {}.".format(self.req_counter), "magenta"))
        print("\r\n")
        print(colored(
            "[+] Total time elapsed: {} seconds".format(self.elapsed), "magenta"))
        return responses

    def inject_payload(self, url="", payloads=[], http_method="get", injection_point="url",  body_params={}, 
                       req_json=False, resp_json=False, html=False, cookie_params={}, url_params={}, 
                       header_params={}, resp_body=True, noise_params=[], **kwargs):
        """method allows to inject payloads to HTTP request/s
           When payloads are used, header|body|cookie|url dictionary should have value as %$%
           example: url_params = {"productId": %$%}

        Args:
            url (str): [URL for endpoint]. Defaults to "".
            payloads (list, optional): [list of payloads for which requests will be generated]. Defaults to [].
            http_method (str, optional): [HTTP method (GET/POST/PUT/PATCH/DELETE/OPTIONS/HEAD)]. Defaults to "get".
            injection_point (str, optional): [Place where payloads should be injected]. Defaults to "url".
            body_params (dict, optional): [Dictionary with key:value pair for parameters]. Defaults to {}.
            req_json (bool, optional): [Flag define if request should be send as JSON formatted data]. Defaults to False.
            resp_json (bool, optional): [Flag define if response should be displayed as JSON formatted data]. Defaults to False.
            html (bool, optional): [Flag define if response should be displayed as HTML]. Defaults to False.
            cookie_params (dict, optional): [Dictionary with key:value pair for parameters]. Defaults to {}.
            url_params (list, optional): [Dictionary with key:value pair for parameters]. Defaults to {}.
            header_params (list, optional): [Dictionary with key:value pair for parameters]. Defaults to {}.
            resp_body (bool, optional): [Flag define if response body should be printed on output console]. Defaults to True
            kwargs(dict, optional) [quote: "'", delimiter: '+', comment: '--', comma: ",", oracle: False, nulls: 1, table_name:  "", column_name_1: "", column_name_2: "", sleep: 5]

        Returns:
            [dict]: Dictionary as key value pair
        """
        if injection_point == "body" and http_method == "get":
            print(colored(
                "[-] Unsupported combination for {} and {}".format(injection_point, http_method), "red"))
            sys.exit(0)
        if self.debug:
            print(colored(
                '''[+] Injection 'Warrior' selected parameters: 
            PAYLOADS: {}
            HTTP METHOD: {}
            URL: {}
            RETURN HTML: {}
            INJECTION POINT: {}
            BODY PARAMS: {}
            COOKIE PARAMS: {}
            URL PARAMS: {}
            HEADER PARAMS: {}
            REQ JSON: {}
            RESP JSON: {}
            RESP_BODY: {}
            NOISE PARAMS: {}
            KWARGS:{}
            '''.format(payloads, http_method, url, html, injection_point, body_params, cookie_params, url_params, header_params, req_json, resp_json, resp_body, noise_params, kwargs), "yellow"))
        values = []
        self.resp_json = resp_json
        self.req_json = req_json
        self.html = html
        http_method = http_method.lower()
        self.http_method = http_method
        self.excluded = noise_params
        
        if len(payloads) == 0 and isinstance(url, list):
            urls = url
        else:
            urls = self._url_path_parse(url, payloads)
            if not len(urls) > 0:
                urls = [url]
        
      
        if injection_point == "header":
            values = self._parse_template(payloads=payloads, **kwargs)
            header_params_list = self._params_converted(
                payloads=values, params=header_params)
            return self._run(http_method=http_method, urls=urls, html=html, url_params=url_params, body_params=body_params, header_params=header_params_list, injection_point=injection_point, cookie_params=cookie_params, req_json=req_json, resp_json=resp_json, resp_body=resp_body)

        elif injection_point == "url":
            values = self._parse_template(payloads=payloads, **kwargs)
            url_params_list = self._params_converted(
                payloads=values, params=url_params)
            return self._run(http_method=http_method, urls=urls, html=html, url_params=url_params_list, injection_point=injection_point, cookie_params=cookie_params, req_json=req_json, resp_json=resp_json, header_params=header_params, resp_body=resp_body)

        elif injection_point == "body":
            values = self._parse_template(payloads=payloads, **kwargs)
            body_params_list = self._params_converted(
                payloads=values, params=body_params)
            return self._run(http_method=http_method, urls=urls, html=html, url_params=url_params, body_params=body_params_list, injection_point=injection_point, cookie_params=cookie_params, header_params=header_params, req_json=req_json, resp_json=resp_json, resp_body=resp_body)

        elif injection_point == "cookie":
            values = self._parse_template(payloads=payloads, **kwargs)
            cookie_params_list = self._params_converted(
                payloads=values, params=cookie_params)
            return self._run(http_method=http_method, urls=urls, html=html, url_params=url_params, body_params=body_params, injection_point=injection_point, cookie_params=cookie_params_list, header_params=header_params, req_json=req_json, resp_json=resp_json, resp_body=resp_body)       

    def _url_path_parse(self, url="", payloads=[]):
        urls = []
        if "%$%" in url:
            for p in payloads:
                temp = url.replace("%$%", str(p))
                urls.append(temp)
        return urls
