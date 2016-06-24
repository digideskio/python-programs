import json
import requests
from flask import Flask, render_template, request, redirect, url_for
from flask.views import View
from flask.views import MethodView

app = Flask(__name__)

buffer = {}


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
            return render_template("home.html", news=news, comentarios=buffer.get(city, ''), city=city), 200
        return render_template("error.html", status=status), status


class AddComentario(MethodView):

    def post(self):
        city = request.args.get('city')
        text = request.form['comentario']
        buffer.setdefault(city, []).append(text)
        return redirect(url_for('home', city=city))


class RemComentario(MethodView):

    def post(self):
        city = request.args.get('city')
        text = request.args.get('comentario')
        buffer.get(city, []).remove(text)
        return redirect(url_for('home', city=city))

app.add_url_rule('/news/', view_func=Home.as_view('home'))
app.add_url_rule('/comentar/', view_func=AddComentario.as_view('comentario'))
app.add_url_rule('/remover/', view_func=RemComentario.as_view('remove'))

if __name__ == '__main__':
    app.run(debug=True)
