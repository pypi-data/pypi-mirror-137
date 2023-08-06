from dateutil.parser import parse as parse_date
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import html, text
from feedparser import parse as parse_feed
from html2text import html2text
from markdownx.models import MarkdownxField
from pico.conf import settings
from urllib.parse import urlparse
from .query import PodcastQuerySet, EpisodeQuerySet, PostQuerySet
from .utils import download, compare_image
import os
import re


PLAYER_REGEXES = (
    (
        re.compile(r'https://media.transistor.fm/([^/]+)/.*'),
        r'https://share.transistor.fm/e/\g<1>'
    ),
)


class Podcast(models.Model):
    objects = PodcastQuerySet.as_manager()

    def upload_artwork(self, filename):
        return 'podcasts/%s/artwork%s' % (
            self.slug,
            os.path.splitext(filename)[-1]
        )

    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=30, unique=True)
    domain = models.CharField(max_length=100, null=True, blank=True)
    rss_feed_url = models.URLField('RSS feed URL', max_length=255, unique=True)

    artwork = models.ImageField(
        max_length=255,
        upload_to=upload_artwork
    )

    subtitle = models.CharField(max_length=255, null=True, blank=True)
    description = MarkdownxField()

    twitter_username = models.CharField(max_length=30, null=True, blank=True)
    facebook_username = models.CharField(max_length=30, null=True, blank=True)
    instagram_username = models.CharField(max_length=30, null=True, blank=True)

    about_page = models.OneToOneField(
        'Page',
        on_delete=models.SET_NULL,
        related_name='about_page_for',
        null=True,
        blank=True
    )

    ordering = models.CharField(
        max_length=1,
        choices=(
            ('r', 'reverse-chronological'),
            ('n', 'episode number')
        ),
        default='r'
    )

    colour_brand = models.CharField(
        'brand',
        max_length=8,
        default='6219ff'
    )

    colour_white = models.CharField(
        'white',
        max_length=8,
        default='ffffff'
    )

    colour_dark = models.CharField(
        'dark',
        max_length=8,
        default='1c203c'
    )

    colour_text = models.CharField(
        'text',
        max_length=8,
        default='1c203c'
    )

    colour_grey = models.CharField(
        'grey',
        max_length=8,
        default='626265'
    )

    colour_error = models.CharField(
        'error messages',
        max_length=8,
        default='d50000'
    )

    colour_success = models.CharField(
        'success messages',
        max_length=8,
        default='008040'
    )

    colour_border = models.CharField(
        'border',
        max_length=8,
        default='f3ece2'
    )

    bg_colour = models.CharField(
        'background',
        max_length=8,
        default='ffffff'
    )

    bg_grey = models.CharField(
        'grey background',
        max_length=8,
        default='f4f0eb'
    )

    def __str__(self):
        return self.name

    def check_feed(self, episode_callback=None):
        feed_data = parse_feed(self.rss_feed_url)
        self.update_feed(feed_data, episode_callback)

    def update_feed(self, feed, episode_callback=None):
        for item in feed['items']:
            season_number = item.get('itunes_season')
            episode_number = item.get('itunes_episode')
            episode_type = item.get('itunes_episodetype')
            author = item.get('author')
            season = None

            if season_number:
                season = self.seasons.filter(
                    number=season_number
                ).first()

                if season is None:
                    season = self.seasons.create(
                        number=season_number
                    )

            image = item.get('image', {}).get('href', '')
            if image:
                image = download(image)

                if self.artwork and not compare_image(image, self.artwork):
                    image = None

            description = item.get('summary')
            summary = html.strip_tags(item.get('subtitle'))

            for detail in item.get('content', []):
                if detail['type'] == 'text/html':
                    description = detail['value']
                    break

            enclosure = None
            for link in item.get('links', []):
                if link['rel'] == 'enclosure':
                    enclosure = link['href']

            date = parse_date(item['published'])
            episode = self.episodes.filter(
                guid=item['id']
            ).first()

            if episode is None:
                episode = Episode(
                    guid=item['id'],
                    podcast=self
                )
            elif episode.artwork:
                if image and not compare_image(image, episode.artwork):
                    image = None

            episode.title = item['title']
            episode.published = date
            episode.season = season
            episode.number = episode_number or 0
            episode.bonus = episode_type == 'bonus'
            episode.trailer = episode_type == 'trailer'

            if image is not None:
                episode.artwork = image

            episode.summary = summary
            episode.feed_description = html2text(description)
            episode.enclosure_url = enclosure
            episode.save()

            if author:
                for name in author.split(','):
                    name_stripped = name.strip()
                    host = Host.objects.filter(
                        name__iexact=name_stripped
                    ).first()

                    if host is not None:
                        episode.hosts.add(host)
                        self.hosts.add(host)

            if callable(episode_callback):
                episode_callback(episode)

    @property
    def apple_podcasts_id(self):
        if not hasattr(self, '__apple_podcasts_id'):
            self.__apple_podcasts_id = None
            for link in self.subscription_links.filter(
                directory__name__iexact='apple podcasts'
            ):
                parts = urlparse(link.url).path
                for part in reversed(parts.split('/')):
                    if part:
                        match = re.match(r'^id(\d+)$', part)
                        if match is not None:
                            return match.groups()[0]

        return self.__apple_podcasts_id

    def reverse(self, urlname, args=(), kwargs={}):
        if settings.DOMAINS_OR_SLUGS == 'slugs':
            if any(kwargs):
                kwargs['podcast'] = self.slug
            else:
                args = (self.slug,) + args

        return reverse(urlname, args=args, kwargs=kwargs)

    def build_absolute_uri(self, path=''):
        while path.startswith('/'):
            path = path[1:]

        if settings.DOMAINS_OR_SLUGS == 'slugs':
            return '/%s/%s' % (self.slug, path)

        return '//%s/%s' % (self.domain, path)

    def get_rss_url(self):
        if settings.DOMAINS_OR_SLUGS == 'slugs':
            return '/%s/css/' % (self.slug)

        return '//%s/css/' % (self.domain)

    def get_order_by(self):
        if self.ordering == 'n':
            return (
                'season__number',
                'number',
                'bonus'
            )

        return ('-published',)

    class Meta:
        ordering = ('name',)


