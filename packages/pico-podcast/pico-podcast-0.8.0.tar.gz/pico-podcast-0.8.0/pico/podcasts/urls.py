from django.urls import path, re_path
from django.conf import settings
from pico.podcasts.views import (
    EpisodeListView, SeasonView, EpisodeDetailView,
    PostListView, PostDetailView, PageDetailView, FeedRedirectView,
    PodcastStylesheetView
)


urlpatterns = (
    path('', EpisodeListView.as_view(), name='episode_list'),
    path('s<int:number>/', SeasonView.as_view(), name='season'),
    path(
        's<int:season>/e<int:number>/',
        EpisodeDetailView.as_view(),
        name='season_episode_detail'
    ),
    path(
        's<int:season>/trailer/',
        EpisodeDetailView.as_view(trailer=True),
        name='season_episode_trailer_detail'
    ),
    path(
        's<int:season>/e<int:number>a/',
        EpisodeDetailView.as_view(bonus=True),
        name='season_episode_bonus_detail'
    ),
    path(
        '<int:number>/',
        EpisodeDetailView.as_view(),
        name='episode_detail'
    ),
    path(
        'trailer/',
        EpisodeDetailView.as_view(trailer=True),
        name='episode_trailer_detail'
    ),
    path(
        '<int:number>/b',
        EpisodeDetailView.as_view(bonus=True),
        name='episode_bonus_detail'
    ),
    path(
        'blog/',
        PostListView.as_view(),
        name='blogpost_list'
    ),
    path(
        'blog/<slug>/',
        PostDetailView.as_view(),
        name='blogpost_detail'
    ),
    path('rss/', FeedRedirectView.as_view(), name='feed_redirect'),
    path('css/', PodcastStylesheetView.as_view(), name='feed_stylesheet')
)


if settings.DEBUG:
    from django.views.static import serve as static_serve

    urlpatterns += (
        re_path(
            r'^media/(?P<path>.*)$',
            static_serve,
            {
                'document_root': settings.MEDIA_ROOT
            }
        ),
    )


urlpatterns += (
    path(
        '<slug>/',
        PageDetailView.as_view(),
        name='page_detail'
    ),
)
