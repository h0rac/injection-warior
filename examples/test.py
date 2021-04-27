from injection_warrior import warrior

inj = warrior.Injector(proxy="http://127.0.0.1:8080", debug=False)
url = "https://ac961f391e6688f2805b47f6008e00b8.web-security-academy.net/product"

payloads = [str(x) for x in range(0, 100)]

inj.inject_payload(
    url=url,
    url_params={"productId": "%$%"},
    injection_point="url",
    payloads=payloads,
    resp_body=True,
    html=True,
    req_json=False,
    http_method="get"
)