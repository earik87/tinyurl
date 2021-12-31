from flask import Flask, jsonify, json, request
from flask_restful import reqparse, abort, Api, Resource
import datetime
import time
import requests
import random
import string
import re

app = Flask(__name__)
api = Api(app)

urlList = []

@app.route('/<shortcode>', methods=['GET'])
def getUrlFromShortcode(shortcode):
    if shortcodeIsValid(shortcode) != 0 : return shortcodeIsValid(shortcode)

    for element in urlList:
        if element['shortcode'] == shortcode:
            element['redirectCount'] += 1
            currentDateTime = getCurrentTime()
            element['lastRedirect'] = currentDateTime
            return {'url': element['url']}, 302

    return "Shortcode not found", 404
 

@app.route('/shorten', methods=['POST'])
def shortenUrl():
    data = request.json
    url = data['url']
    shortcode = data['shortcode']

    if not url: 
        return "Please specify a URL.", 413
    
    if urlIsPresent(url) != 0 : return urlIsPresent(url)
    if shortcodeIsValid(shortcode) != 0 : return shortcodeIsValid(shortcode)

    for element in urlList:
        if element['url'] == url:
            return {'shortcode': element['shortcode']}, 201

    for element in urlList:
        if element['shortcode'] == shortcode:
            return "Shortcode is in use", 409 

    while True:
        if not shortcode:
            shortcode = ''.join(random.choices(string.ascii_letters+string.digits,k=6))
        for element in urlList:
            if element['shortcode'] == shortcode:
                continue
        break

    currentDateTime = getCurrentTime()
    urlList.append({'url': url, 'shortcode': shortcode,
                    'created': currentDateTime, 'lastRedirect': "", 
                    'redirectCount': 0})
    return {'shortcode': shortcode}, 201


@app.route('/<shortcode>/stats', methods=['GET'])
def urlStats(shortcode):
    if shortcodeIsValid(shortcode) != 0 : return shortcodeIsValid(shortcode)
    
    for element in urlList:
        if element['shortcode'] == shortcode:
            return { 'created': element['created'], 
                     'lastRedirect': element['lastRedirect'], 
                     'redirectCount': element['redirectCount']}, 200

    return "Shortcode not found", 404


@app.route('/', methods=['GET'])
def allUrls():
        return jsonify(urlList)


def urlIsPresent(url):

    if not urlIsValid(url):
        return "URL is not valid.", 400

    page = ''
    url_with_http = 'http://' + url 
    while page == '':
        try:
            page = requests.get(url_with_http)
            break
        except:
            time.sleep(2)
            return "URL not present.", 400
    return 0

def urlIsValid(url):
    regex = re.compile(
                r"(\w+://)?"                # protocol                      (optional)
                r"(\w+\.)?"                 # host                          (optional)
                r"((\w+)\.(\w+))"           # domain
                r"(\.\w+)*"                 # top-level domain              (optional, can have > 1)
                r"([\w\-\._\~/]*)*(?<!\.)")  # path, params, anchors, etc.   (optional)
    return re.match(regex, url) is not None

def shortcodeIsValid(shortcode):
    if shortcode:
        if len(shortcode) != 6 or not shortcode.isalnum():
            return "The provided shortcode must be made of six alphanumeric "\
                   "characters", 412
    return 0

def getCurrentTime():
    currentDateTime = datetime.datetime.utcnow()
    currentDateTime = currentDateTime.strftime('%Y-%m-%dT%H:%M:%S') + currentDateTime.strftime('.%f')[:4] + 'Z'
    return currentDateTime

if __name__ == '__main__':
    app.run(debug=True)
