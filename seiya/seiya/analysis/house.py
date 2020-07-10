from flask import Blueprint, render_template, redirect, url_for, request
#from analysis.models import Job, House, Restaurant


# 创建蓝图，没有具体的url_prefix就是默认的首页('/') 
house = Blueprint('house', __name__, url_prefix='/house')

@house.route('/house')
def index():
	
	return render_template('house/index.html')