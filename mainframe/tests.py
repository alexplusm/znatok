from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from .views import site

class SiteTests(TestCase):
    def test_site_view_status_code(self):
        url = reverse('site')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_site_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, site)