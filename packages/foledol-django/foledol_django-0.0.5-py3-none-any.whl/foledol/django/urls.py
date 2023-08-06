from django.conf.urls import url

from foledol.django.views import logs

app_name = "django"

urlpatterns = [
    url(r'logs', logs.log_list, name='logs'),
    url(r'log_plot_today', logs.log_plot_today, name='log_plot_today'),
    url(r'log_plot', logs.log_plot, name='log_plot'),
    url(r'log_events', logs.log_events, name='log_events'),
    url(r'log_update/(?P<pk>\d+)', logs.log_update, name='log_update')
]


