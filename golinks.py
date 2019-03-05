import hug
import simplejson as json
from urllib import parse
import copy

import falcon
import datetime

from path import Path

STATSPATH = Path('data/stats')
ALIASESPATH = Path('data/aliases')
data = {}


def is_internal(url):

    return url.startswith('192.168') or url.startswith('10.') or url.startswith('172.')


def read_db(aliases=ALIASESPATH, stats=STATSPATH):
    """
    Reads all linkdata from the file
    """
    statsvalues = json.load(stats.open('r'))

    aliasesheaders = ['shortlink', 'destination']
    # Convert the following format into server format
    # Input
    #   g google.com
    #
    # Output
    #  [{'shortlink': 'g', 'destination': 'google.com'}]
    #
    aliasesvalues = [
        dict(zip(aliasesheaders, x.split()))
        for x in aliases.lines(retain=False)
    ]

    values = {}
    for aliases in aliasesvalues:

        shortlink = aliases['shortlink']

        values[shortlink] = aliases

        aliases.update(statsvalues.get(shortlink, {}))

    print("Read {0} URLs".format(len(values.keys())))
    data.update(values)


def get_all_links():

    return sorted([x for x in data.values()],
                  key=lambda x: x.get('created', timenow()),
                  reverse=True)


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
    read_db()


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
    read_db()


def edit_link(shortlink, values):
    """
    Edits a shortlink to the database
    """

    origvalues = data.pop(values['origshortlink'])
    origvalues['shortlink'] = shortlink
    origvalues['destination'] = values['destination']

    # remove if we dont allow creator to be modified
    origvalues['creator'] = values.get('creator', '')
    origvalues['modified'] = timenow()

    data[shortlink] = origvalues

    write_db(data)
    read_db()


@hug.startup()
def setup(api):
    """
    Read the database when server boots up
    """
    Path('data').mkdir_p()

    if not STATSPATH.exists():
        STATSPATH.write_lines(["{}"])

    if not ALIASESPATH.exists():
        ALIASESPATH.write_lines([])

    read_db()


def update_stats(link):

    link['hits'] = link.get('hits', 0) + 1
    link['modified'] = timenow()

    data[link['shortlink']] = link

    write_db(data)
    read_db()


def write_db(data):
    """
    Handles writing of data to database
    """

    data = copy.deepcopy(data)

    aliaseslinetemplate = "{shortlink} {destination}"

    aliases = [aliaseslinetemplate.format_map(x) for x in data.values()]

    # Return value doesnt matter.
    [(x.pop('shortlink'), x.pop('destination')) for x in data.values()]

    ALIASESPATH.write_lines(aliases)
    json.dump(data, open(STATSPATH, 'w'))


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

    destination = 'http://%s' % destination

    response.content_type = falcon.MEDIA_HTML

    response.body = '''<html><head><script>window.location="{0}";</script></head><body>Redirecting to {0}</body></html>'''.format(
        destination)


@hug.sink('/')
def redirect_handler(request, response):
    """Main shortlink handler"""
    shortlink = request.path.lstrip('/')

    link = find(shortlink)

    body = request.stream.read()

    if request.method == 'GET' and link:
        print("Redirecting: {} -> {}".format(shortlink, link['destination']))

        if is_internal(link['destination']):
            update_stats(link)
            return respond_internal_url(response, link['destination'])
        else:
            update_stats(link)
            return respond_external_url(response, link['destination'])

    elif request.method == 'GET' and not link:
        # Trying to go link that doesnt exist yet. Give an option to create
        print(
            "Trying to go to a link that doesnt exist yet. Here's an option to create"
        )
        pass
    elif request.method == 'POST' and body:

        # This is adding a new shortlink
        body = json.loads(body)
        print("Setting up a new golink: {} -> {}".format(
            shortlink, body['destination']))
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
    return ("dist/", )


@hug.get('/_api/allurls')
def api_allurls_handler(request, response, cors: hug.directives.cors = "*"):

    return get_all_links()


@hug.get('/_api/delete/{shortlink}')
def api_delete_url_handler(shortlink,
                           request,
                           response,
                           cors: hug.directives.cors = "*"):

    del_link(shortlink)


@hug.post('/_api/add/{shortlink}')
def api_add_url_handler(shortlink,
                        body,
                        request,
                        response,
                        cors: hug.directives.cors = "*"):

    add_link(shortlink, body['destination'], body.get('creator', ''))


@hug.post('/_api/edit/{shortlink}')
def api_edit_url_handler(shortlink,
                         body,
                         request,
                         response,
                         cors: hug.directives.cors = "*"):

    edit_link(shortlink, body)


@hug.get('/_api/validate/{shortlink}')
def api_validate_shortlink_handler(shortlink,
                                   body,
                                   request,
                                   response,
                                   cors: hug.directives.cors = "*"):

    return shortlink_exists(shortlink)


@hug.get('/_api/refresh')
def api_validate_shortlink_handler(body,
                                   request,
                                   response,
                                   cors: hug.directives.cors = "*"):

    read_db()
    return get_all_links()


# Some testing fixtures
if __name__ == '__main__':
    print(read_db())
    print(find('mail'))
    print(find('foo'))
