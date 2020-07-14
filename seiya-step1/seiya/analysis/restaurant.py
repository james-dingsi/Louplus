from flask import Blueprint, render_template, redirect, url_for, request
#from analysis.models import Job, House, Restaurant


# 创建蓝图，没有具体的url_prefix就是默认的首页('/') 
restaurant = Blueprint('restaurant', __name__, url_prefix='/restaurant')

@restaurant.route('/restaurant')
def index():
	
	return render_template('restaurant/index.html')