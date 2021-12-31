from application import app
from flask import json

class TestClass:
    def testShortenUrl(self):        
        response = app.test_client().post(
            '/shorten',
            data=json.dumps({'url': "www.facebook.com",
                             'shortcode': "abc123"}),
            content_type='application/json')

        data = json.loads(response.get_data(as_text=True))
        
        assert response.status_code == 201
        assert data['shortcode'] == "abc123"

    def testGetUrlFromShortcode(self):
        response = app.test_client().get('/abc123')
        
        data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 302
        assert data['url'] == "www.facebook.com"

    def testUrlStats(self):
        response = app.test_client().get('/abc123/stats')
        
        data = json.loads(response.get_data(as_text=True))

        assert response.status_code == 200
        assert len(data) == 3
        assert data['redirectCount'] == 1

    def testGetUrlFromWrongShortcode(self):
        response = app.test_client().get('/abc456')
        
        data = response.get_data(as_text=True)

        assert response.status_code == 404
        assert data == "Shortcode not found"

    def testShortenUrlWithUsedShortcode(self):
        response = app.test_client().post(
            '/shorten',
            data=json.dumps({'url': "www.apple.com",
                             'shortcode': "abc123"}),
            content_type='application/json')

        data = response.get_data(as_text=True)
        
        assert response.status_code == 409
        assert data == "Shortcode is in use"

    def testShortenUrlWithInvalidShortcode(self):
        response = app.test_client().post(
            '/shorten',
            data=json.dumps({'url': "www.apple.com",
                             'shortcode': "abc1234"}),
            content_type='application/json')

        data = response.get_data(as_text=True)
        
        assert response.status_code == 412
        assert data == "The provided shortcode must be made of six alphanumeric characters"
