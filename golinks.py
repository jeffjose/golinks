import hug
import simplejson as json
from urllib import parse

import falcon
import datetime

from path import Path

DB = Path('data/db.json')
data = {}


def read_db(filename):
    """
    Reads all linkdata from the file
    """
    values = json.load(filename.open('r'))
    print("Read {0} URLs".format(len(values.keys())))
    data.update(values)


def get_all_links():

    return sorted([x for x in data.values()], key = lambda x: x['created'], reverse = True)

def shortlink_exists(shortlink):

    return shortlink in data


def find(shortlink):
    """
    Searches the linkdata for the golink. Returns empty dict if not found
    """
    return data.get(shortlink, {})


def del_link(shortlink):
    """
    Removes a shortlink from the database
    """
    if shortlink in data:
        data.pop(shortlink)

    write_db(data)
    read_db(DB)


def timenow():

    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def add_link(shortlink, destination, creator):
    """
    Adds a shortlink to the database
    """
    values = {
        'shortlink': shortlink,
        'destination': destination,
        'creator': creator,
        'hits': 0,
        'created': timenow(),
        'modified': timenow(),
    }

    data[shortlink] = values

    write_db(data)
    read_db(DB)


@hug.startup()
def setup(api):
    """
    Read the database when server boots up
    """
    Path('data').mkdir_p()

    if not DB.exists():
        DB.write_lines(["{}"])

    read_db(DB)


def update_stats(link):

    link['hits'] = link.get('hits', 0) + 1
    link['modified'] = timenow()

    data[link['shortlink']] = link

    write_db(data)
    read_db(DB)


def write_db(data):
    """
    Handles writing of data to database
    """
    json.dump(data, open(DB, 'w'))


def respond_external_url(response, destination):
    """
    Use 301 to redirect regular URLs
    """

    url = parse.urlparse(destination)

    if not url.scheme:
        fulldestination = "http://%s" % destination
    else:
        fulldestination = destination

    #response.status = falcon.HTTP_301
    response.status = falcon.HTTP_302
    response.set_header('Location', fulldestination)


def respond_internal_url(response, destination):
    """
    Use javascript to redirect Internal URLs
    """

    response.content_type = falcon.MEDIA_HTML

    response.body = '''<html><head><script>window.location="http://{0}";</script></head><body>Redirecting to {0}</body></html>'''.format(
        destination)


@hug.sink('/')
def redirect_handler(request, response):
    """Main shortlink handler"""
    shortlink = request.path.lstrip('/')

    link = find(shortlink)

    body = request.stream.read()

    if request.method == 'GET' and link:
        print("Redirecting: {} -> {}".format(shortlink, link['destination']))

        if link['destination'].startswith('192.168'):
            update_stats(link)
            return respond_internal_url(response, link['destination'])
        else:
            update_stats(link)
            return respond_external_url(response, link['destination'])

    elif request.method == 'GET' and not link:
        # Trying to go link that doesnt exist yet. Give an option to create
        print("Trying to go to a link that doesnt exist yet. Here's an option to create")
        pass
    elif request.method == 'POST' and body:

        # This is adding a new shortlink
        body = json.loads(body)
        print("Setting up a new golink: {} -> {}".format(shortlink,
                                                         body['destination']))
        add_link(shortlink, body['destination'], body['creator'])
    elif request.method == 'POST' and not body:
        # Trying to create a go link with no data. Error
        print("Trying to create a go link with no data. Error")


@hug.get('/')
def frontend_handler(request, response):
    response.content_type = falcon.MEDIA_HTML
    response.body = open('dist/index.html', 'r').read()


@hug.static('/_admin')
def frontend_assets_handler():
    return ("dist/",)


@hug.get('/_api/allurls')
def api_allurls_handler(request, response, cors: hug.directives.cors = "*"):

    return get_all_links()


@hug.get('/_api/delete/{shortlink}')
def api_delete_url_handler(shortlink, request, response, cors: hug.directives.cors = "*"):

    del_link(shortlink)


@hug.post('/_api/add/{shortlink}')
def api_add_url_handler(shortlink, body, request, response, cors: hug.directives.cors = "*"):

    add_link(shortlink, body['destination'], body.get('creator', ''))

@hug.get('/_api/validate/{shortlink}')
def api_validate_shortlink_handler(shortlink, body, request, response, cors: hug.directives.cors = "*"):

    return shortlink_exists(shortlink)


# Some testing fixtures
if __name__ == '__main__':
    print(read_db(DB))
    print(find('mail'))
    print(find('foo'))
