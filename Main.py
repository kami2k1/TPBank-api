from operator import truediv
from dotenv import load_dotenv
load_dotenv()
import os
_data={
      "S":os.getenv("stk"),
      "name":os.getenv("NAME")
}
from Rq import req , sql
import sys , json
print("đã kiết nối Db ")
if not req.login():
        print("login that bai fuck ")
        sys.exit(904)
sql._load()
data = req._find()
import time
import threading
checkupda ='''
UPDATE `logs`
SET `status` = 4 
WHERE `status` = 0
  AND `time_st` <= NOW() - INTERVAL 1 HOUR;
'''
if data:
        def _start():
              while True:
               try:
     
                      qr = "SELECT * FROM `logs` WHERE `status` =0"
                      cu = sql.Kami._get_cu()
                      cu.execute(checkupda)
                      cu.execute(qr)
                      row = cu.fetchall()
                      
                      if row:
                        data = req._find()
                        if data:
                            
                            for itme in row:
                                  for i in data:
                                    try:
                                        if str(i['description']) == str(itme['d']) and int(i['amount']) == itme['amout']:
                                              print("Xác thực thành Công ! giao dịch")
                                              qr = f"UPDATE `logs` SET `status` = 1 WHERE `id` = {itme['id']}"
                                              cu.execute(qr)
                                              sql.Kami.conn.commit()
                                    except:
                                          continue
                      cu.close()
                      time.sleep(10)

               except:
                     ""
threading.Thread(target=_start).start()
from datetime import datetime ,timedelta

from flask import Flask , render_template , request , jsonify , send_from_directory , redirect
app = Flask(__name__, static_folder='static', static_url_path='')
def int_to_vnd(amount):
    return "{:,.0f}đ".format(amount).replace(",", ".")
@app.route("/pay")
def indx():
      d =request.args.get("t")
      if len(d)>2:
                     cu = sql.Kami._get_cu()
                     cu.execute(f"SELECT * FROM `logs` WHERE `d` = '{d}' AND `status`=0")
                     row =cu.fetchone()
                     if row:
                            print(row)
                            data=row
                            data['vnd'] =int_to_vnd( data['amout'])
                            print(data)
                            expire_time = data['time_st'] + timedelta(hours=1)


                            now = datetime.now()


                            s = int((expire_time - now).total_seconds())
                            print("------------ ", s)
                            data.update(_data)
                            data['ti'] = s * 1000
                            cu.close()
                            return render_template("pay4acb.html",data = data)
      return e()

@app.route("/red")

def red():
      d = request.args.get('t')
      with temp_redit_lock:
            if d not in  temp_redit:
                  return e()
                  
      
            return render_template('red.html',data=temp_redit[d])
@app.route("/e")
def e():
      return render_template('e.html')
@app.route('/<path:filename>')
def public_files(filename):
    return send_from_directory('public', filename)
## check Api key
@app.route("/api")
def _check_api():
        send = {
                "code": 99,
                "data":{}
        }
        key = request.args.get("api")
        if len(key)> 2 :
                f, d = sql._FinApi(key)
                if f:
                        send={
                                "code":0,
                                "data":d
                        }


        return jsonify(send)
import string , random
def kami_id(length=10):
    chars = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return "kami"+''.join(random.choices(chars, k=length))
@app.route("/add")
def add():

    key = request.args.get("api")
    url = request.args.get("url")
    amout = request.args.get("a")
    amout = int(amout)
    send ={
           "code":99,
           "data":{}
    }
    try:

        if len(key) >2 and len(url) > 2:
               cu = sql.Kami._get_cu()
               f , d = sql._FinApi(key)
               if f:
                       for i in range(1,9999):
                              id = kami_id()
                              cu.execute(f"SELECT * FROM `logs` WHERE `d` = '{id}'")
                              row = cu.fetchall()
                              if not row:
                                     break
                       qr = "INSERT INTO `logs` (`amout`, `api_id`, `url`,`d`) VALUES (%s, %s,%s,%s)"
                       cu.execute(qr,(amout,d['id'],url,id))

                       cu.close()
                       send = {
                              'code':0,
                              "data":{
                                     "key":id,
                                     "api_id":d['id'],
                                     "amout":amout,
                                     "url":url,
                                     "payurl":os.getenv("web")+f"/pay?t={id}"
                              }
                       }
    except:
        ""
    return jsonify(send)
                              
@app.route("/inf")
def inf():
       send ={
              "code":99,
              "data": {}
       }
       d = request.args.get("d")
       try:
              if len(d)>2:
                     cu = sql.Kami._get_cu()
                     cu.execute(f"SELECT * FROM `logs` WHERE `d` = '{d}'")
                     row =cu.fetchone()
                     if row:
                            
                            send={
                                   "code":0,
                                   "data": row
                            }
                     cu.close()        

       except Exception as e:
        
              ""     
       return jsonify(send)  
temp_redit_lock = threading.Lock()
temp_redit = {}
@app.route("/v2/gateway/action",methods=['POST'])
def ativon():
     action = request.form.get('action')
     d =  request.form.get('t')
     
     if len(d)>2:
      try:
       
       cu = sql.Kami._get_cu()
       qr = f"SELECT * FROM `logs` WHERE `d` = '{d}'"
       
       cu.execute(qr)
       row = cu.fetchone()
       
       if row:
             row['vnd'] = int_to_vnd(row['amout'])

           
             if row['status'] ==1:
                 row['e'] = False
             else:
                                              cu = sql.Kami._get_cu()
                                              qr = f"UPDATE `logs` SET `status` = 3 WHERE `id` = {row['id']}"
                                              cu.execute(qr)
                                              sql.Kami.conn.commit()
                                              cu.close()
                                              row['e'] = True

             if "e" in row:
                 with temp_redit_lock:
                       temp_redit[d] = row
                 send={
                     "status_code": 0,
                     "redirect": True,
                     "return_url":os.getenv("web")+f"/red?t={d}",
                     "returnUrl":os.getenv("web")+f"/red?t={d}",

                 }
                 return redirect(f"/red?t={d}")
             
                  

       
              

      except Exception as ez:
       print(ez)
       
       ""
     return e()
@app.route("/v2/gateway/queryProcessingTransaction",methods=['POST'])
@app.route("/v2/gateway/querySession",methods=['POST'])
def temp_v2():
    send ={
    "sessionId": "",
    "status_code": 1000,
    "redirect": False
}
    try:
       
       d = request.args.get('t')

       cu = sql.Kami._get_cu()
       
       cu.execute(f"SELECT * FROM `logs` WHERE `d` = '{d}'")
       row = cu.fetchone()
       if row:
             
             row['vnd'] = int_to_vnd(row['amout'])


             if row['status'] !=0:
                 row['e'] = True

          
                 send={
                     "status_code": 0,
                     "redirect": True,
                     "return_url":os.getenv("web")+f"/red?t={d}",
                     "returnUrl":os.getenv("web")+f"/red?t={d}",

                 }
                 with temp_redit_lock:
                     temp_redit[d] = row
                 if row['status']==1:
                  row['e'] = False

       else:
            send={
                     "status_code": 92,
                     "redirect": True,
                     "return_url":os.getenv("web")+f"/red?t={d}",
                     "returnUrl":os.getenv("web")+f"/red?t={d}",

                 }
       cu.close()
              

    except Exception as e:
        print(e)

    return send
       
if __name__ == "__main__":
        app.run(host="0.0.0.0",port=80)