import time
import praw
import urllib.request
import os
import re
from subprocess import call
from pprint import pprint

bot = praw.Reddit(
	user_agent=os.environ['REDDIT_USER_AGENT'],
	client_id=os.environ['REDDIT_CLIENT_ID'],
	client_secret=os.environ['REDDIT_CLIENT_SECRET'],
	username=os.environ['REDDIT_USERNAME'],
	password=os.environ['REDDIT_PWD'])

work_dir = os.getcwd()
progress = []

def set_environ():
	subR = getSubreddit()
	subreddit = bot.subreddit(subR)
	path = work_dir + '/' + subR
	set_Path(path=path)
	score = setLimit()
	find_photos(subreddit=subreddit, path=path, score=score)
	return subR

def find_photos(subreddit, path, score):
	for submission in subreddit.hot(limit=50):
		os.chdir(path)
		if submission.score >= score:
			filename = re.sub(r'\W+', '', submission.title) + submission.thumbnail[-4:]
			url = submission.url
			download_photos(url,filename)

def download_photos(url,filename):
	image = urllib.request.urlretrieve(url,filename)
	progress.append(filename)
	printProgress()

def finish(dir_name):
	print('Done. downloaded {}'.format(len(progress)))
	os.chdir('..')
	target_dir = work_dir + "/" + dir_name
	print(target_dir)
	call(["open", target_dir])

def setLimit():
	return int(input('Set a score param: '))

def getSubreddit():
	return input('Enter the subreddit: ')

def set_Path(path):
	print("Downloaded photos will go to: {}".format(path))
	if not os.path.exists(path):
		os.makedirs(path)

def printProgress():
	call('clear', shell=True)
	print('downloading... ' + str((len(progress))))


if __name__ == '__main__':
	print('Authenticated as {}'.format(bot.user.me()))
	dir_name = set_environ()
	finish(dir_name)
