from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpRequest
from . import controller
import typing as tp
from .forms import RSSFeedUrlForm


def index(request: HttpRequest, rss_feed_url: str = 'https://rss.app/feeds/fSA6Np3GEBi0GdDC.xml') -> HttpResponse:
    if request.method == 'POST':
        form = RSSFeedUrlForm(request.POST)
        rss_feed_url = form['rss_feed_url'].value()
    else:
        rss_feed_url = request.session['rss_feed_url']\
            if 'rss_feed_url' in request.session.keys() else rss_feed_url
        form = RSSFeedUrlForm()
    recent_feed_items: tp.List[tp.Dict[str, str]] = controller.get_recent_feed_items(rss_feed_url)
    request.session['rss_feed_url'] = rss_feed_url
    return render(request, 'rss_reader_interface/index.html', context={
        'rss_feed_url': rss_feed_url,
        'recent_feed_item': recent_feed_items,
        'form': form
    })

def show_more_about_item(request: HttpRequest, item_index: int) -> HttpResponse:
    if 'rss_feed_url' in request.session.keys():
        rss_feed_url = request.session['rss_feed_url']
    else:
        return redirect(reverse(index))
    recent_feed_items: tp.List[tp.Dict[str, str]] = controller.get_recent_feed_items(rss_feed_url)
    item_data = recent_feed_items[item_index]
    return render(request, 'rss_reader_interface/item.html', context={
        'item_data': item_data,
    })


def return_to_index(request: HttpRequest) -> HttpResponse:
    return redirect(reverse(index))
