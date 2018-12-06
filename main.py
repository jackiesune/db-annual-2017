import requests
import time
from pyquery import PyQuery as pq
import json
from multiprocessing.pool import Pool



def get_item(url):
    headers={
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.",
        "Host":"book.douban.com",
        "Referer":"https://book.douban.com/annual/2017?source=navigation"
    }
    response=requests.get(url=url,headers=headers)
    return response.json()


def parse_item(content):
    items=content.get('res').get('subjects')
    listd=[]
    if items:
        for item in items:

            bdict={}
            bdict['type']=content.get('res').get('payload').get('title')
            bdict['title']=item.get('title')
            bdict['rating']=item.get('rating')
            bdict['cover']=content.get('res').get('subject').get('cover')
            listd.append(bdict)
    else:  return 'no books'
    return listd

def write_tofile(books):
    with open('2017书籍榜单.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(books,ensure_ascii=False)+'\n')





def main(nums):
    url='https://book.douban.com/ithil_j/activity/book_annual2017/widget/'+str(nums)
    html=get_item(url)
    books=parse_item(html)
    write_tofile(books)
#    print(books)



GROUP_START=1
GROUP_END=40
if  __name__=='__main__':
    pool=Pool()
    nums=([i for i in range(GROUP_START,GROUP_END)])
    pool.map(main,nums)
    pool.close()
    pool.join()
#if __name__=='__main__':
#    for i in range(40):
#        main(i)
