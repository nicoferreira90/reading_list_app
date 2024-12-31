from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Book


class AboutPageViewTest(TestCase):
    """Test the about page view."""

    def test_about_page_status_code(self):
        response = self.client.get(reverse("about_page"))
        self.assertEqual(response.status_code, 200)

    def test_about_page_template(self):
        response = self.client.get(reverse("about_page"))
        self.assertTemplateUsed(response, "reading/about.html")


class BookIntegrationTest(TestCase):
    """Test the creation and updating of a book."""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")

    def test_create_and_update_book(self):
        # Create a book
        response = self.client.post(
            reverse("add_book"),
            {"book-title": "Test Book", "book-author": "Test Author"},
        )
        self.assertEqual(response.status_code, 200)

        # Verify the book was created
        book = Book.objects.get(title="Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.book_owner, self.user)
        self.assertFalse(book.finished)

        # Update the book
        book.finished = True
        book.finished_date = datetime.now()
        book.rating = "5 stars"
        book.save()

        # Verify the book's fields were updated
        updated_book = Book.objects.get(title="Test Book")
        self.assertTrue(updated_book.finished)
        self.assertIsNotNone(updated_book.finished_date)
        self.assertEqual(updated_book.rating, "5 stars")


class BookIntegrationTest2(TestCase):
    """Test the creation and deletion of a book."""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.client.login(username="testuser", password="12345")

    def test_create_and_delete_book(self):
        # Create a book
        response = self.client.post(
            reverse("add_book"),
            {"book-title": "Test Book", "book-author": "Test Author"},
        )
        self.assertEqual(response.status_code, 200)

        # Verify the book was created
        book = Book.objects.get(title="Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.book_owner, self.user)

        # Delete the book
        response = self.client.delete(reverse("delete_book", args=[book.pk]))
        self.assertEqual(response.status_code, 200)

        # Verify the book was deleted
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(title="Test Book")
