import json
from cgi import log

import pymysql

import settings


# 存到文件
# class MoviePipeline(object):
#     def __init__(self):
#         # 打开文件
#         self.file = open('data.json', 'w', encoding='utf-8')
#     # 该方法用于处理数据
#     def process_item(self, item, spider):
#         # 读取item中的数据
#         line = json.dumps(dict(item), ensure_ascii=False) + "\n"
#         # 写入文件
#         self.file.write(line)
#         # 返回item
#         return item
#     # 该方法在spider被开启时被调用。
#     def open_spider(self, spider):
#         pass
#     # 该方法在spider被关闭时被调用。
#     def close_spider(self, spider):
#         self.file.close()

# 存到数据库
class DBPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor();

    def process_item(self, item, spider):
        try:
            # 查重处理
            self.cursor.execute("""select * from doubanmovie where img_url = %s""", item['img_url'])
            # 是否有重复数据
            repetition = self.cursor.fetchone()

            # 重复
            if repetition:
                # 应该更新数据
                self.cursor.execute("""update doubanmovie set movie_url = %s where img_url= %s""", (item['movie_url'],
                                    item['img_url']))
                pass
            else:
                # 插入数据
                self.cursor.execute(
                    """insert into doubanmovie(name, info, rating, num ,quote, img_url,movie_url)
                    value (%s, %s, %s, %s, %s, %s,%s)""",
                    (item['name'],
                     item['info'],
                     item['rating'],
                     item['num'],
                     item['quote'],
                     item['img_url'],
                     item['movie_url']))
            # 提交sql语句
            self.connect.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            log(error)
        return item
