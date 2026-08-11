from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from .models import Book

class BookDetailViewTest(TestCase):

    def test_book_detail_returns_200(self):
        book = Book.objects.create(
            title="Django avancé",
            total_copies=10,
            unavailable_copies=3,
            # ...
        )

        response = self.client.get(
            reverse("book_detail", kwargs={"pk": book.pk})
        )

        self.assertEqual(response.status_code, 200)