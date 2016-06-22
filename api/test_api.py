import api
import unittest
import httpretty
import json

from flask import Flask, url_for

class HomeTestCase(unittest.TestCase):
	def setUp(self):
		self.app = api.app.test_client()
		self.city = 'rj'
		self.data = [
			{
				"subtitulo": "sub1", 
				"titulo": "tit1", 
				"url": "url1" 
			},
			{
				"subtitulo": "sub2", 
				"titulo": "tit2", 
				"url": "url2"
			}
		]

	def tearDown(self):
		pass

	@httpretty.activate
	def test_get_news_ok(self):
		httpretty.register_uri(httpretty.GET, "http://c.api.globo.com/news/{}.json".format(self.city), 
			body=json.dumps(self.data),
			status=200)

		home = api.Home()
		response, status = home.get_news(self.city)
		self.assertEqual(status, 200)
		self.assertEqual(response, self.data)

	@httpretty.activate
	def test_get_news_not_found(self):
		httpretty.register_uri(httpretty.GET, "http://c.api.globo.com/news/{}.json".format(self.city), 
			body='',
			status=404)

		home = api.Home()
		response, status = home.get_news(self.city)
		self.assertEqual(response, '')
		self.assertEqual(status, 404)

	@httpretty.activate
	def test_home_ok(self):
		httpretty.register_uri(httpretty.GET, "http://c.api.globo.com/news/{}.json".format(self.city), 
			body=json.dumps(self.data),
			status=200)
		response = self.app.get("/news/?city={}".format(self.city))
		self.assertEqual(response.status_code, 200)
		self.assertIn("<title>Flask App</title>", response.data)

	@httpretty.activate
	def test_home_nok(self):
		httpretty.register_uri(httpretty.GET, "http://c.api.globo.com/news/{}.json".format(self.city), 
			body='',
			status=404)
		response = self.app.get("/news/?city={}".format(self.city))
		self.assertEqual(response.status_code, 404)
		self.assertIn("<title>Not Found</title>", response.data)


class ComentarioTestCase(unittest.TestCase):
	def setUp(self):
		self.city = 'rj'
		self.app = api.app.test_client()

	def tearDown(self):
		api.buffer = {}

	def test_add_comentario(self):
		response = self.app.post(
			"/comentar/?city={}".format(self.city),
			data={"comentario": "tt"}
		)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.location, 'http://localhost/news/?city={}'.format(self.city))
		self.assertEqual(api.buffer, {"rj": ["tt"]})

	def test_remove_comentario(self):
		api.buffer[self.city] = ['tt', 'te']
		response = self.app.post(
			"/remover/?city={}&comentario={}".format(self.city, "tt")
		)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.location, 'http://localhost/news/?city={}'.format(self.city))
		self.assertEqual(api.buffer, {"rj": ['te']})


if __name__ == '__main__':
    unittest.main()