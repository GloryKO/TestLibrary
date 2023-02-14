from django.test import TestCase,SimpleTestCase
from django.urls import reverse
from django.urls.base import resolve
from .views import home
from .forms import AddBookForm
# Create your tests here.
from .models import Catalogue 
class CatalogueFormTests(SimpleTestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_book_form(self):
        form = self.response.context.get('add_book_form')
        self.assertIsInstance(form, AddBookForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_bootstrap_class_used_for_default_styling(self):
        form = self.response.context.get('add_book_form')
        self.assertIn('class="form-control"', form.as_p())

    def test_book_form_validation_for_blank_items(self):
        add_book_form = AddBookForm(
            data={'title': '', 'ISBN': '', 'author': '', 'price': '', 'availability': ''}
            )
        self.assertFalse(add_book_form.is_valid())


class ElibraryURLsTest(SimpleTestCase):
    def test_homepage_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        
    def test_root_url_resloves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home)

class CatalogueModelTest(TestCase):

    def setUp(self): #sets up before performing any action on the model
        self.book = Catalogue(
            title= 'First Title',
            ISBN ='19192-38484-8848',
            author='glory kolade',
            price = '9.99',
            availability ='True',
        )
    
    
    def test_create_book(self):
        self.assertIsInstance(self.book,Catalogue) #check if the book is an instance of the Catalogue model 
    
    def test_str_representation(self): #test the string representation of the model
        self.assertEquals(str(self.book.title),'First Title')
    
    def test_saving_and_retrieving_books(self): #test the number of books saved and retrieved from the database
        first_book = Catalogue()
        first_book.title = 'FirstTitle'
        first_book.ISBN = '1939-4949-4848'
        first_book.author ='glory kolade'
        first_book.price='9.90'
        first_book.availability='True'
        first_book.save()

        second_book = Catalogue()
        second_book.title = 'First Title'
        second_book.ISBN = '1939-4949-4848'
        second_book.author ='glory kolade'
        second_book.price='9.90'
        second_book.availability='True'
        second_book.save()

        saved_books = Catalogue.objects.all()
        self.assertEqual(saved_books.count(),2)
        first_saved_book = saved_books[0]
        second_saved_book = saved_books[1]
        self.assertEqual(first_saved_book.title,'FirstTitle')
        self.assertEqual(second_saved_book.author, 'glory kolade')
        
