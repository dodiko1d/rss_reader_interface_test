from django import forms

class RSSFeedUrlForm(forms.Form):
    rss_feed_url = forms.CharField(label='New RSS feed link', max_length=100)