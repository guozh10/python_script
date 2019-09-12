import sys,os
import json
import requests

class Harbor_api(object):
    def __init__(self,harbor_ip):
        self.harbor_ip = harbor_ip
        self.harbor_api = "http://" + self.harbor_ip + "/api/repositories"
        self.smartwarehouse = self.harbor_api + "?page=1&page8.113/api/repositories?page=1&page_size=15&project_id=13"
        self.conn = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}

    def project(self):
        pass
    def image_all(self):


        all = self.conn.get(self.smartwarehouse,headers=self.headers)

        return  all.json()
    def tag_version(self):
        tag_json = []
        for i in self.image_all():
            url = "%s/%s/tags?detail=%s" %(self.harbor_api,i.get('name'),i.get('id'))
            tag = self.conn.get(url,headers=self.headers)
            d1 = dict()
            l1 = []
            for i1 in tag.json():
                tag_name = i1.get('name')
                l1.append(tag_name)
            d1.update({i.get('name'):l1})
            tag_json.append(d1)
        # print(tag_json)
        return tag_json
    def up_to_date(self):
        tag_json = []
        data = self.tag_version()
        for tag_list in data:
            l1 = []
            for k,v in tag_list.items():
                tag_json.append(k[15:]+' '+max(v))
             #   l1.append(k+' '+max(v))
            #tag_json.append(l1)
        return tag_json
if __name__ == "__main__":
    ip = sys.argv[1]
    d = Harbor_api(ip)
    # print(d.image_all())
    d.tag_version()
    for i in d.up_to_date():
        print(i)
