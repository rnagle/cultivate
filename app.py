import os

from flask import Flask, render_template, request

app = Flask(__name__)

if os.environ.get('DEPLOYMENT_TARGET', False) == 'production':
    app.config.from_object('config.ProdConfig')
else:
    app.config.from_object('config.Config')

@app.route('/')
def home():
    return render_template('home.html', **{'content': 'Cultivate!'})


@app.route('/results')
def results():
    return render_template('results.html', **{'content': 'Results!'})


@app.route('/person/<identifier>')
def person(identifier):
    return render_template('home.html', **{'content': 'Person!'})


@app.route('/search', methods=['POST'])
def search():
    """
    TODO:
    - search for stuff on twitter
    - figure out who's included and rank them
    - return json to build results list
    """
    query = dict(request.form)
    return '{"success": true}'


port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(port=port, host='0.0.0.0')
