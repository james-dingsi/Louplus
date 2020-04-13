#!/usr/bin/env python3
import os
from flask import Flask, render_template, url_for, redirect, request, json

app = Flask(__name__)

news_dict = {}
path_json = "/home/shiyanlou/files"

@app.route('/')
def index():
    for n in os.listdir(path_json):    # serch files name
        with open(path_json + '/' + n) as f:    # open the files
            filememo = json.load(f)    # save to filememo
            news_dict[n.split('.')[0]] = [filememo.get('title'), 
                    filememo.get('created_time'), filememo.get('content')]
    return render_template('index.html', news_dict=news_dict)

@app.errorhandler(400)
def not_found(error):
    return render_template('404.html')

@app.route('/files/<filename>')
def files(filename):
    if filename+'.json' in os.listdir(path_json):
        news_title, news_ct, news_content = news_dict.get(filename)
        return render_template('file.html', filename=filename, title=news_title, 
                ct=news_ct, content=news_content)
    return render_template('404.html')
'''
    try:
        with open(path_json + '/' + name_json) as f:
            newsfiles = json.load(f)
            
            return json.dump(newsfiles)
    except IOError:
'''

if __name__ == '__main__':
    app.run()
