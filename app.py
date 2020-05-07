from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'welcome'


@app.route('/py-site', methods=['GET'])
def py_site():
    return render_template('py_site.html')

if __name__ == '__main__':
    app.run(port=9001, debug=True)