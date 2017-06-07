from django.test import TestCase, Client
from django.contrib.auth.models import User
from Application.models import UserProfile, Section


class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="example", password="example", email="example@example.com")
        UserProfile.objects.create(user=User.objects.get(username="example"))

    def test_login(self):
        c = Client()
        UserProfile.objects.get(user__username="example")
        response = c.login(username='example', password='example')
        self.assertTrue(response)


class IndexTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="example", password="example", email="example@example.com")
        UserProfile.objects.create(user=User.objects.get(username="example"))

    def test_main_page(self):
        c = Client()
        response = c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_login_index(self):
        c = Client()
        c.login(username="example", password="example")
        response = c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_not_login_index(self):
        c = Client()
        response = c.get("/item/list/")
        self.assertRedirects(response, "/login/?next=/item/list/", fetch_redirect_response=False)


class SectionTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="example", password="example", email="example@example.com")
        profile = UserProfile.objects.create(user=User.objects.get(username="example"))
        Section.objects.create(title='Example', description='Example', user=profile)

    def test_create_section(self):
        c = Client()
        c.login(username="example", password="example")

        logs_before = Section.objects.all().count()

        response = c.post("/feed/create/", {
            "url": "http://www.feedforall.com/sample-feed.xml",
            "section": "RSS Example",
        })
        self.assertEquals(response.status_code, 302)

        section_last = Section.objects.all().last()
        self.assertEquals(section_last.title, "RSS Example")

        logs_after = Section.objects.all().count()
        self.assertEquals(logs_before + 1, logs_after)

    def test_edit_section(self):
        c = Client()
        c.login(username="example", password="example")
        section = Section.objects.all().last()

        response = c.post("/section/edit/{}/".format(section.id), {
            "title": section.title,
            "description": "This is an example",
        })
        self.assertEquals(response.status_code, 302)

        section_edit = Section.objects.get(id=section.id)
        self.assertEquals(section.title, section_edit.title)
        self.assertNotEquals(section.description, section_edit.description)
