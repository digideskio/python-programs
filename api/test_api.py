import api
import unittest
import httpretty
import json

from flask import Flask

class ApiTestCase(unittest.TestCase):
	def setUp(self):
		self.app = api.app.test_client()
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
		httpretty.register_uri(httpretty.GET, "http://c.api.globo.com/news/rj.json", 
			body=json.dumps(self.data),
			status=200)

		home = api.Home()
		response, status = home.get_news('rj')
		self.assertEqual(status, 200)
		self.assertEqual(response, self.data)

	@httpretty.activate
	def test_get_news_not_found(self):
		httpretty.register_uri(httpretty.GET, "http://c.api.globo.com/news/rj.json", 
			body='',
			status=404)

		home = api.Home()
		response, status = home.get_news('rj')
		self.assertEqual(response, '')
		self.assertEqual(status, 404)

	@httpretty.activate
	def test_home_ok(self):
		
		httpretty.register_uri(httpretty.GET, "http://c.api.globo.com/news/rj.json", 
			body=json.dumps(self.data),
			status=200)
		response = self.app.get("/news/?city=rj")
		self.assertEqual(response.status_code, 200)
		self.assertIn("<title>Flask App</title>", response.data)

	@httpretty.activate
	def test_home_nok(self):
		
		httpretty.register_uri(httpretty.GET, "http://c.api.globo.com/news/rj.json", 
			body='',
			status=404)
		response = self.app.get("/news/?city=rj")
		self.assertEqual(response.status_code, 404)
		self.assertIn("<title>Not Found</title>", response.data)

if __name__ == '__main__':
    unittest.main()