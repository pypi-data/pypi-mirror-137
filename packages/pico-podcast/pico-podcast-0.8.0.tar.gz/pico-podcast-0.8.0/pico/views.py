from django.http.response import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from django.views.generic.base import View
from django.views.generic.list import ListView
from markdown import markdown
from pico.conf import settings
from pico.podcasts.models import Podcast, Page, Episode, Post
from pico.podcasts.tasks import update_feed
from pico.seo.mixins import SEOMixin, OpenGraphMixin
import json
import re


LINK_REGEX = re.compile(r'^\<([^\>]+)\>')


class PodcastListView(SEOMixin, OpenGraphMixin, ListView):
    model = Podcast
    template_name = 'index.html'

    def get_menu_items(self):
        if settings.DOMAINS_OR_SLUGS == 'slugs':
            yield {
                'url': '/',
                'text': 'Home'
            }

            for podcast in Podcast.objects.all():
                yield {
                    'url': '/%s/' % podcast.slug,
                    'text': podcast.short_name or podcast.name
                }

            for page in Page.objects.filter(
                podcast=None,
                menu_visible=True
            ):
                yield {
                    'url': page.get_absolute_url(),
                    'text': page.menu_title or page.title
                }

            if Post.objects.filter(
                published__lte=timezone.now(),
                podcast=None
            ).exists():
                yield {
                    'url': '/blog/',
                    'text': 'Blog'
                }

            return

    def build_menu(self):
        items = list(self.get_menu_items())

        for item in items:
            if item['url'] == self.request.path:
                item['active'] = True

            item['url'] = self.request.build_absolute_uri(item['url'])

        return items

    def get_seo_title(self):
        network_name = settings.NETWORK_NAME
        network_subtitle = settings.network_subtitle

        if network_subtitle:
            return '%s - %s' % (
                network_name,
                network_subtitle
            )

        return network_name

    def get_context_data(self, **kwargs):
        return {
            'menu_items': self.build_menu(),
            **super().get_context_data(**kwargs)
        }


class PodcastPingView(View):
    def get(self, request):
        topic = request.GET.get('hub.topic')
        mode = request.GET.get('hub.mode')
        challenge = request.GET.get('hub.challenge')

        for podcast in Podcast.objects.filter(
            rss_feed_url=topic
        ):
            if mode in ('subscribe', 'unsubscribe') and challenge:
                return HttpResponse(challenge)

        return HttpResponseBadRequest('FAIL')

    def post(self, request):
        topic = request.META.get('HTTP_LINK')

        if topic:
            match = LINK_REGEX.match(topic)
            if match is not None:
                url = match.groups()[0]

                for podcast in Podcast.objects.filter(
                    rss_feed_url=url
                ):
                    update_feed.delay(podcast.pk, request.body)
                    return HttpResponse('OK')

        return HttpResponseBadRequest('FAIL')


class ContentListView(View):
    def get_fields(self):
        if not hasattr(self, 'fields'):
            self.fields = self.request.GET.get(
                'fields',
                'id,title,url,published_at,feature_image'
            ).split(',')

        return self.fields

    def get_formats(self):
        if not hasattr(self, 'formats'):
            self.formats = self.request.GET.get(
                'formats',
                'plaintext'
            ).split(',')

        return self.formats

    def get_querysets(self):
        limit = self.request.GET.get('limit', 'all')
        querysets = [
            Episode.objects.all(),
            Post.objects.filter(
                published__lte=timezone.now()
            )
        ]

        if 'published_at' not in self.get_fields():
            querysets.append(
                Page.objects.all()
            )

        if limit != 'all':
            limit = int(limit)

            for queryset in querysets:
                queryset = queryset[:limit]

        return querysets

    def serialise_object(self, obj):
        fields = self.get_fields()
        formats = self.get_formats()
        data = {
            'id': '%s.%s:%s' % (
                obj._meta.app_label,
                obj._meta.model_name,
                obj.pk
            )
        }

        if 'title' in fields:
            data['title'] = str(obj)

        if 'url' in fields:
            data['url'] = obj.get_absolute_url()

        if 'published_at' in fields:
            if isinstance(obj, (Episode, Post)):
                data['published_at'] = obj.published.isoformat()

        if 'feature_image' in fields:
            data['feature_image'] = ''

            if isinstance(obj, Episode) and obj.artwork:
                data['feature_image'] = obj.artwork.url
            elif isinstance(obj, (Post, Page)) and obj.image:
                data['feature_image'] = obj.image.url
            elif obj.podcast_id and obj.podcast.artwork:
                data['feature_image'] = obj.podcast.artwork.url

        if 'plaintext' in formats:
            if isinstance(obj, Episode):
                data['plaintext'] = obj.feed_description or obj.body
            else:
                data['plaintext'] = obj.body

        if 'html' in formats:
            if isinstance(obj, Episode):
                data['html'] = markdown(obj.feed_description or obj.body)
            else:
                data['html'] = markdown(obj.body)

        return data

    def get_object_list(self):
        for queryset in self.get_querysets():
            for obj in queryset:
                yield self.serialise_object(obj)

    def get(self, request):
        return HttpResponse(
            json.dumps(
                {
                    'posts': list(self.get_object_list())
                }
            ),
            content_type='application/json'
        )
