import requests
from lxml import html
import sys
import json
import os
reload(sys) 
sys.setdefaultencoding('utf8')

def parse(url):
    r=requests.get(url)
    htree = html.fromstring(r.text)
    #print htree
    dic={}
    title=htree.xpath("//h1/text()")[0]
    post=htree.xpath("//div[@id='post_content']/p/text()")
    post="\n".join(post[:-1])
    author=htree.xpath("//h5/a/text()")[0]
    dic['post']=post
    dic['title']=title
    dic['author']=author
    reply=htree.xpath("//ul/li[@class='comment']")
    contain=[]
    for item in reply:
        tmp={}
        original_author=item.xpath(".//div[@class='author author--create']//h5/a[1]/text()")
        original_post=item.xpath("./article/div[@class='post__content break-word']/p/text()")
        original_time=item.xpath("./article/div[@class='post__header']/p[@class='post__stats']/time/@datetime")
        #print original_author," ".join(original_post),original_time[0]
        tmp['reply_author']=original_author[0] if original_author else " "
        tmp['reply_content']=" ".join (original_post) 
        tmp['reply_time']=original_time[0] if original_time else " "
        print tmp
        contain.append(tmp)
        nested=item.xpath(".//li[@class='comment comment--nested']")
        for x in nested:
            tmp={}
            reply_author=x.xpath("./article//h5/a[1]/text()")
            reply_post=x.xpath(".//div[@class='post__content break-word']/p/text()")
            reply_time=x.xpath(".//time/@datetime")
            tmp['reply_author']=reply_author[0] if reply_author else " "
            tmp['reply_content']=" ".join (reply_post)
            tmp['reply_time']=reply_time[0]  if reply_time else " "
            contain.append(tmp)
    dic['reply']=contain
    return dic
seed="https://patient.info/forums/discuss/browse/abdominal-disorders-3321"
r=requests.get(seed)
htree = html.fromstring(r.text)
url_pool=[]
top_url=htree.xpath("//h3[@class='post__title']//a/@href")
url_pool=top_url[:20]
#print url_pool

for url in url_pool:
    url="https://patient.info"+url
    data=parse(url)
    filename = "Patient"+".json"
    with open(filename, "a+") as json_file:
        json.dump(data, json_file, indent = 4)
        json_file.write("\n")
        

