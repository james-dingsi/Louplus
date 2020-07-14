from flask import Blueprint, render_template, redirect, url_for, request, Response, jsonify
import seiya.analysis.house as house_

house = Blueprint('house', __name__, url_prefix='/house')

# 租房数据分析索引页
@house.route('/')
def index():
	return render_template('house/index.html')

# 出租热门小区 Top10
@house.route('/house_top10')
def house_top10():
	return render_template('house/house_top10.html', query=house_.house_top10())
@house.route('/house_top10.json')
def house_top10_json():
	return jsonify(house_.house_top10())


# 户型分布占比统计
@house.route('/count_type')
def count_type():
	return render_template('house/count_type.html', query=house_.count_type())
@house.route('/count_type.json')
def count_type_json():
	return jsonify(house_.count_type())


# 房源面积分布统计
@house.route('/count_area')
def count_area():
	return render_template('house/count_area.html', query=house_.count_area())
@house.route('/count_area.json')
def count_area_json():
	return jsonify(house_.count_area())

# 租金最贵小区 Top10
@house.route('/rent_top10')
def rent_top10():
	return render_template('house/rent_top10.html', query=house_.rent_top10())
@house.route('/rent_top10.json')
def rent_top10_json():
	return jsonify(house_.rent_top10())

