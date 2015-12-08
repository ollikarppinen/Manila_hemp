import queue, threading, json
from urllib.request import urlopen
from urllib.parse import quote

class article:
	def __init__(self, title, father):
		self.title = title
		self.father = father

def apiCall(url, title):
	response = urlopen(url + quote(title))
	str_response = response.readall().decode('utf-8')
	obj = json.loads(str_response)
	return obj

def linksHere(title):
	obj = apiCall('http://en.wikipedia.org/w/api.php?action=query&prop=linkshere&format=json&lhprop=pageid%7Ctitle&lhlimit=5000&titles=', title)
	arr = []
	for i in obj['query']['pages']:
		if 'linkshere' in obj['query']['pages'][i].keys():
			for j in obj['query']['pages'][i]['linkshere']:
				if j['ns'] == 0:
					arr += [j['title']]
	return arr

def links(title):
	obj = apiCall('http://en.wikipedia.org/w/api.php?action=query&prop=links&format=json&pllimit=5000&titles=', title)
	arr = []
	for i in obj['query']['pages']:
		if 'links' in obj['query']['pages'][i].keys():
			for j in obj['query']['pages'][i]['links']:
				if j['ns'] == 0:
					arr += [j['title']]
	return arr

def path(goal, start, article):
	a = article
	str = goal
	while not a.title == start:
		str = a.title + " -> " + str
		a = a.father
	return start + " -> " + str

#Basic settings and variables
#start = "Army_Group_Centre"
#goal = "Adolf_Hitler"
#start = "Heat_(1996_film)"
start = input("Start article: ")
goal = input("Goal article: ")

num_worker_threads = 5
q = queue.Queue()
visited = []
goals = linksHere(goal)
f = True

#Worker thread
def worker():
	global start
	global goal
	global f
	global visited
	while True:
		if not f:
			q.task_done()
		elif q:
			a = q.get()
			obj = links(a.title)
			for i in obj:
				if not i in visited:
					newArticle = article(i, a)
					if i in goals:
						f = False
						print(path(goal, start, newArticle))
					else:
						visited += i
						q.put(newArticle)
	

#Start worker threads
for i in range(num_worker_threads):
	t = threading.Thread(target=worker)
	t.daemon = True
	t.start()

q.put(article(start, ""))
q.join()

'''
import Queue, threading

#Basic settings and variables
num_worker_threads = 5
q = Queue.Queue()

#Worker thread
def worker():
	while True:
			item = q.get()
			print item
			q.task_done()

#Start worker threads
for i in range(num_worker_threads):
	t = threading.Thread(target=worker)
	t.daemon = True
	t.start()


for i in range(10):
	q.put(i)

q.join()
'''