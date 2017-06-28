from django.conf import settings
from django.core import mail
from django.shortcuts import resolve_url as r
from django.test import TestCase

from aloisioimoveis.core.forms import ContactForm


class ContactViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('contact'))

    def test_get(self):
        """GET /contato/ should return 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use contact.html"""
        self.assertTemplateUsed(self.response, 'contact.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 4),
                ('type="email"', 1),
                ('<textarea', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have contact form"""
        form = self.response.context['form']
        self.assertIsInstance(form, ContactForm)


class ContactFormPostValid(TestCase):
    def setUp(self):
        self.data = dict(name='Thiago Rossener',
                         email='thiago@rossener.com',
                         phone='12-981491771',
                         message='Olá')
        self.response = self.client.post(r('contact'), self.data)

    def test_post(self):
        """Valid post should show a success message"""
        self.assertContains(self.response,
                            '<strong>Mensagem enviada com sucesso</strong><br />'
                            'Retornaremos assim que possível.<br />Obrigado!')

    def test_send_email(self):
        """Valid post should send an email"""
        self.assertEqual(len(mail.outbox), 1)

    def test_email_subject(self):
        """Email should have contact name in subject"""
        subject = mail.outbox[0].subject
        self.assertTrue(self.data['name'] in subject)

    def test_email_from(self):
        """Email should have contact email in from"""
        from_email = mail.outbox[0].from_email
        self.assertEqual(self.data['email'], from_email)

    def test_email_to(self):
        """Email should be sent to default email"""
        to = mail.outbox[0].to
        self.assertIn(settings.DEFAULT_TO_EMAIL, to)

    def test_email_body(self):
        """Email should contain the contact fields values in body"""
        body = mail.outbox[0].body
        for key, value in self.data.items():
            with self.subTest():
                self.assertTrue(value in body)

    def test_form_content(self):
        """Form should be empty when the message is sent successfully"""
        form = self.response.context['form']
        self.assertFalse(form.is_bound)


class ContactFormPostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post(r('contact'))

    def test_not_send_email(self):
        """Invalid post should not send an email"""
        self.assertEqual(len(mail.outbox), 0)

    def test_form_content(self):
        """Form should contain all the filled data"""
        form = self.response.context['form']
        self.assertTrue(form.is_bound)


class ContactFormFieldsValidation(TestCase):
    def test_phone_is_optional(self):
        """Phone field should be optional"""
        data = dict(name='Thiago Rossener',
                    email='thiago@rossener.com',
                    message='Olá')
        response = self.client.post(r('contact'), data)
        form = response.context['form']
        self.assertEqual(len(form.errors), 0)
