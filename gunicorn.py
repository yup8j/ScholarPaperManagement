import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

bind = '127.0.0.1:8000'  # 绑定ip和端口号
backlog = 512  # 监听队列
timeout = 600  # 超时
worker_class = 'sync'  # 使用sync模式
chdir = '/root/ScholarPaperManagement'
workers = 1  # 进程数
threads = 2  # 指定每个进程开启的线程数
loglevel = 'info'  # 日志级别
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'  # gunicorn访问日志格式
