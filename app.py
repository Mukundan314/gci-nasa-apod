import os
import urllib.request
import urllib.error
import json
import datetime
from weasyprint import HTML
from flask import Flask, Response, render_template, abort

API_KEY = os.environ.get('API_KEY', 'DEMO_KEY')
API_URL = "https://api.nasa.gov/planetary/apod?date={}&api_key=" + API_KEY

app = Flask(__name__)


def apod_api(date):
    with urllib.request.urlopen(API_URL.format(date)) as res:
        return json.load(res)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<date>')
def apod_html(date):
    try:
        start = datetime.date.fromisoformat('1995-05-16')
        today = datetime.date.today()

        if start <= datetime.date.fromisoformat(date) <= today:
            data = apod_api(date)
            return render_template('apod.html',
                                   date=date,
                                   title=data['title'],
                                   explanation=data['explanation'],
                                   image=data['url'])
        else:
            abort(404)
    except (ValueError, urllib.error.HTTPError):
        abort(500)


@app.route('/<date>/pdf')
def apod_pdf(date):
    return Response(HTML(string=apod_html(date)).write_pdf(), mimetype="application/pdf")


if __name__ == "__main__":
    app.run(debug=True)
