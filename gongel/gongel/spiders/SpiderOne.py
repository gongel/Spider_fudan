import urllib.request
from urllib.parse import urljoin
import scrapy
from PIL import Image
from scrapy.http import Request,FormRequest
# class Gong(scrapy.Spider):
#     name = 'gel'
#     #url作为来的常量
#     start_urls = ['http://lab.scrapyd.cn/page/1/',
#             'http://lab.scrapyd.cn/page/2/', ]
#     '''
#     初始写法
#     def start_requests(self):
#     #url作为方法的常量
#         urls=['http://lab.scrapyd.cn/page/1/',
#             'http://lab.scrapyd.cn/page/2/',]
#         for url in urls:
#             yield scrapy.Request(url=url,callback=self.parse)
#     '''
#     def parse(self, response):
#         page =response.url.split('/')[-2]
#         filename='gel-%s.html'% page
#         with open(filename,'wb') as f:
#             f.write(response.body)
#         self.log('保存文件：%s' % filename)
#
# class Gong2(scrapy.Spider):
#     name='gel2'
#     start_urls=['http://lab.scrapyd.cn']
#     def parse(self, response):
#         one=response.css('div.quote')[2]
#         text=one.css('.text::text').extract_first()
#         print(text)
#         author=one.css('.author::text').extract_first()
#         filename='%s-语录.txt' % author
#         with open(filename,'a+') as f:
#             f.write(text)
#             f.write('\n')

#人工识别验证码，保存验证码到本地
class Gong3(scrapy.Spider):
    name='fudan'
    Headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    def start_requests(self):
        return [Request("http://yjsxk.fudan.edu.cn/wsxk",callback=self.login,meta={"cookiejar":1})]

    def login(self,response):
        picture=response.xpath("//*[@id='validateCode']/@src"   ).extract()[0]
        url="http://yjsxk.fudan.edu.cn"
        localpath="C:/Users/Administrator/Desktop/验证码.png"
        print(urljoin(url,picture))
        urllib.request.urlretrieve(urljoin(url,picture),filename=localpath)
        captcha_value=input("请输入验证码：")
        data={
            "Login.Token1":"18210240081",
            "Login.Token2":"200113",
            "verifyCode":captcha_value,
        }
        print("Login in.......................")
        return [FormRequest.from_response(response,headers=self.Headers,callback=self.crawl)]

    def crawl(self, response):
        if "验证码错误" in bytes.decode(response.body):
            print("登录失败！")
        else:
            print("登陆成功")
        print(response.url)
        return [scrapy. Request('http://yjsxk.fudan.edu.cn/wsxk/jsp/T_PYGL_KWGL_WSXK_GGKKCXX.jsp',headers=self.Headers,callback=self.praseCourse)]

    def praseCourse(self,response):
        print(response.url)


#用cookie免登陆，直达目的网址
class Gong5(scrapy.Spider):
    name="fudan2"
    Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    cookie = {
        "JSESSIONID": "0000RY47pPQsFkbBWuDWwy74sOO:1bo9j6imq"
    }
    def start_requests(self):
        return [Request("http://yjsxk.fudan.edu.cn/wsxk/jsp/T_PYGL_KWGL_WSXK_GGKKCXX.jsp",headers=self.Headers,cookies=self.cookie,callback=self.parse,)]

    def parse(self, response):
        if "验证码错误" in bytes.decode(response.body):
            print("登录失败！")
            exit(-1)
        else:
            print("登陆成功")
        print(response.url)
        print(response.text)
        print(response.xpath("//div[@align='left']//text()").re(".*中国.*"))


#人工识别验证码，保存到根目录并直接打开验证码
class Gong6(scrapy.Spider):
    name='fudan3'
    Headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    def start_requests(self):
        return [Request("http://yjsxk.fudan.edu.cn/wsxk",callback=self.login,meta={"cookiejar":1})]

    def login(self,response):
        picture=response.xpath("//*[@id='validateCode']/@src"   ).extract()[0]
        urlbase="http://yjsxk.fudan.edu.cn"
        urllib.request.urlretrieve(urljoin(urlbase,picture),'pict.png')
        img=Image.open('pict.png')
        img.show()
        captcha_value=input("请输入验证码：")
        data={
            "Login.Token1":"18210240081",
            "Login.Token2":"200113",
            "verifyCode":captcha_value,
        }
        print("Login in.......................")
        return [FormRequest.from_response(response,headers=self.Headers,callback=self.crawl)]

    def crawl(self, response):
        if "验证码错误" in bytes.decode(response.body):
            print("登录失败！")
        else:
            print("登陆成功")
        print(response.url)
        return [scrapy. Request('http://yjsxk.fudan.edu.cn/wsxk/jsp/T_PYGL_KWGL_WSXK_GGKKCXX.jsp',headers=self.Headers,callback=self.praseCourse)]

    def praseCourse(self,response):
        print(response.url)
