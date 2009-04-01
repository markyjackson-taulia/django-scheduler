from schedule.models import Calendar
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from schedule.feeds.atom import Feed
import datetime, itertools

class UpcomingEventsFeed(Feed):
    feed_id = "upcoming"
    
    def feed_title(self, obj):
        return "Upcoming Events for %s" % obj.name
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Calendar.objects.get(pk=bits[0])
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()
    
    def items(self, obj):
        return itertools.islice(obj.occurrences_after(datetime.datetime.now()), 
            get_attr(settings, "FEED_LIST_LENGTH", 10))
    
    def item_id(self, item):
        return str(item.id)
    
    def item_title(self, item):
        return item.event.title
    
    def item_authors(self, item):
        return [{"name": item.event.creator.username}]
    
    def item_updated(self, item):
        return item.event.created_on
    
    def item_content(self, item):
        return item.event.title + "\n" + item.event.description