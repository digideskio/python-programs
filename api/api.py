import json
import requests
from flask import Flask, render_template, request
from flask.views import View

app = Flask(__name__)

class Home(View):
	def get_news(self, city):
		req = requests.get('http://c.api.globo.com/news/{}.json'.format(city.lower()))
		if req.status_code != 200:
			return '', req.status_code
		return json.loads(req.text), req.status_code

	def dispatch_request(self):
		city = request.args.get('city')
		news, status = self.get_news(city)
		if status == 200:
			return render_template("home.html", news=news), 200
		return render_template("error.html", status=status), status

app.add_url_rule('/news/', view_func=Home.as_view('home'))

if __name__ == '__main__':
  app.run(debug=True)