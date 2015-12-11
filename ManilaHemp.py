import queue
import threading
import json
from urllib.request import urlopen
from urllib.parse import quote


# Wikipedia article
# @title: Title of the Wiki article
# @father: The article which had a link to this one
# @reverse: True if this article originates from start article
#          False if this article originates from goal article
class article:

    def __init__(self, title, father, reverse):
        self.title = title
        self.father = father
        self.reverse = reverse


# Makes Wikipedia API call
# @url: API calls URL as String
# @title: Title of the Wiki article that is being used in API call
# returns: JSON object
def apiCall(query, title):
    url = 'http://en.wikipedia.org/w/api.php?'
    response = urlopen(url + query + quote(title))
    str_response = response.read().decode('utf-8')
    obj = json.loads(str_response)
    obj_pages = obj['query']['pages']
    obj_links = list(map(lambda x: obj_pages[x], obj_pages.keys()))
    return obj_links[0]


# /w/api.php?action=query&prop=linkshere&format=json&lhnamespace=0&lhlimit=500&titles=
def linksHere(title):
    obj = apiCall(
        '&action=query'
        '&prop=linkshere'
        '&format=json'
        '&lhnamespace=0'
        '&lhlimit=500'
        '&titles=', title)
    try:
        return list(map(lambda x: x['title'], obj['linkshere']))
    except KeyError:
        print("KeyError")


def links(title):
    obj = apiCall(
        'action=query'
        '&prop=links'
        '&format=json'
        '&plnamespace=0'
        '&pllimit=500'
        '&titles=', title)
    try:
        return list(map(lambda x: x['title'], obj['links']))
    except KeyError:
        print("KeyError")


def path(article, link):
    a = article
    str = goal
    while not a.title == start:
        str = a.title + " -> " + str
        a = a.father
    return start + " -> " + str


'''
Basic settings and variables
start = "Army_Group_Centre"
goal = "Adolf_Hitler"
start = "Heat_(1996_film)"
'''

start = input("Start article: ")
goal = input("Goal article: ")

num_worker_threads = 5

# Job queues for workers
jobs = queue.Queue()
r_jobs = queue.Queue()

# Article arrays to keep track of the link paths
articles = []
r_articles = []

# Arrays for checking if path has been found
titles = []
r_titles = []

# Flag: True if path has been found
f = False

num_worker_threads = 50
q = queue.Queue()
visited = []
goalTitles = linksHere(goal)
f = True

# Worker thread


def worker():
    global start
    global goal
    global f
    global visited
    while f:
        a = q.get()
        obj = links(a.title)
        if obj:
            for i in obj:
                if not i in visited:
                    newArticle = article(i, a, False)
                    if i in goalTitles:
                        f = False
                        print(path(newArticle, i))
                        break
                    else:
                        visited += i
                        q.put(newArticle)
                if not f:
                    break
        q.task_done()


# Start worker threads
for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

q.put(article(start, "", False))
q.join()
