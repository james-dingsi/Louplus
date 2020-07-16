from flask import Flask, render_template, request
from ele import ele_red_packet

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def phone_number_form():
	if request.method =='POST':
		phone_number = request.form.get('phone')
		get_red_packet = ele_red_packet(phone_number)
		return render_template('index.html', phone_number=get_red_packet)
	return render_template('index.html')

'''
def phone_number_form():
	#if request.method == 'POST':
	print(request.method)
	phone_number = request.form('name', default=13606098835)
	print(request.form)
	get_red_packet = ele_red_packet(phone_number)
	return render_template('index.html', phone_number=get_red_packet)
'''

if __name__ == '__main__':
	app.run()
	#app.run(host='127.0.0.1', port=5000)
