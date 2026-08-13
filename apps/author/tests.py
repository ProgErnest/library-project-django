from django.test import TestCase
from apps.author.models import Author

# Create your tests here.
class AuthorTests(TestCase):

    def setUp(self):
        Author.objects.create(name="NIOB", surname="Bio", birthday="1986-10-10")

    def test_result(self):
        author = Author.objects.get(name="NIOB")
        self.assertEqual(str(author.name),"NIOB")