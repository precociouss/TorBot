import requests

from urllib.parse import urlsplit
from termcolor import cprint


def executeAll(target, soup, response):

    try:
        get_robots_txt(target)
    except Exception:
        cprint("No robots.txt file Found!""blue")
    try:
        get_dot_git(target)
    except Exception:
        cprint("Error !""red")
    try:
        get_dot_svn(target)
    except Exception:
        cprint("Error""red")
    try:
        get_dot_htaccess(target)
    except Exception:
        cprint("Error""red")
    try:
        get_webpage_description(soup)
    except Exception:
        cprint("Error""red")
    try:
        get_headers(response)
    except Exception:
        cprint("Error""red")


def get_headers(response):
    print('''
          RESPONSE HEADERS
          __________________
          ''')
    for key, val in response.headers.items():
        print('*', key, ':', val)


def get_robots_txt(target):
    cprint("[*]Checking for Robots.txt"'yellow')
    url = target
    target = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    requests.get(target+"/robots.txt")
    cprint(r'blue')


def get_dot_git(target):
    cprint("[*]Checking for .git folder"'yellow')
    url = target
    target = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    req = requests.get(target+"/.git/")
    r = req.status_code
    if r == 200:
        cprint("Alert!"'red')
        cprint(".git folder exposed publicly"'red')
    else:
        print("NO .git folder found"'blue')


def get_dot_svn(target):
    cprint("[*]Checking for .svn folder"'yellow')
    url = target
    target = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    req = requests.get(target+"/.svn/entries")
    r = req.status_code
    if r == 200:
        cprint("Alert!"'red')
        cprint(".SVN folder exposed publicly"'red')
    else:
        cprint("NO .SVN folder found"'blue')


def get_dot_htaccess(target):
    cprint("[*]Checking for .htaccess"'yellow')
    url = target
    target = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    req = requests.get(target+"/.htaccess")
    statcode = req.status_code
    if statcode == 403:
        cprint("403 Forbidden"'blue')
    elif statcode == 200:
        cprint("Alert!!"'blue')
        cprint(".htaccess file found!"'blue')
    else:
        cprint("Status code"'blue')
        cprint(statcode)


def get_webpage_description(soup):
    cprint("[*]Checking for description meta tag"'yellow')
    metatags = soup.find_all('meta')
    for meta in metatags:
        if meta.has_attr('name'):
            attributes = meta.attrs
            if attributes['name'] == 'description':
                cprint("Page description: " + attributes['content'])
