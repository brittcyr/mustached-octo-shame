#!/usr/bin/env python
import feedparser
import smtplib
import datetime
from BeautifulSoup import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

now = datetime.datetime.now().strftime('%a, %d %b %Y')

def get_menu(dining_hall):
    feed = {'Maseeh':398, 'Baker':399}[dining_hall]
    url = 'http://legacy.cafebonappetit.com/rss/menu/' + str(feed)
    week = feedparser.parse(url)
    today = 0
    for entry in week['entries']:
        today = entry['summary'] if entry['title'] == now else today
    if not today:
        return 'Error getting today\'s menu for ' + dining_hall

    today = BeautifulSoup(today)

    current_meal = 'Breakfast'
    meals = {'Lunch':'', 'Breakfast':'', 'Brunch':'', 'Dinner':''}
    for item in today:
        for meal in meals.keys():
            current_meal = current_meal if meal not in item else meal
        if item == '\n':
            continue
        meals[current_meal] += str(item).replace('&nbsp', '').replace('\n','')
    return meals['Dinner']

print 'Maseeh:'
print get_menu('Maseeh') + '\n'
print 'Baker:'
print get_menu('Baker')


me = "cyrbritt@mit.edu"
you = "cyrbritt@mit.edu"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Dinner Menus"
msg['From'] = me
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
text = "Menus"
html = "<h1>Maseeh</h1>" + get_menu('Maseeh') + "<h1>Baker</h1>" + get_menu('Baker')

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.
s = smtplib.SMTP('localhost')
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(me, you, msg.as_string())
s.quit()
