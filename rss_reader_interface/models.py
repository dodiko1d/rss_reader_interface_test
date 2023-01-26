from django.db import models

# Create your models here.
class RSSFeed(models.Model):
    link: models.TextField = models.TextField()

class RSSFeedItem(models.Model):
    title: models.TextField = models.TextField()
    date: models.DateTimeField = models.DateField()
    rss_feed: models.ForeignKey = models.ForeignKey(RSSFeed, on_delete=models.CASCADE)
    thumbnail_url: models.TextField = models.TextField()
    source_url: models.TextField = models.TextField()
