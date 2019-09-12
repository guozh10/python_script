import requests
import json,re,sys
class Verification_Platform(object):
    def __init__(self,ipaddress,username,passwd):
        self.Sum    =   10
        self.url    =   ipaddress
        self.username   =  username
        self.passwd     =   passwd
        self.event_api  = "https://" + self.url +"/api/v1/inbound/events?offset=0&limit=0&sortField=&sortMode="
        self.login_api  = "https://" + self.url + "/api/v1/auth/login"
    def Login(self,Passwd):
        conn = requests.session()
        headerss = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        headers1 = {'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome / 63.0.3239.132Safari / 537.36'}
        login_info = {'username': self.username, 'password': Passwd}

        login = conn.post(self.login_api, verify=False, data=login_info, headers=headerss)
        login.encoding = 'utf-8'
        return conn,login.ok
    def Evnet(self,login_api):
        successful = 0
        failed = 0
        Warning = 0
        Data = []
        if login_api[1]:
            login = login_api[0].get(self.event_api, verify=False)
            data_dist = json.loads(login.text)
            if not data_dist.get('message'):
               for evnet_data in data_dist.get('result'):
                   Data.append(evnet_data)

                   v  = evnet_data.get("msg")
                   if v != None:
                       status = re.findall('successful|failed|unsuccessful', v)
                       if status:
                         if  status[0] == "successful":
                             successful += 1
                         elif status[0] == "failed" or status[0] == "unsuccessful":
                             failed += 1
                    #elif status[0] == "unsuccessful":
                    #    Warning += 1
                         else:
                             Warning += 1


        successful_status = "successful: %s "%successful
        failed_status = "failed: %s "%failed
        Warning_status = "Warning: %s "%Warning
        return Data,successful_status,failed_status,Warning_status
    def Data(self):
          for Sum in range(self.Sum):
              login = self.Login(self.passwd)
              print("login web SUM ",Sum)
              if Sum == 5:
                  login = self.Login("password")
                  data = self.Evnet(login)
                  total = len(data[0])
                  
                  total_info = """login_total: %s\n%s\n%s\n%s """ %(total,data[1],data[2],data[3])
                  with open('file.txt','w') as F:
                      F.write(total_info)
                  print total_info
                 
                  # for i in data[]:
                  #     print(i)
                  break




if __name__ == "__main__":
    ip = sys.argv[1]
    username = sys.argv[2]
    passwd = sys.argv[3]
    v = Verification_Platform(ip,username,passwd)
    v.Data()
