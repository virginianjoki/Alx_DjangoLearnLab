from django.test import TestCase
from .models import Post

class PostSearchTest(TestCase):
    def setUp(self):
        Post.objects.create(title="Django tutorial", content="Learn Django", tags="django")
        Post.objects.create(title="Flask tutorial", content="Learn Flask", tags="flask")

    def test_search(self):
        response = self.client.get('/search/?q=django')
        self.assertContains(response, "Django tutorial")
        self.assertNotContains(response, "Flask tutorial")