class Directory(models.Model):
    def upload_icon(self, filename):
        return 'directories/%s%s' % (
            text.slugify(self.name),
            os.path.splitext(filename)[-1]
        )

    name = models.CharField(max_length=100)
    icon = models.FileField(
        max_length=255,
        upload_to=upload_icon
    )

    ordering = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('ordering',)
        verbose_name_plural = 'directories'


class SubscriptionLink(models.Model):
    podcast = models.ForeignKey(
        Podcast,
        on_delete=models.CASCADE,
        related_name='subscription_links'
    )

    directory = models.ForeignKey(
        Directory,
        on_delete=models.CASCADE,
        related_name='entries'
    )

    url = models.URLField('URL', max_length=255)

    def __str__(self):
        return urlparse(self.url).netloc

    class Meta:
        ordering = ('directory__ordering',)
        unique_together = ('directory', 'podcast')


class Season(models.Model):
    def upload_artwork(self, filename):
        return 'podcasts/%s/%s%s' % (
            self.podcast.slug,
            self.number,
            os.path.splitext(filename)[-1]
        )

    podcast = models.ForeignKey(
        Podcast,
        on_delete=models.CASCADE,
        related_name='seasons'
    )

    number = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=100, null=True, blank=True)

    artwork = models.ImageField(
        max_length=255,
        upload_to=upload_artwork,
        null=True,
        blank=True
    )

    summary = models.TextField(null=True, blank=True)
    description = MarkdownxField(null=True, blank=True)

    def __str__(self):
        return self.name or ('Season %d' % self.number)

    def get_absolute_url(self):
        return self.podcast.reverse('season', args=(self.number,))

    class Meta:
        unique_together = ('number', 'podcast')
        ordering = ('number',)


class Host(models.Model):
    def upload_photo(self, filename):
        return 'hosts/%s%s' % (
            self.slug,
            os.path.splitext(filename)[-1]
        )

    podcasts = models.ManyToManyField(
        Podcast,
        related_name='hosts'
    )

    photo = models.ImageField(
        max_length=255,
        upload_to=upload_photo
    )

    number = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=30, unique=True)
    biography = MarkdownxField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'


