import requests
from lxml import etree
import os
import time


def coffee_dou_requests_1(m,u,i,p,j):
    start = time.time()
    a = float(0)
    for mima in range(5):
        if m == 'qazplm75124':
            break
        else:
            print("密码错误")
            exit('')
    for c in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
              '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33']:
        url = u
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }
        b = '.jpg'

        response = requests.get(url=url, headers=headers)
        page_text = response.text
        tree = etree.HTML(page_text)
        li_list = tree.xpath(i)
        if not os.path.exists(f'./{p}'):
            os.mkdir(f'./{p}')
        for li in li_list:
            a = a+1
            u = li.xpath(f'{j}')[0]
            img_name = (f'{a}+{b}')
            # img_name = img_name.encode('iso-8859-1').decode('gbk')
            img_data = requests.get(url=u, headers=headers).content
            img_path = f'{p}/' + img_name
            with open(img_path, 'wb') as fp:
                fp.write(img_data)
            print(img_name, u, '爬取完毕！！')
            end = time.time()
            print('总耗时:', end - start)
    print("爬取结束！！！")
    return a

def coffee_dou_requests_2(m,u,i,p,j,l):
    start = time.time()
    a = float(0)
    for mima in range(5):
        if m == 'qazplm75124':
            break
        else:
            print("密码错误")
            exit('')
    for c in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
              '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33']:
        url = u
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }
        b = '.jpg'
        response = requests.get(url=url, headers=headers)
        page_text = response.text
        tree = etree.HTML(page_text)
        li_list = tree.xpath(i)
        if not os.path.exists(f'./{p}'):
            os.mkdir(f'./{p}')
        for li in li_list:
            a = a+1
            u = l+li.xpath(f'{j}')[0]
            img_name = (f'{a}+{b}')
            # img_name = img_name.encode('iso-8859-1').decode('gbk')
            img_data = requests.get(url=u, headers=headers).content
            img_path = f'{p}/' + img_name
            with open(img_path, 'wb') as fp:
                fp.write(img_data)
            print(img_name, u, '爬取完毕！！')
            end = time.time()
            print('总耗时:', end - start)
    print("爬取结束！！！")
    return a
#u为url
#i为宏观位置
#p为文件名称
#j为具体位置


#使用本程序代表接受以下条款：
#声明：
#本模块完全由作者开发，无借鉴任何帖子
#模块解释所有权归作者所有
#若使用者使用本模块有关违法的行为，并造成严重后果的，作者均不承担相应的法律责任
#感谢您下载此模块，希望能带来美好的体验
#如有打赏，请联系作者
#如有需求，请联系作者
#如有bug或无法使用，请联系作者
#作者邮箱：1666285441@qq.com
#无作者允许，禁止转发或盗用此代码
#如有违反以上原则，作者将交到公安机关，并依法处理
#由于学业繁忙，周一~周五不提供更新服务
#使用模块前请下载requests,lxml模块
#要问作者为什么模块叫咖啡豆请求，因为咖啡豆为作者外号，且作者朋友为此编了个故事集，有兴趣请联系： 3024928063qq.com（jonexi）


#提供以下测试代码使用：
'''
from coffee_dou_requests_package import coffee_dou_requests
#import asyncio
#u=input("请输入url或url格式:")
#i=input("请输入宏观位置(类型为xpath)：")
#p=input("请输入文件名称：")
#j=input("请输入爬取内容具体位置(类型为xpath)：")
m=input("请输密码:")



u = 'https://www.xmqmnet.com/meinvtupian/' + 'index-' + '2' + '.html'
i = '//div[@class="main"]/div[2]/ul/li'
p = "图片"
j = './div/a/img/@src'
u = coffee_dou_requests(m, u, i, p, j)
print(u)


#密码为：qazplm75124

'''