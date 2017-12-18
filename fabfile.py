# -*- coding: utf-8 -*-
from fabric.api import env,run
from fabric.operations import sudo
#git仓库名
GIT_REPO = 'git@github.com:YannisYao/DjangoBlog.git'

env.user = 'yannis'
#env.password = ''
env.key_filename = '~/.ssh/id_rsa'
#服务器主机对应的域名
env.hosts = ['www.yanniszone.com']

#一般情况下为22端口，如果非22端口请看服务器ssh端口配置
env.port = '22'

def deploy():
	#app的工作目录
	source_folder = '/home/yannis/sites/www.yanniszone.com/DjangoBlog'
	#cd 到工作目录，更新项目
	run('cd %s && git pull' % source_folder)
	#1.安装第三方依赖
	#2.收集静态文件
	#3.生成数据库
	run("""
		cd {} &&
		../env/bin/pip install -r  requirements.txt &&
		../env/bin/python3 manage.py collectstatic --noinput &&
		../env/bin/python3 manage.py migrate
		""".format(source_folder))
	#重启Gunicorn
	sudo('systemctl restart yannis')
	#重启nginx
	sudo('service nginx restart')



