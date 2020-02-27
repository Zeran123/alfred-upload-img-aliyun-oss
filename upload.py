#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import os
import sys
import atexit
import uuid
from subprocess import call
from os.path import expanduser, exists, basename, getsize
from workflow import Workflow3

def capture():
    file_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_'+str(uuid.uuid1())[0:8]+'.png')
    file_path = os.path.join('/tmp/', file_name)
    atexit.register(lambda x: os.remove(x) if os.path.exists(x) else None, file_path)
    save = call(['./pngpaste', file_path])
    if save == 1:
        # Quit job if no image found in clipboard
        print('No image found in clipboard')
        sys.exit()
    return file_path, file_name

def main(wf):
		import oss2
		file_path, file_name = capture()
		# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
		auth = oss2.Auth(os.getenv('access_key'), os.getenv('secret_key'))
		# Endpoint以杭州为例，其它Region请按实际情况填写。
		bucket = oss2.Bucket(auth, 'https://oss-cn-'+os.getenv('region')+'.aliyuncs.com', os.getenv('bucket_name'))

		# 上传文件
		# 如果需要上传文件时设置文件存储类型与访问权限，请在put_object中设置相关headers, 参考如下。
		# headers = dict()
		# headers["x-oss-storage-class"] = "Standard"
		# headers["x-oss-object-acl"] = oss2.OBJECT_ACL_PRIVATE
		# result = bucket.put_object('<yourObjectName>', 'content of object', headers=headers)
		result = bucket.put_object_from_file(os.getenv('folder') + '/' + file_name, file_path)

		if result.status == 200:
			output = "%s/%s" %(os.getenv('bucket_uri'), file_name)
			print(output,end='')
		else:
		# HTTP返回码。
			print('error: httpCode='+result.status,end='')
		# 请求ID。请求ID是请求的唯一标识，强烈建议在程序日志中添加此参数。
		# print('request_id: {0}'.format(result.request_id))
		# ETag是put_object方法返回值特有的属性。
		# print('ETag: {0}'.format(result.etag))
		# HTTP响应头部。
		# print('date: {0}'.format(result.headers['date']))

if __name__ == '__main__':
    wf = Workflow3(libraries=['./lib'])
    sys.exit(wf.run(main))