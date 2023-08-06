from django.conf import settings as django
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt
from pico.conf import settings as pico
from .views import PodcastListView, PodcastPingView, ContentListView


urlpatterns = (
    path('admin/rq/', include('django_rq.urls')),
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('~/ping/', csrf_exempt(PodcastPingView.as_view()), name='api_ping'),
    path('~/content/', ContentListView.as_view(), name='content_list'),
    path('', PodcastListView.as_view(), name='podcast_list')
)

if django.DEBUG:
    from django.views.static import serve as static_serve

    urlpatterns += (
        re_path(
            r'^media/(?P<path>.*)$',
            static_serve,
            {
                'document_root': django.MEDIA_ROOT
            }
        ),
    )


if pico.DOMAINS_OR_SLUGS == 'slugs':
    urlpatterns += (
        path('<podcast>/', include('pico.podcasts.urls')),
    )
