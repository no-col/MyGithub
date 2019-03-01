#导入数据库模块
import pymysql
#导入Flask框架，这个框架可以快捷地实现了一个WSGI应用 
from flask import Flask
#默认情况下，flask在程序文件夹中的templates子文件夹中寻找模块
from flask import render_template
#导入前台请求的request模块
from flask import request   
import json
import traceback  
#传递根目录
app = Flask(__name__)
#默认路径访问登录页面
@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

#默认路径访问注册页面
@app.route('/regist', methods=['GET', 'POST'])
def regist():
    return render_template('regist.html')

#获取注册请求及处理
@app.route('/registuser', methods=['GET', 'POST'])
def getRigisfistRequest():
	#把用户名和密码注册到数据库中

	#连接数据库，此前在数据库中创建数据库customer
	db = pymysql.connect("localhost","root","usbw","customer",charset='utf8')
	#使用cursor()方法获取操作游标
	cursor = db.cursor()
	#SQL插入语句
	#sql = "INSERT INTO customer(name, password) VALUES ("+request.form.get('user')+", "+request.form.get('password')+")"
	sql = "INSERT INTO customer(name,password) VALUES('%s','%s')"%(request.form.get('user'),request.form.get('password'))
	try:
		# 执行sql语句
		cursor.execute(sql)
		# 提交到数据库执行
		db.commit()
		#注册成功之后跳转到登录页面
		return render_template('login.html')
	except:
		#抛出错误信息 
		traceback.print_exc()
		# 如果发生错误则回滚
		db.rollback()
		return '注册失败'
	# 关闭数据库连接
	db.close()

# 获取登录参数及处理
@app.route('/loginuser', methods=['GET', 'POST'])
def getLoginRequest():
# 查询用户名及密码是否匹配及存在
  #连接数据库，此前在数据库中创建数据库customer
	db = pymysql.connect("localhost","root","usbw","customer",charset='utf8')
	#使用cursor()方法获取操作游标
	cursor = db.cursor()
	# sql查询语句
	#sql = "select * from customer where name="+request.form.get('user',type=str, default=None)+" and password="+request.form.get('password',type=str, default=None)+""
	sql = "select * from customer where name = '%s' and password = '%s'"%(request.form.get('user'),request.form.get('password'))
	try:
	    #执行sql语句
		cursor.execute(sql)
		results = cursor.fetchall()
		print(len(results))
		if (len(results) == 1):
			return render_template('index.html')
		else:
			return '用户名或密码不正确'
		db.commit()
  		#提交到数据库执行
	except:
  		#如果发生错误雨则回滚
		traceback.print_exc()
		db.rollback()
	# 关闭数据库连接
	db.close()
#默认路径访问增加页面
@app.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('index.html')

#获取增添数据请求及处理
@app.route('/adduser', methods=['GET', 'POST'])
def getaddRequest():
	#把客户信息增加到数据库中

	#连接数据库，此前在数据库中创建数据库customer
	db = pymysql.connect("localhost","root","usbw","customer",charset='utf8')
	#使用cursor()方法获取操作游标
	cursor = db.cursor()
	#SQL插入语句
	#sql = "INSERT INTO customer(name, password) VALUES ("+request.form.get('user')+", "+request.form.get('password')+")"
	sql = "INSERT INTO information(id,name,telephone,address) VALUES('%s','%s','%s','%s')"%(request.form.get('id'),request.form.get('name'),request.form.get('telephone'),request.form.get('address'))
	try:
		# 执行sql语句
		cursor.execute(sql)
		# 提交到数据库执行
		db.commit()
		#增添成功之后跳转到登录页面
		return render_template('index.html')
	except:
		#抛出错误信息
		traceback.print_exc()
		# 如果发生错误则回滚
		db.rollback()
		return '增添失败'
	# 关闭数据库连接
	db.close()
 
@app.route('/query', methods=['GET', 'POST'])
def query():
    return render_template('query.html')

@app.route('/queryuser',methods=['GET','POST'])
def getqueryRequest():
	id = request.form.get('id')
	name = request.form.get('name')
	telephone = request.form.get('telephone')
	address = request.form.get('address')
	sql1 = "select * from information where id = '%s'"%id
	sql2 = "select * from information where name like '%s'"%('%'+name+'%')
	sql3 = "select * from information where telephone like '%s'"%('%'+telephone+'%')
	sql4 = "select * from information where address like '%s'"%('%'+address+'%')
	db = pymysql.connect("localhost","root","usbw","customer",charset='utf8')
	cursor = db.cursor()
	try:
		if id.strip() and name.strip() == "" and telephone.strip() == "" and address.strip() == "":
			cursor.execute(sql1)
			U = cursor.fetchall()
			db.commit()
			return render_template("show.html",u = U)
		elif id.strip() == "" and name.strip() and telephone.strip() == ""and address.strip() == "":
			cursor.execute(sql2)
			U = cursor.fetchall()
			db.commit()
			return render_template("show.html",u = U)
		elif id.strip()=="" and name.strip() == "" and telephone.strip() and address.strip() == "":
			cursor.execute(sql3)
			U = cursor.fetchall()
			db.commit()
			return render_template("show.html",u = U)
		elif id.strip() == "" and name.strip() == "" and telephone.strip() == "" and address.strip():
			cursor.execute(sql4)
			U = cursor.fetchall()
			db.commit()
			return render_template("show.html",u = U)
	except:
		#抛出错误信息
		traceback.print_exc()
		# 如果发生错误则回滚
		db.rollback()
		return '查询失败'
	db.close()



    #使用__name__ == '__main__'是Python的惯用法，确保直接执行此脚本时才能
    #启动服务器，若用其他程序调用该脚本可能父级程序会启动不同的服务器
if __name__ == '__main__':
	app.run(debug = True)