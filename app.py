from flask import Flask, render_template

app = Flask(__name__)
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


if __name__ == "__main__":
    app.run()
