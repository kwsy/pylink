from flask import Flask, render_template, request
from db.mysql_client import PyWebsite, query_data_by_page


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'welcome'


@app.route('/py-site', methods=['GET'])
def py_site():
    page = int(request.args.get('page', 1))
    count = int(request.args.get('count', 10))
    datas, page_count = query_data_by_page(PyWebsite, page, count)
    return render_template('py_site.html',
                           py_data=datas,
                           page_count=page_count,
                           current_page=page)


if __name__ == '__main__':
    app.run(port=9001, debug=True)
