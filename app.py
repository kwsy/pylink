from flask import Flask, render_template
from db.mysql_client import PyWebsite, Csdn, Zhihu, query_data

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'welcome'


@app.route('/py-site', methods=['GET'])
def py_site():
    datas = query_data(PyWebsite)
    return render_template('py_site.html', py_data=datas)

@app.route('/csdn', methods=['GET'])
def csdn():
    datas = query_data(Csdn)
    return render_template('csdn.html', py_data=datas)

if __name__ == '__main__':
    app.run(port=9001, debug=True)