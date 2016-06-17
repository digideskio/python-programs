import json
import requests
from flask import Flask, render_template

app = Flask(__name__)

def get_news(city):
	req = requests.get('http://c.api.globo.com/news/{}.json'.format(city.lower()))
	return json.loads(req.text)

@app.route('/news/<city>/')
def home(city):
	news = get_news(city)
	return render_template("home.html", news=news), 200
	
if __name__ == '__main__':
  app.run(debug=True)