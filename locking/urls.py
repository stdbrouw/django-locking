from django.conf.urls.defaults import patterns
from warnings import warn


warn("The use of 'locking.urls' is deprecated and is no longer needed.",
    DeprecationWarning)


# We need at least one url inside urlpatterns to keep include('locking.urls')
# from throwing an exception
urlpatterns = patterns('',
    (r'jsi18n/$', 'django.views.i18n.javascript_catalog', {'packages': 'locking'}),
)
