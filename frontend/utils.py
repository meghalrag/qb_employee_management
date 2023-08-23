def format_api_res(response):
    res = {}
    res["status_code"] = response.status_code
    if response.status_code == 204:
        pass
    elif response.status_code in [200, 201]:
        res["data"] = response.json()
    else:
        res_json = response.json()
        if "message" in res_json:
            res_json["error"] = res_json["message"]
        res.update(res_json)
    return res

def export_to_csv(data):
    pass

def export_to_xlsx(data):
    pass

def export_to_json(data):
    pass
