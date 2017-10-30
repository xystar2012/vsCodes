# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jiandan import settings  
import os,time  
import urllib.request   
from queue import Queue
from threading import Thread

class ProcessWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self._bQuit = False

    def download_link(self,path, link):
        with urllib.request.urlopen(link) as image,open(path,'wb') as f:
            f.write(image.read())

    def run(self):
        print('thread:%s starting ...'% self.name)
        while not self._bQuit:
            try:
                # Get the work from the queue
                directory, link = self.queue.get()
                print('Downloading %s Thread:%s start at %.3f' % (link,self.name, time.time()))
                self.download_link(directory, link)
                print('Downloading %s Thread:%s end at %.3f' % (link,self.name, time.time()))
                self.queue.task_done()

            except:
                print('DownLoading:%s error'% link)
                self.queue.task_done()

        print('thread:%s quitting ...'% self.name)

class JiandanPipeline(object):
    
    def __init__(self):
        # Create a queue to communicate with the worker threads
        self.queue = Queue(100)
        # Create 4 worker threads
        # 创建四个工作线程
        workers = []
        self.subPathIndex = 1
        print('config:%s  %s cntPerDir:%d' %(settings.IMAGES_STORE,settings.SUB_DIR,settings.FILECNT_PERDIR))
        for x in range(4):
            worker = ProcessWorker(self.queue)
            worker.setName(str(x+1))
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            # 将daemon设置为True将会使主线程退出，即使worker都阻塞了
            worker.daemon = True
            worker.start()
            workers.append(worker)

    def close_spider(self,spider):
        # 让主线程等待队列完成所有的任务
        for w in workers:
            self._bQuit = True
            w.join(500)
        self.queue.join()

    def process_item(self, item, spider):
        global fileIndex
        dir_path = '%s/%s/%s'%(settings.IMAGES_STORE,spider.name,settings.SUB_DIR)#存储路径  

        # iCnt = 0
        # if os.path.exists(dir_path):
        #     for i in os.scandir(dir_path):
        #         if i.is_file():                        
        #             iCnt += 1
        #     if (iCnt + self.queue.qsize()) >= settings.FILECNT_PERDIR:
        #         self.subPathIndex += 1
        #         dir_path = '%s/%s/%s%d'%(settings.IMAGES_STORE,spider.name,settings.SUB_DIR,self.subPathIndex)#存储路径
        
        if not os.path.exists(dir_path):  
            os.makedirs(dir_path) 
        print('dir_path',dir_path)   
        for image_url in item['image_urls']:  
            list_name = image_url.split('/')  
            file_name = list_name[len(list_name)-1]#图片名称 
            lastfix =  list_name[len(list_name)-2]
            # print 'filename',file_name  
            file_path = '%s/%s'%(dir_path,file_name)  
            # print 'file_path',file_path  
            image_url = image_url.replace(lastfix,'large')
            if os.path.exists(file_name) or  'static' in image_url:  
                continue
            url = image_url
            if  image_url[0:4] != 'http': 
                url = 'http:' +  image_url
            
            if self.queue.full():
                while self.queue.qsize() > 50:
                    time.sleep(1)
            self.queue.put((file_path,url))
            # with open(file_path,'wb') as file_writer: 
            #     print('downloading:',url)    
            #     conn = urllib.request.urlopen(url)#下载图片  
            #     file_writer.write(conn.read())  

        return item  
