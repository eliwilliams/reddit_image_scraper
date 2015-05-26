import urllib, urllib2, json, requests, os, getpass, sys


def doWork(header={"imgscraper" : "reddit"}, subreddit="wallpapers", savepath=""):
	try:
		data = requests.get("http://www.reddit.com/r/{0}/.json".format(subreddit), headers=header)
	except Exception:
		print "Cannot connect to reddit's servers at this time"
	d = data.json()
	try:
		posts = d["data"]["children"]
	except Exception:
		print "Encountered error; running again."
		main()
	pics = []
	galleries = []
	for post in posts:
		if "i.imgur" in post["data"]["domain"]:
			pics.append(post["data"]["url"].encode('utf-8'))
		elif "imgur" and "gallery" in post["data"]["domain"]:
			galleries.append(post["data"]["url"])
	if len(pics) > 0:
		saveImages(savepath, pics)
	if len(galleries) > 0:
		saveGallery(savepath, galleries)
			


def sanitizeImages(piclist):
	extensions = ["jpg", "gif", "png"]
	
	for pic in piclist[:]:
		picname = str.split(pic, "/")[len(str.split(pic, "/")) - 1]
		if not str.split(picname, ".")[len(str.split(picname, ".")) - 1] in extensions:
			for e in extensions:
				if e in str.split(picname, ".")[len(str.split(picname, ".")) - 1]:
					piclist = [pic.replace(str.split(picname, ".")[len(str.split(picname, ".")) - 1], e) for pic in piclist]
					continue
	return piclist
	

def saveImages(savepath, piclist):
	counter = 0
	piclist = sanitizeImages(piclist)
	
	if os.getcwd is not savepath:
			fixDir(savepath)

	for pic in piclist:
			picname = str.split(pic, "/")[len(str.split(pic, "/")) - 1]
			if not os.path.exists(savepath + "/" + picname):
				urllib.urlretrieve(pic, picname)
				counter += 1
	print "Successfully saved {0} images to {1}".format(counter, savepath)
	return
	
	
	
def saveGallery(savepath, glist):
	print "Encountered gallery, skipping for now"
		
		
		
def fixDir(savepath):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	os.chdir(savepath)
	
	
def main():
	subreddit = "funny" #sys.argv[1]
	header = {"Python Image Scraper" : "/u/dudest"}
	un = getpass.getuser()
	sp = "/Users/{0}/Pictures/{1}".format(un, subreddit) #sys.argv[2]
	doWork(header, subreddit, sp)

if __name__ == "__main__":
	main()


'''
workflow:
create list of picutes (seperate from galleries) from json of desired subreddit
check to see if a save path exists (in Pictures folder) that matches subreddit, if not, create one
save list of pictures from imgur (gallery support to be added soon)

***note that sometimes it is touchy with the reddit.com servers, so please be gentle***
'''
