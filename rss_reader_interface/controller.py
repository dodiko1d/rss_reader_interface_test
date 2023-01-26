import typing as tp
import datetime
from dateutil import parser
from . import models
import feedparser
from django.db import transaction


@transaction.non_atomic_requests
def add_items_to_db_and_view_data(
        rss_feed: tp.Union[models.RSSFeed],
        data: tp.List[tp.Dict[str, tp.Any]],
        view_data: tp.List[tp.Dict[str, str]]
) -> None:
    for index, item in enumerate(data):
        thumbnail_url: tp.Union[str, None] = item['media_content'][0]['url'] if 'media_content' in item.keys() else None
        thumbnail_url = item['image']['href'] if 'image' in item.keys() else thumbnail_url
        source_url: tp.Union[str, None] = item['links'][0]['href'] if 'links' in item.keys() else None
        source_url = item['link'] if 'link' in item.keys() else source_url
        date: tp.Union[datetime.datetime, None] = parser.parse(item['updated']) \
            if 'updated' in item.keys() else parser.parse(item['published'])

        item_data = {
            'title': item['title'],
            'date': date,
            'thumbnail_url': thumbnail_url if thumbnail_url else 'None',
            'source_url': source_url if source_url else 'Unknown source'
        }
        models.RSSFeedItem.objects.create(rss_feed=rss_feed, **item_data)
        item_data['index'] = index
        view_data.append(item_data)


@transaction.non_atomic_requests
def get_recent_feed_items(rss_feed_link: str) -> tp.List[tp.Dict[str, str]]:
    data = feedparser.parse(rss_feed_link)['entries']
    view_data: tp.List[tp.Dict[str, str]] = []

    link_filtered_rss_feed_objects = models.RSSFeed.objects.filter(link=rss_feed_link)
    if len(link_filtered_rss_feed_objects) == 0:
        rss_feed: models.RSSFeed = models.RSSFeed.objects.create(link=rss_feed_link)
        add_items_to_db_and_view_data(rss_feed, data, view_data)
    else:
        rss_feed: models.RSSFeed = link_filtered_rss_feed_objects[0]
        the_oldest_post_date: datetime.datetime = parser.parse(data[-1]['updated']) \
            if 'updated' in data[-1].keys() else parser.parse(data[-1]['published'])
        rss_feed_item_set = rss_feed.rssfeeditem_set.all()
        rss_feed_item_set\
            .filter(rss_feed__rssfeeditem__date__range=(datetime.datetime.min, the_oldest_post_date))\
            .delete()
        data = data[:len(data) - len(rss_feed.rssfeeditem_set.all())]
        add_items_to_db_and_view_data(rss_feed, data, view_data)
    return view_data
