from django.contrib.auth.models import User
from django.test import TestCase

from aloisioimoveis.locations.models import City, Neighborhood
from aloisioimoveis.properties.models import Photo, Land


class PhotoModelTest(TestCase):
    def setUp(self):
        property = self.create_property()
        self.obj = Photo(
            property=property,
            image_url='photo.jpg',
            order=1,
        )
        self.obj.save()

    def test_create(self):
        """Should create a Photo"""
        self.assertTrue(Photo.objects.exists())

    def test_str(self):
        """str() must return the image url"""
        self.assertEqual('photo.jpg', str(self.obj))

    def create_property(self):
        city = self.create_city()
        neighborhood = self.create_neighborhood(city=city)
        user = self.create_user()

        property = Land(
            price=1000,
            city=city,
            neighborhood=neighborhood,
            user=user,
        )
        property.save()
        return property

    def create_city(self):
        city = City(
            name='Taubaté'
        )
        city.save()
        return city

    def create_neighborhood(self, city):
        neighborhood = Neighborhood(
            name='Centro',
            city=city
        )
        neighborhood.save()
        return neighborhood

    def create_user(self):
        user = User(
            first_name='Thiago',
            last_name='Rossener',
            email='thiago@rossener.com'
        )
        user.save()
        return user
