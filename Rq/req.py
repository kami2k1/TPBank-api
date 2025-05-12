import requests
from dotenv import load_dotenv

import os

## data 
deviceId = "J4AEald6hatSqk5b6Leqlk1iBVUuYWHpJGBvjsQDy4"
app_vison =  "2025.03.31"
headers = {
    "accept": "application/json, text/plain, */*",
    "app_version":app_vison,
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

from datetime import datetime
from dateutil.relativedelta import relativedelta




Rq = requests.session()

def _date():
    today = datetime.now()
    to_date = today.strftime("%Y%m%d")
    from_date = (today - relativedelta(months=3)).strftime("%Y%m%d")
    return from_date , to_date
maxpage = 5
def _dologin():
    # r = Rq.get("https://ebank.tpb.vn/gateway/api/customers-presentation-service/v1/customers",headers=headers)
    # code = r.json()['cifNumber']
    _driverId = _reg_driver()
    # r = Rq.get(f"https://ebank.tpb.vn/gateway/api/customers-presentation-service/v1/etoken-plus/check-status?code={code}"
    #            )
    jsonpost = {"deviceManagementId":_driverId,"appVersion":app_vison}
    r = Rq.post("https://ebank.tpb.vn/gateway/api/device-presentation-service/v1/device/login",json=jsonpost,headers=headers)
    if r.status_code == 201:
        print("ok")
    else:
        print("that bai code ", r.status_code)
def _reg_driver():
    data_p ={"app":"HYDRO",
             "platformName":"WEB",
             "platformVersion":"136",
             "deviceId":deviceId,
             "deviceName":"Chrome",
             "appVersion":app_vison}
    r = Rq.post("https://ebank.tpb.vn/gateway/api/device-presentation-service/v1/device/register",headers=headers,json=data_p)
    if r.status_code == 200:
      
      print(f"reg : {r.json()['registrationDate']}")
      return r.json()['deviceManagementId']
    return None
def _find():
    from_date , to_date = _date()
    data_post = {"pageNumber":1,
                 "pageSize":400,
                 "accountNo":os.getenv("stk"),
                 "currency":"VND",
                 "maxAcentrysrno":"",
                 "fromDate":from_date,
                 "toDate":to_date,
                 "keyword":""}
    r = Rq.post("https://ebank.tpb.vn/gateway/api/smart-search-presentation-service/v2/account-transactions/find",headers=headers,json=data_post)
    match r.status_code:
          case 200:
            data = []
            for item in  r.json()['transactionInfos']:
                if item['creditDebitIndicator'] ==  "CRDT": ## CHir Lays dataa + tien 
                    data.append(item)

            return data
          case 401:
            print("reset token ")
            login()
            return _find()
    return None

    
    


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
    

def _packet(data : dict, code : int, reg :bool = False ):
    
    match code:
        case 200:
            print("login Ok")
            if reg:
                _dologin()
            headers['authorization'] = f"Bearer {data['access_token']}"

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
    
    return _packet(r.json(),r.status_code, True if len(id)>5 else False)
