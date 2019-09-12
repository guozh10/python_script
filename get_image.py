#!/usr/bin/env python
from commands import getoutput, getstatusoutput
import requests
from bs4 import BeautifulSoup
import re,os
def get_html(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

def get_image_dir(html):

    soup = BeautifulSoup(html, 'lxml')
    L1 = []
    for title in soup.select('a'):
        L1.append(title.get_text())
    L1.remove('../')
    L1.sort()
    return L1
def jenkins_api():
    jenkine_url = "http://10.121.223.10:8088/jenkins/job"
    job_name = "Isddc-ova-build"
    token_id="4f528ce51c948e09a93bcfc8f57a3990"
    job_token="buildWithParameters?token=password"
    curl_cmd = "curl -X GET %s/%s/%s --user guozh10:%s"%(jenkine_url,job_name,job_token,token_id)
    os.system(curl_cmd)
def get_image_file(html,get_dir,path_1,path_2):
    path = os.path.join(html,get_dir)
    url = get_html(path)
    image_addr  = get_image_dir(url)
    file_path = ''
    file_name = ''
    if not  os.path.exists(path_1):
       print "file %s not exist"%path_1
       print "create %s file"%path_1
       with open(path_1, "w") as FFF:
           FFF.write('test')
    with open(path_1,'r') as FF:
         local_file = FF.readlines()
    local_files = [' '.join([i.strip() for i in price.strip().split('\t')]) for price in local_file]
    print local_file
    for file in image_addr:
        if file.endswith('ova'):
            if file != local_files[-1]:
           	file_name = file
           	file_path = os.path.join(path,file)
            else:
                print "%s Existing"%file
                return 
    # print(file_path)
    path_dir = "/var/www/html/%s/%s"%(path_1,get_dir)
    if not os.path.exists(path_dir):
        print('create %s'%get_dir)
        os.makedirs(path_dir)
    if file_path:
        #response = requests.get(file_path)
        #with open(path_dir+"/"+file_name, 'wb') as f:
        #    f.write(response.content)
 	print("start download %s image "%file_path)
        
        status, result = getstatusoutput('wget  %s -P %s'%(file_path,path_dir))
        #status = 0
	if status ==0 :
	   print('image download success')
           images_path = '/var/www/html/%s'%path_2
           download_image = 'http://10.121.121.76/%s/%s'%(path_2,file_name)
           os.system('echo %s >%s/image_name.txt'%(download_image,path_dir))
           os.system('scp -r %s/* 10.121.121.76:%s'%(path_dir,images_path))
           os.system('rm -rf %s'%path_dir)
           with open(path_1,'w') as F:
                F.write(file_name)
           if path_2 =="images":
              print(path_2)
              jenkins_api()
if __name__ == "__main__":
  url_path  = {"images":"99.0.0","images-i":"99.0.0-i"}
  for k,v in url_path.items():
     url_joke = "http://10.241.54.4/ftp/lxco/%s/"%v
     html = get_html(url_joke)
     joke_content = get_image_dir(html)
     get_image_file(url_joke,joke_content[-1],v,k)
#  jenkins_api()
