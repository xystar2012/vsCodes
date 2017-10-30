# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class DoubanMoviePipeline(object):
    def __init__(self):
            self.conn = pymysql.connect(
                                      user='root',            
                                      password= '123123',
                                      host='10.10.10.211',
                                      db='movie',
                                      charset='utf8'
                                      )
            self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        
        if item['no'] is None:
            return item

        try:

            sql = "select * from movie250 where no = '{}'".format(item['no'])
            self.cursor.execute(sql)
            
            if self.cursor.fetchone() is None:
                sql = """insert into movie250(no,movie_name,director,writer,actor,type,region,language,date,length,another_name,introduction,grade,comment_times) 
                                        values("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")"""
            else:
                sql = """update movie250 set movie_name = "{1}",director = "{2}",writer = "{3}",actor = "{4}",type = "{5}",region = "{6}",
                language = "{7}",date = "{8}",length = "{9}",another_name = "{10}",introduction = "{11}",grade = "{12}",comment_times = "{13}"
                WHERE no = "{0}" """ 
                                        
            sql = sql.format (      item['no'],
                                    item['movie_name'],
                                    item['director'],
                                    item['writer'],
                                    item['actor'],
                                    item['type'],
                                    item['region'],
                                    item['language'],
                                    item['date'],
                                    item['length'],
                                    item['another_name'],
                                    item['introduction'],
                                    item['grade'],
                                    item['comment_times']
                                     )
                        
            # print(sql)
            self.cursor.execute(sql)
            self.conn.commit()       
        except Exception as e:
            print(e)
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
