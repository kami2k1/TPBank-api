import requests
from dotenv import load_dotenv

import os

## data 
deviceId = "J4AEald6hatSqk5b6Leqlk1iBVUuYWHpJGBvjsQD0y4"
headers = {
    "accept": "application/json, text/plain, */*",
    "app_version": "2025.03.31",
    "authorization": "Bearer ", 
    "content-type": "application/json",
    "device_id":deviceId,
    "device_name": "Chrome",
    "platform_name": "WEB",
    "platform_version": "136",
    "referer": "https://ebank.tpb.vn/retail/vX/",
    "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "source_app": "HYDRO",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "user_name": "HYD"
}
token = None
import time

## burrh 
def load():
    load_dotenv()


Rq = requests.session()
def _check(data : dict):
    data_post ={"rsaToken":data['rsa_token'],
                "transactionId":data["transaction_id"]}
    r = Rq.post("https://ebank.tpb.vn/gateway/api/auth/transaction/check",headers=headers,json=data_post)
    r = r.json()
    if r['status'] == "FAIL":
        print("That bai fuck ")
        return False
    if r['status'] == "CONFIRM":
            return login(data["transaction_id"])
    print("check sau 2s nx  vui long vo app va xac thuc ( bam vao smart otp va quet mat)")
    time.sleep(2)
    return _check(data)
    

def _packet(data : dict, code : int ):
    match code:
        case 200:
            headers['authorization'] = f"Bearer {data['access_token']}"
            print(data)
            print("login thaanh cong roi")
            return True
        case 401:
            if data['error']['error_code'] == "50525":
                print("sai mat khau khong spam login sai 5 lan la khao tai khoan ")
            elif data['error']['error_code'] == "70101":
                return _check(data["error"])


    return False

def login(id : str = ""):
    load()
    data_login={"username":os.getenv("user"),
                "password":os.getenv("pass"),
                "deviceId":deviceId,
                "transactionId":id}
    r = Rq.post("https://ebank.tpb.vn/gateway/api/auth/login/v3",headers=headers,json=data_login)
    return _packet(r.json(),r.status_code)
