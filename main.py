import requests
import base64
import re
import json
from urllib import parse
import csv
import time

def CNVD_fid():
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"
    }

    #第一行写FOFA邮箱，第二行写FOFA key
    with open("config.ini","r") as config:
        email = config.readline()
        key = config.readline()

    with open("companys.txt","r", encoding='utf-8') as companys:
        for company in companys:
            word = '"'+company+'"'+'&& title="系统" && country="CN" && region!="HK" && region!="TW" && region!="MO"'
            word_base64=base64.b64encode(word.encode('utf-8')).decode("utf-8")
            url="http://fofa.info/api/v1/search/all?email="+email+"&key="+key+"&qbase64="+word_base64+"&size=1000&full=false"

            req = requests.get(url, headers=headers).text
            jsons = json.loads(req)
            # print(jsons['query'])
            web_count = req.count("[")-1
            print(f"搜索资产数：{web_count}")

            #看资产数量是否大于10，这个数值可以自己调整
            if web_count>9:
                company_result = jsons['query']
                com_res = ''.join(re.findall('[\u4e00-\u9fa5]', company_result)).replace("系统","")
                print(com_res)
                     
                keyw = '"'+com_res+'"'+'&& country="CN" && region!="HK" && region!="TW" && region!="MO" && status_code="200"'
            
                keyw_base64 = base64.b64encode(keyw.encode('utf-8')).decode("utf-8")
                keyw_url = parse.quote(keyw_base64)
                
                # 使用第二个接口搜索fid参数
                url="https://fofa.info/api/v1/search/stats?fields=fid&qbase64="+keyw_url+"&email="+email+"&key="+key
                req = requests.get(url,headers=headers).text
                jsons = json.loads(req)
                
                jsons_beaut = jsons['aggs']['fid']
                
                for i in jsons_beaut:
                    print(i)
                    #此处参数可自定义，小于500是因为数量太多有可能是apache之类的组件fid
                    if 9 < i['count'] < 500:
                        fidString="fid"+'="'+i['name']+'"'
                        fidString_base64 = base64.b64encode(fidString.encode('utf-8')).decode("utf-8")
                        url_fid="http://fofa.info/api/v1/search/all?email="+email+"&key="+key+"&qbase64="+fidString_base64+"&size=1000&full=false&fields=title"
                        time.sleep(1)
                        req_fid = requests.get(url_fid, headers=headers).text
                        jsons = json.loads(req_fid)
                        #只取前五个标题
                        titles = jsons['results'][:5]

                        #将结果写入result.csv中
                        with open('result/result.csv', 'a', newline='', encoding='utf-8') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(["fid"+'="'+i['name']+'"', com_res,titles])

                #fofa的统计聚合有冷却时间的，说是5秒一次，但是测试下来最好sleep10秒
                time.sleep(10)


if __name__ == '__main__':
    CNVD_fid()
    