class Episode(models.Model):
    objects = EpisodeQuerySet.as_manager()

    def upload_artwork(self, filename):
        if self.season_id:
            return 'podcasts/%s/%s-%s%s%s' % (
                self.podcast.slug,
                self.season.number,
                self.trailer and 'trailer' or self.number,
                self.bonus and 'a' or '',
                os.path.splitext(filename)[-1]
            )

        return 'podcasts/%s/%s%s%s' % (
            self.podcast.slug,
            self.trailer and 'trailer' or self.number,
            self.bonus and 'a' or '',
            os.path.splitext(filename)[-1]
        )

    podcast = models.ForeignKey(
        Podcast,
        on_delete=models.CASCADE,
        related_name='episodes'
    )

    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='episodes',
        null=True,
        blank=True
    )

    hosts = models.ManyToManyField(
        Host,
        related_name='episodes'
    )

    title = models.CharField(max_length=255)
    guid = models.CharField(max_length=255, db_index=True)
    published = models.DateTimeField()
    number = models.CharField(max_length=3, db_index=True)
    bonus = models.BooleanField(default=False)
    trailer = models.BooleanField(default=False)

    artwork = models.ImageField(
        max_length=255,
        upload_to=upload_artwork,
        null=True,
        blank=True
    )

    summary = models.TextField()
    feed_description = models.TextField()
    enclosure_url = models.URLField(
        'enclosure URL',
        max_length=255,
        unique=True
    )

    body = MarkdownxField(null=True, blank=True)

    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='episodes'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.season_id:
            if self.trailer:
                return self.podcast.reverse(
                    'season_episode_trailer_detail',
                    args=(
                        self.season.number,
                    )
                )

            if self.bonus:
                return self.podcast.reverse(
                    'season_episode_bonus_detail',
                    args=(
                        self.season.number,
                        self.number
                    )
                )

            return self.podcast.reverse(
                'season_episode_detail',
                args=(
                    self.season.number,
                    self.number
                )
            )

        if self.trailer:
            return self.podcast.reverse('episode_trailer_detail')

        if self.bonus:
            return self.podcast.reverse(
                'episode_bonus_detail', args=(self.number,)
            )

        return self.podcast.reverse('episode_detail', args=(self.number,))

    @property
    def player_html(self):
        for (regex, repl) in PLAYER_REGEXES:
            match = regex.match(self.enclosure_url)
            if match is not None:
                return render_to_string(
                    'podcasts/player.html',
                    {
                        'url': regex.sub(repl, self.enclosure_url)
                    }
                )

        return ''

    class Meta:
        unique_together = ('guid', 'podcast')
        ordering = ('-published',)


class Post(models.Model):
    objects = PostQuerySet.as_manager()

    def upload_image(self, filename):
        if self.podcast:
            return 'podcasts/%s/blog/%s%s' % (
                self.podcast.slug,
                self.slug,
                os.path.splitext(filename)[-1]
            )

        return 'blog/%s%s' % (
            self.slug,
            os.path.splitext(filename)[-1]
        )

    podcast = models.ForeignKey(
        Podcast,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        null=True,
        blank=True
    )

    author = models.ForeignKey(
        Host,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30)
    published = models.DateTimeField()
    image = models.ImageField(
        max_length=255,
        upload_to=upload_image,
        null=True,
        blank=True
    )

    summary = models.TextField()
    body = MarkdownxField(null=True, blank=True)

    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='blog_posts'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.podcast_id and settings.DOMAINS_OR_SLUGS == 'slugs':
            return '/%s/blog/%s/' % (self.podcast.slug, self.slug)

        return '/blog/%s/' % self.slug

    class Meta:
        unique_together = ('slug', 'podcast')
        ordering = ('-published',)


class Page(models.Model):
    def upload_image(self, filename):
        if self.podcast:
            return 'podcasts/%s/pages/%s%s' % (
                self.podcast.slug,
                self.slug,
                os.path.splitext(filename)[-1]
            )

        return 'pages/%s%s' % (
            self.slug,
            os.path.splitext(filename)[-1]
        )

    podcast = models.ForeignKey(
        Podcast,
        on_delete=models.CASCADE,
        related_name='pages',
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=30)
    ordering = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        max_length=255,
        upload_to=upload_image,
        null=True,
        blank=True
    )

    body = MarkdownxField(null=True, blank=True)
    menu_visible = models.BooleanField('show in menu', default=True)
    menu_title = models.CharField(
        'menu item title',
        max_length=50,
        null=True,
        blank=True
    )

    cta = models.BooleanField('highlight in menu')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.podcast_id and settings.DOMAINS_OR_SLUGS == 'slugs':
            return '/%s/%s/' % (self.podcast.slug, self.slug)

        return '/%s/' % self.slug

    class Meta:
        unique_together = ('slug', 'podcast')
        ordering = ('ordering',)
