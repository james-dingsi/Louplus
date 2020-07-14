from flask import Blueprint, render_template, redirect, url_for, request, Response, jsonify
import seiya.analysis.job as job_

job = Blueprint('job', __name__, url_prefix='/job')

# 拉钩网职位数据分析
@job.route('/')
def index():
	return render_template('job/index.html')

# 职位最多城市 Top10
@job.route('/count_top10')
def count_top10():
	return render_template('job/count_top10.html', query=job_.count_top10())

# 薪资排名城市 Top10
@job.route('/salary_top10')
def salary_top10():
	return render_template('job/salary_top10.html', query=job_.salary_top10())

# 排名前十的热门标签
@job.route('/hot_tags')
def hot_tags():
	return render_template('job/hot_tags.html', query=job_.hot_tags())

# 排名前十的热门标签生成图片
@job.route('/hot_tags.png')
def hot_tags_plot():
	# Response将数据直接发送给浏览器，无需前端模板
	# 使用函数将图片发送给浏览器，并指定类型为png的图片
	return Response(job_.hot_tags_plot(), content_type='image/png')

# 排名前十的热门标签数据转换为JSON
@job.route('/hot_tags.json')
def hot_tags_json():
	#d = {key: int(value) for key, value in job_.hot_tags().to_dict().items}
	return jsonify(job_.hot_tags())

# 工作经验统计
@job.route('/experience_stat')
def experience_stat():
	return render_template('job/experience_stat.html', query=job_.experience_stat())

@job.route('/experience_stat.json')
def experiece_stat_json():
	return jsonify(job_.experience_stat())

# 学历要求统计
@job.route('/education_stat')
def education_stat():
	return render_template('job/education_stat.html', query=job_.education_stat())

@job.route('/education_stat.json')
def education_stat_json():
	return jsonify(job_.education_stat())

@job.route('/salary_education')
def salary_education():
	return render_template('job/salary_education.html', query=job_.salary_education())

@job.route('/salary_education.json')
def salary_education_json():
	return jsonify(job_.salary_education())
