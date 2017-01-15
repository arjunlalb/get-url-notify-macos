#!/usr/bin/python
import simplejson
from pync import Notifier
import requests
import argparse
import time

HTTP_PREFIX = "http://"
HTTPS_PREFIX = "https://"

def fire_url_get_response(url) :
	session = requests.session()
	response = session.get(url)
	return response.text

def send_notification(titleText, message):
	Notifier.notify(str(message), title = str(titleText))
	return

def parse_url(url):
	if ( url.find(HTTP_PREFIX, 0, len(HTTP_PREFIX)) != -1 or url.find(HTTPS_PREFIX, 0, len(HTTPS_PREFIX)) != -1 ):
		return url
	return "http://" + url

def main():
	parser = argparse.ArgumentParser(description="Script to hit a URL and notify with response at specific intervals (OSX)")
  	parser.add_argument("--url", required=True, help="URL to hit")
  	parser.add_argument("--notif_title", required=True, help="Title to be used for the notification")
  	parser.add_argument("--notif_interval", required=False, help="Time interval between notifications (in seconds)", default=300)
  	parser.add_argument("--total", required=False, help="Total number of notifications to be shown", default=-1)
  	args = parser.parse_args()

	url = parse_url(args.url)
	notification_title = args.notif_title
	notification_interval = args.notif_interval
	total_notifications = args.total
	notification_count = 0

	while(total_notifications == -1 or notification_count != total_notifications) :
		response = fire_url_get_response(url)
		send_notification(notification_title, response)	
		time.sleep(notification_interval)
		notification_count += 1
	
if __name__ == "__main__":
  main()

