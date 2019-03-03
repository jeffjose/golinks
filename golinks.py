import hug
import simplejson as json

import falcon

from path import Path

DB = Path('data/db.json')
data = {}


def read_db(filename):
    """
    Reads all linkdata from the file
    """
    return json.load(filename.open('r'))


def find(shortlink):
    """
    Searches the linkdata for the golink. Returns empty dict if not found
    """
    return data.get(shortlink, {})


def add_link(shortlink, destination, creator):
    """
    Adds a shortlink to the database
    """
    values = {
        'shortlink': shortlink,
        'destination': destination,
        'creator': creator
    }

    data[shortlink] = values

    write_db(data)


@hug.startup()
def setup(api):
    """
    Read the database when server boots up
    """
    Path('data').mkdir_p()

    if not DB.exists():
        DB.write_lines(["{}"])

    data.update(read_db(DB))


def write_db(data):
    """
    Handles writing of data to database
    """
    json.dump(data, open(DB, 'w'))


def respond_external_url(response, destination):
    """
    Use 301 to redirect regular URLs
    """

    #response.status = falcon.HTTP_301
    response.status = falcon.HTTP_302
    response.set_header('Location', destination)


def respond_internal_url(response, destination):
    """
    Use javascript to redirect Internal URLs
    """

    response.content_type = falcon.MEDIA_HTML

    response.body = '''<html><head><script>window.location="http://{0}";</script></head><body>Redirecting to {0}</body></html>'''.format(
        destination)

@hug.sink('/')
def handle(request, response):
    """Main shortlink handler"""
    shortlink = request.path.lstrip('/')

    link = find(shortlink)

    body = request.stream.read()

    if request.method == 'GET' and link:
        print("Redirecting: {} -> {}".format(shortlink, link['destination']))

        if link['destination'].startswith('192.168'):
            return respond_internal_url(response, link['destination'])
        else:
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

@hug.static('/_admin')
def admin_handler():
    return ("dist",)

# Some testing fixtures
if __name__ == '__main__':
    print(read_db(DB))
    print(find('mail'))
    print(find('foo'))
