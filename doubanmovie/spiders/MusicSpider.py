import json
import shutil
import sys
import scrapy
import re, requests

sys.path.append('D:\download\doubanmovie\doubanmovie')
from MusicItem import Music


class KuGouMusic(scrapy.Spider):
    # 爬虫唯一标识符
    name = 'KugouMusic'
    # 爬取域名
    allowed_domain = ['m.kugou.com']
    # 爬取页面地址---酷狗客户端微信分量链接
    share_url = 'http://m.kugou.com/share/?chain=1u0G07teP1&'
    # 获取音乐list链接
    music_list = 'http://m.kugou.com/schain/transfer'

    # 截取chain
    chainList = re.findall(r"chain=(.+?)&|chain=(.+?)$", share_url)
    chainSplitList = chainList[0]
    if ('' != chainSplitList[0]):
        chain = chainSplitList[0]
    pageIndex = 1;
    perPageSize = 30;
    maxPage = 1;

    musicPath = "D:\\Download\\Music\\";

    # """
    # POST http://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand=0.4768735209349304&page=0&size=20 HTTP/1.1
    # Host: gs.amac.org.cn
    # Proxy-Connection: keep-alive
    # Content-Length: 2
    # Accept: application/json, text/javascript, */*; q=0.01
    # Origin: http://gs.amac.org.cn
    # X-Requested-With: XMLHttpRequest
    # User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36
    # Content-Type: application/json
    # Referer: http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html
    # Accept-Encoding: gzip, deflate
    # Accept-Language: zh-CN,zh;q=0.9
    # """
    # headers = {
    #     "Host": "gs.amac.org.cn",
    #     "Accept": "application/json, text/javascript, */*; q=0.01",
    #     "Origin": "http://gs.amac.org.cn",
    #     "X-Requested-With": "XMLHttpRequest",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    #     "Content-Type": "application/json",
    #     "Referer": "http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html",
    #     "Accept-Language": "zh-CN,zh;q=0.9",
    # }

    def start_requests(self):
        if ('' == self.chain):
            print("未获取到分享的chain")
            return
        yield scrapy.Request(
            self.music_list + "?chain=" + self.chain + "&page=" + str(self.pageIndex) + '&pagesize=' + str(
                self.perPageSize),
            method="POST",
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        print(response.text)
        result = json.loads(response.text)
        if (0 != result['errcode']):
            return

        resultInfo = result['info']
        maxPage = resultInfo['count'] // self.perPageSize + 1

        musicList = resultInfo["list"]
        for item in musicList:
            musicName = item["filename"]
            musicHash = item["hash"]
            hashUrl = "http://www.kugou.com/yy/index.php?r=play/getdata&hash=" + musicHash
            hashCotent = requests.get(hashUrl).text
            musicUrl = re.findall('"play_url":"(.*?)"', hashCotent)
            musicUrl = ''.join(musicUrl)
            downloadUrl = musicUrl.replace("\\", "")
            print("下载地址：" + downloadUrl)
            if ('' != downloadUrl):
                with open(self.musicPath + musicName + ".mp3", "wb") as fp:
                    fp.write(requests.get(downloadUrl).content)
                    print(musicName + "下载成功")
            else:
                print("下载失败：" + musicName)
            if (self.pageIndex < maxPage):
                self.pageIndex = self.pageIndex + 1
                yield scrapy.Request(
                    self.music_list + "?chain=" + self.chain + "&page=" + str(self.pageIndex) + '&pagesize=' + str(
                        self.perPageSize),
                    method="POST",
                    callback=self.parse,
                    dont_filter=True
                )
