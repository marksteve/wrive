from cachecore import RedisCache
from flask import Flask, abort, render_template
import requests
import json


DRIVE_GET_URL = 'https://www.googleapis.com/drive/v2/files/%s?key=%s'


app = Flask(__name__)
app.config.from_object('wrive.settings')


if app.config.get('SIMPLE_API_ACCESS_KEY') is None:
    raise KeyError("SIMPLE_API_ACCESS_KEY is not set!")


cache = RedisCache(host=app.config['REDIS_HOST'],
                   port=app.config['REDIS_PORT'],
                   key_prefix=app.config['REDIS_KEY_PREFIX'])


@app.route('/')
@app.route('/<file_id>')
def index(file_id=None):
    if file_id is None:
        return render_template('index.html')

    # Get doc metadata
    # TODO: Check if valid drive doc
    r = requests.get(DRIVE_GET_URL %
                     (file_id, app.config['SIMPLE_API_ACCESS_KEY']))
    if not r.ok:
        # r.reason
        abort(r.status_code)
    doc = json.loads(r.content)
    modified_date = doc.get('modifiedDate')

    # Try to get cached copy
    cache_key = '%s.%s' % (file_id, modified_date)
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response

    # Else retrieve doc
    r = requests.get(doc['exportLinks']['text/html'] + '&key=' +
                     app.config['SIMPLE_API_ACCESS_KEY'])
    if not r.ok:
        # r.reason
        abort(r.status_code)

    # Store doc content in cache
    cache.set(cache_key, r.content)

    return r.content
