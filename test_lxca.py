import requests
import json,re,sys,os

class Lxac_api(object):
   def __init__(self,ip):
      self.ip  = ip
      self.user = 'user'
      self.password = 'password'

      self.create_url = "https://%s/api/v1/connector/discovery"%self.ip
      self.get_url = "https://%s/api/v1/data/managers"%self.ip
      self.login_api = "https://" + self.ip + "/api/v1/auth/login"
   def Login(self):
       conn = requests.session()
       headers = {
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
       headers1 = {
           'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome / 63.0.3239.132Safari / 537.36'}
       login_info = {'username': self.user, 'password': self.password}

       login = conn.post(self.login_api, verify=False, data=login_info, headers=headers)
       login.encoding = 'utf-8'
       return conn, login.ok
   def Get_source(self):
      data = {}
      login = self.Login()
      if login[1] == True:
        Lxac_get_source = login[0].get(self.get_url,verify=False)
        data = json.loads(Lxac_get_source.text)
      return data,login[0]

   def API(self):
        Lxac_Data = {"lxcas":[{"ip": '10.121.116.9',"user": 'admin',"password": 'Lenovo123'}]}
        get_data = self.Get_source()
        if not get_data[0].get('result'):
            print("start create LXAC env")
            post_data =get_data[1].post(self.create_url,verify=False,data=json.dumps(Lxac_Data))
            get_data = self.Get_source()
        return get_data[0]
   def DATA(self):
       ip = ''
       build_sum = ''
       version = ''
       for data in self.API().get('result'):
           ip = data.get('ip')
           version = data.get('version')
           build_sum = data.get('build')
       file_info = """%s\n%s\n%s\n"""%(ip,version,build_sum)
       with open('lxac.txt','w') as f:
             f.write(file_info)
       return ip,version,build_sum
if __name__ == "__main__":
    ip = sys.argv[1]
    #ip = "10.121.127.11"
    v = Lxac_api(ip)
    print(v.DATA())   
