from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import RedirectView

from aloisioimoveis.properties.models import Property

redirect_rent = RedirectView.as_view(pattern_name='rent', permanent=True)
redirect_buy = RedirectView.as_view(pattern_name='buy', permanent=True)
redirect_company = RedirectView.as_view(pattern_name='company', permanent=True)
redirect_contact = RedirectView.as_view(pattern_name='contact', permanent=True)


def redirect_record(request):
    try:
        prop = get_object_or_404(Property, pk=int(request.GET.get('id')))
        return redirect(prop.specific().get_absolute_url(), permanent=True)
    except (TypeError, ValueError):
        raise Http404()
