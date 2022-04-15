import requests
import secret.secrets as secrets

def get_auth_headers():
    body = {
        "grant_type":"client_credentials",
        "client_id":secrets.gfycat_client_id,
        "client_secret":secrets.gfycat_secret,
    }

    token = requests.post("https://api.gfycat.com/v1/oauth/token", json=body, timeout=3).json()

    access_token = token["access_token"]

    auth_headers = {
        "Authorization" : "Bearer {}".format(access_token)
    }

    return auth_headers

def upload_gif(title, tags, file):
    jif_info = {
        "title" : title,
        "tags" : tags,
    }

    headers = get_auth_headers()

    create = requests.post("https://api.gfycat.com/v1/gfycats", json=jif_info, headers=headers)
    gfyid = create.json().get("gfyname")

    if gfyid:
        print("gif will be @ https://gfycat.com/{}".format(gfyid))

        with open(file, "rb") as video:
            res = requests.put("https://filedrop.gfycat.com/{}".format(gfyid), video)
            print(res.status_code)
