import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

config = {
    'user':os.getenv("user_db") ,
    'password': os.getenv("passdb"),
    'host': os.getenv("host"),
    'database':  os.getenv("db"),
    'raise_on_warnings': True
}

class Db:
   def __init__(self):
       self.conn = None
       self.reh = False
       self._login()
   def _login(self):

        try:

        
            self.conn = mysql.connector.connect(
                # host="127.0.0.1",
                # user="root",
                # password="",
                # database="tranhs"
                **config
            )
           
            if self.conn.is_connected():
                print("bat auto commit")
                self.conn.autocommit = True
        except mysql.connector.errors.ProgrammingError as e:
            print(f"Lỗi kết nối DB (ProgrammingError): {e}")
        except Exception as e:
            print(f"Lỗi kết nối DB: {e}")
   def _commit(self):
       if self.conn:
           self.conn.commit()
   def _get_cu(self):
   
        """Lấy một con trỏ từ hàng đợi hoặc tạo mới nếu hết con trỏ."""
        try:
                self.conn.cursor(dictionary=True,buffered=True).execute("SELECT 1") 

                if self.conn is None or not self.conn.is_connected():
                    print("🔄 Kết nối lại MySQL...")
                    if not self.reh:
                         self.reh = True
                         self._login()
                if self.conn: 
                    self.conn.commit()
                    return self.conn.cursor(dictionary=True,buffered=True)
        except:
         ""
        self.reh = False
        return None
print("0")
try:
   Kami = Db()
except Exception as e:
    print(e)

print("1")
import threading
Api_key = threading.Lock() ## lock tranh dddos
Data_apikey = []

def _loadApikey(key :str = ""):
    data = []
    cu = Kami._get_cu()
    if len(key) > 2:
        sql = f"SELECT * FROM api WHERE `key` = '{key}'"
        cu.execute(sql)
        row = cu.fetchone()
        if row:
           
            data.append(row)
      
          

    else:
        sql= "SELECT * FROM api"
        cu.execute(sql)
        row = cu.fetchall()
        if row:
            data +=row
    if len(data)>=1:
     
        return True , data
    else:
        return False , None
def _FinApi(Key : str):
   global Data_apikey
   try: 
    with Api_key:
        for item in Data_apikey:
            if item['key'] == Key:
              return True , item
        f , d = _loadApikey(Key)
        if f:
          
            Data_apikey +=d
            return True , d[0]
        else:
          
            return False , None
   except Exception as e:
 
    ""
   
    return False , None
def _load():
    global Data_apikey
    f , d = _loadApikey()
    if f :
        Data_apikey +=d


    



    