from flask import Blueprint, render_template, redirect, url_for, request, Response, jsonify
import seiya.analysis.restaurant as restaurant_

restaurant = Blueprint('restaurant', __name__, url_prefix='/restaurant')

@restaurant.route('/')
def index():
	return render_template('restaurant/index.html')

@restaurant.route('/evaluate_top10')
def evaluate_top10():
	return render_template('restaurant/evaluate_top10.html', query=restaurant_.evaluate_top10())
@restaurant.route('/evaluate_top10.json')
def evaluate_top10_json():
	return jsonify(restaurant_.evaluate_top10())
	