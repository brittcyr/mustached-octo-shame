import feedparser
import datetime
from BeautifulSoup import BeautifulSoup

now = datetime.datetime.now().strftime('%a, %d %b %Y')

def get_menu(dining_hall):
    feed = {'Maseeh':398, 'Baker':399}[dining_hall]
    url = 'http://legacy.cafebonappetit.com/rss/menu/' + str(feed)
    week = feedparser.parse(url)
    for entry in week['entries']:
        if entry['title'] == now:
            today = entry['summary']

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
