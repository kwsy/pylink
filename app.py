from flask import Flask, render_template
from db.mysql_client import PyWebsite,Zhihu_hjf,pysite_query,zhihu_query
app = Flask(__name__,
            static_folder='static',     # 配置静态文件的文件夹
            template_folder='templates') # 配置模板文件的文件夹


@app.route('/', methods=['GET'])
def index():
    return 'welcome'

@app.route('/py-site', methods = ['GET'])
def py_site():
    datas = pysite_query(PyWebsite)
    return render_template('py_site.html', py_datas=datas)

@app.route('/zhihu-site', methods = ['GET'])
def zhihu_site():
    datas = zhihu_query(Zhihu_hjf)
    return render_template('zhihu.html', zhihu_datas=datas)

if __name__ == '__main__':
    app.run(port=9001, debug=True)