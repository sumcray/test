from flask import render_template,request,jsonify
#导入蓝本 main
from . import main
from app.main.spider import court
from app.main import global_values

global_values._init()


@main.route('/spider', methods=['GET', 'POST'])
def spider():
    return render_template('find.html')

@main.route('/summernote')
def summernote():
    return render_template('/summernote.html')

@main.route('/login')
def login():
    return render_template('/login2.html')

@main.route('/manage')
def manage():
    return render_template('/manage.html')

@main.route('/result',methods=['GET'])
def result():
    str=request.args.get('key')
    # global_values.set_value(str)
    # return court.run(str)
    return render_template('/result.html',json_data=court.run(str))
