from dal import autocomplete
from django import forms

from aloisioimoveis.locations.models import Neighborhood, City
from aloisioimoveis.properties.models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete'),
            'neighborhood': autocomplete.ModelSelect2(url='neighborhood-autocomplete', forward=['city'])
        }
