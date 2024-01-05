from django.test import TestCase
from .models import User, Application, Contact_information, Foreign_language, Work_experience, Reference_letter, Scholarship, Theses, Studies, Undergraduate, Postgraduate
from django.core.exceptions import ValidationError
from django.test import Client

# Create your tests here.

class UserTest(TestCase):
    
    def setUp(self):
        User.objects.create(username="marios", amka='12345678900', afm='123456789') #correct
        User.objects.create(username="stelios", amka='123456789', afm='123456789000') #incorrect

    def test_user_correct_amka(self):
        u = User.objects.get(username = "marios") #has correct amka
        self.assertIsNone(u.validate_amka(u.amka))

    def test_user_incorrect_amka(self):
        u = User.objects.get(username = "stelios") #has incorrect amka
        self.assertRaises(ValidationError, u.validate_amka, u.amka)    


    
    def test_user_correct_afm(self):
        u = User.objects.get(username = "marios") #has correct afm
        self.assertIsNone(u.validate_afm(u.afm))

    def test_user_incorrect_afm(self):
        u = User.objects.get(username = "stelios")
        self.assertRaises(ValidationError, u.validate_afm, u.afm)


class ApplicationTest(TestCase):

    def setUp(self):
        u = User.objects.create(username="marios")
        Application.objects.create(user=u)

    def test_create_application(self):
        app = Application.objects.get(pk = 1)
        self.assertEqual(app.__str__(), app.user.username)


class ContactInformationTest(TestCase):

    def setUp(self):
        u = User.objects.create(username="marios")   
        Contact_information.objects.create(user=u, home_number='2105863547', cell_number = '6975863547') #correct
        us = User.objects.create(username="stelios")  
        Contact_information.objects.create(user=us, home_number='210586354700', cell_number = '697586354700') #incorrect   

    def test_contact_information_correct(self):
        contact_info = Contact_information.objects.get(home_number='2105863547')
        self.assertIsNone(contact_info.validate_number(contact_info.home_number))    

    def test_contact_information_incorrect(self):  
        contact_info = Contact_information.objects.get(cell_number='697586354700')  
        self.assertRaises(ValidationError, contact_info.validate_number, contact_info.cell_number)


    def test_contact_information(self):
        contact_info = Contact_information.objects.get(pk = 1)
        self.assertEqual(contact_info.__str__(), contact_info.user.username)    



class ForeignLanguageTest(TestCase):
    
    def setUp(self):
        u = User.objects.create(username="marios")
        Foreign_language.objects.create(user=u, language = "english") #correct

    def test_foreign_language(self):
        foreign_language = Foreign_language.objects.get(pk = 1)
        self.assertEqual(foreign_language.__str__(), foreign_language.user.username)    


class WorkExperienceTest(TestCase):
    
    def setUp(self):
        u = User.objects.create(username="marios")
        Work_experience.objects.create(user=u, position = "junior web dev")

    def test_work_experience(self):
        work_experience = Work_experience.objects.get(pk = 1)
        self.assertEqual(work_experience.__str__(), work_experience.user.username)     


class ReferenceLetterTest(TestCase):
    
    def setUp(self):
        u = User.objects.create(username="marios")
        Reference_letter.objects.create(user=u, email = "tempemail@gmail.com")

    def test_reference_letter(self):
        reference_letter = Reference_letter.objects.get(pk = 1)
        self.assertEqual(reference_letter.__str__(), reference_letter.user.username)     


class ScholarshipTest(TestCase):
    
    def setUp(self):
        u = User.objects.create(username="marios")
        Scholarship.objects.create(user=u, educational_institution = "Harokopio")

    def test_scholarship(self):
        scholarship = Scholarship.objects.get(pk = 1)
        self.assertEqual(scholarship.__str__(), scholarship.user.username)     


class ThesesTest(TestCase):
    
    def setUp(self):
        u = User.objects.create(username="marios")
        Theses.objects.create(user=u, title = "some title")

    def test_theses(self):
        theses = Theses.objects.get(pk = 1)
        self.assertEqual(theses.__str__(), theses.user.username)    


class UndergraduateStudiesTest(TestCase):
    
    def setUp(self):
        u = User.objects.create(username="marios")
        Undergraduate.objects.create(user=u, univercity = "Harokopio")

    def test_undergraduate_studies(self):
        undergraduate = Undergraduate.objects.get(pk = 1)
        self.assertEqual(undergraduate.__str__(), undergraduate.user.username)    


class PostgraduateStudiesTest(TestCase):
    
    def setUp(self):
        u = User.objects.create(username="marios")
        Postgraduate.objects.create(user=u, univercity = "Harokopio")

    def test_undergraduate_studies(self):
        postgraduate = Postgraduate.objects.get(pk = 1)
        self.assertEqual(postgraduate.__str__(), postgraduate.user.username)         


class ViewTestNotLoggedIn(TestCase):

    def setUp(self):
        self.c = Client()


    def test_view_login(self):
        response = self.c.get("/login/")
        self.assertEqual(response.status_code, 200)    
        self.assertTemplateUsed(response, 'main/login_register.html')

    def test_view_register(self):
        response = self.c.get("/register/")
        self.assertEqual(response.status_code, 200)    
        self.assertTemplateUsed(response, 'main/login_register.html') 

    def test_view_home(self):
        response = self.c.get("")
        self.assertEqual(response.status_code, 200)    
        self.assertTemplateUsed(response, 'main/base.html') 

    def test_view_register_error(self):
        c = Client()
        response = c.post("/register/", {"username": "marios", "first_name": "marios", 
                                         "last_name": "pap", "email": "mpap@gmail.com", "password1": "1234", "password2": "1234"})
        self.assertEqual(response.status_code, 200)
        
    def test_view_register(self):
        c = Client()
        response = c.post("/register/", {"username": "mariosp", "first_name": "mariosp", 
                                         "last_name": "pap", "email": "mpap@gmail.com", "password1": "ii123456", "password2": "ii123456"})
        self.assertRedirects(response, '/')    

            

class ViewTestLoggedIn(TestCase): 
    
    def setUp(self):
        User.objects.create_user(username='marios', password='12345')
        self.c = Client()    
        self.c.login(username='marios', password='12345')         
        
    def test_view_logout(self):
        response = self.c.get("/logout/")
        self.assertRedirects(response, '/') 

    def test_view_create_application(self):
        response = self.c.get("/create-application/")
        self.assertEqual(response.status_code, 200)    
        self.assertTemplateUsed(response, 'main/application_form.html')
         
    def test_view_login(self):
        response = self.c.get("/login/")
        self.assertRedirects(response, '/')    

    def test_view_register(self):
        response = self.c.get("/register/")
        self.assertRedirects(response, '/')   
        

         
            