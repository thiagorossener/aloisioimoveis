from django.conf import settings
from django.core import mail
from django.shortcuts import resolve_url as r
from django.test import TestCase
from model_mommy import mommy

from aloisioimoveis.core.forms import ContactForm
from aloisioimoveis.properties.models import House, Property


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
                ('<input', 6),
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


class ContactFormPostValidTest(TestCase):
    def setUp(self):
        self.data = get_form_data()
        self.response = self.client.post(r('contact'), self.data)

    def test_success_message(self):
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
        """Email should have default email in from"""
        from_email = mail.outbox[0].from_email
        self.assertEqual(settings.DEFAULT_TO_EMAIL, from_email)

    def test_email_to(self):
        """Email should be sent to default email"""
        to = mail.outbox[0].to
        self.assertIn(settings.DEFAULT_TO_EMAIL, to)

    def test_email_reply_to(self):
        """Email should have contact email in reply_to"""
        reply_to = mail.outbox[0].reply_to
        self.assertIn(self.data['email'], reply_to)

    def test_email_body(self):
        """Email should contain the contact fields values in body"""
        body = mail.outbox[0].body
        for key, value in self.data.items():
            with self.subTest():
                self.assertTrue(value in body)

    def test_empty_form(self):
        """Form should be empty when the message is sent successfully"""
        form = self.response.context['form']
        self.assertFalse(form.is_bound)


class ContactFormPostInvalidTest(TestCase):
    def setUp(self):
        self.response = self.client.post(r('contact'))

    def test_email_not_sent(self):
        """Invalid post should not send an email"""
        self.assertEqual(len(mail.outbox), 0)

    def test_filled_form(self):
        """Form should contain all the filled data"""
        form = self.response.context['form']
        self.assertTrue(form.is_bound)


class ContactFormFieldsValidationTest(TestCase):
    def test_phone_is_optional(self):
        """Phone field should be optional"""
        data = get_form_data(phone='')
        response = self.client.post(r('contact'), data)
        form = response.context['form']
        self.assertEqual(len(form.errors), 0)


class ContactFormFromRecordViewTest(TestCase):
    def test_load_record_data(self):
        """Should load a record id and type in hidden inputs"""
        contents = [
            ('type="hidden"', 2),
            ('name="record_id"', 1),
            ('value="999"', 1),
            ('name="record_type"', 1),
            ('value="casa"', 1),
        ]
        response = self.client.get(r('contact'), {'id': 999, 'tipo': 'casa'})
        for content, count in contents:
            with self.subTest():
                self.assertContains(response, content, count)

    def test_link_on_email(self):
        """Should send email with a link to the record view"""
        house = mommy.make(House, pk=777)
        self.submit_form(record_id=house.pk, record_type=Property.HOUSE)
        self.assertTrue(house.get_absolute_url() in mail.outbox[0].body)

    def test_non_existent_record(self):
        """Should not send link when the record does not exist"""
        self.submit_form(record_id=1234, record_type=Property.HOUSE)
        self.assertFalse('Clique aqui para visualizar' in mail.outbox[0].body)

    def test_invalid_record_data(self):
        """Should show message with error when record data is invalid"""
        response = self.submit_form(record_id='invalid')
        self.assertContains(response, 'Ocorreu um erro interno. '
                                      'Por favor, tente novamente mais tarde.')

    def submit_form(self, **kwargs):
        return self.client.post(r('contact'), get_form_data(**kwargs))


class ContactEmailHtmlTest(TestCase):
    def setUp(self):
        data = get_form_data(phone='', message='Fala rapaz\naqui é da quebrada')
        self.client.post(r('contact'), data)
        self.email_body = mail.outbox[0].body

    def test_br_in_message(self):
        """Email message should break lines"""
        self.assertTrue('Fala rapaz<br />aqui é da quebrada' in self.email_body)

    def test_phone_not_informed(self):
        """Should show a message when the phone isn't informed"""
        self.assertTrue('Telefone: <strong>Não informado</strong>' in self.email_body)


def get_form_data(name='Thiago Rossener', email='thiago@rossener.com',
                  phone='12-981491771', message='Olá', **kwargs):
    form_data = dict(name=name, email=email, phone=phone, message=message)
    form_data.update(**kwargs)
    return form_data
