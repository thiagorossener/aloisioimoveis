from itertools import chain
from operator import attrgetter

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render
from django.template.loader import render_to_string

from aloisioimoveis.core.forms import ContactForm
from aloisioimoveis.properties.models import House, Apartment, Commercial, Land, Property


def home(request):
    models = (House, Apartment, Commercial, Land)
    queries = (model.objects.filter(featured=True) for model in models)
    properties = sorted(chain(*queries),
                        key=attrgetter('updated_at'),
                        reverse=True)[:3]
    context = {
        'properties': properties
    }
    return render(request, 'index.html', context)


def rent(request):
    models = (House, Apartment, Commercial, Land)
    queries = [model.objects.filter(intent=Property.RENT) for model in models]

    # Sorting
    sort_key = request.GET.get('ordem')
    if sort_key == 'preco':
        properties_list = sorted(chain(*queries), key=attrgetter('price'))
    elif sort_key == '-preco':
        properties_list = sorted(chain(*queries), key=attrgetter('price'), reverse=True)
    else:
        properties_list = sorted(chain(*queries), key=attrgetter('updated_at'), reverse=True)

    # Pagination
    page = request.GET.get('pagina', 1)
    paginator = Paginator(properties_list, 10)
    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)

    context = {
        'properties': properties,
        'params': request.GET.dict(),
    }
    return render(request, 'rent_list.html', context)


def buy(request):
    # Get all properties
    models = (House, Apartment, Commercial, Land)
    queries = (model.objects.filter(intent=Property.BUY) for model in models)

    # Sorting
    sort_key = request.GET.get('ordem')
    if sort_key == 'preco':
        properties_list = sorted(chain(*queries), key=attrgetter('price'))
    elif sort_key == '-preco':
        properties_list = sorted(chain(*queries), key=attrgetter('price'), reverse=True)
    else:
        properties_list = sorted(chain(*queries), key=attrgetter('updated_at'), reverse=True)

    # Pagination
    page = request.GET.get('pagina', 1)
    paginator = Paginator(properties_list, 10)
    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)

    context = {
        'properties': properties,
        'params': request.GET.dict(),
    }
    return render(request, 'buy_list.html', context)


def search(request):
    num_record = request.GET.get(Property.RECORD)
    if num_record is not None:
        # Record Number
        try:
            models = [House, Apartment, Commercial, Land]
            queries = [m.objects.filter(num_record=int(num_record)) for m in models]
            queryset = list(chain(*queries))
            if len(queryset) == 0:
                raise Http404('No property matches the record number.')
        except ValueError:
            raise Http404('No property matches the record number.')
    else:
        # Property Type
        property_type = request.GET.get(Property.TYPE)
        if property_type == Property.HOUSE:
            manager = House.objects
        elif property_type == Property.APARTMENT:
            manager = Apartment.objects
        elif property_type == Property.COMMERCIAL:
            manager = Commercial.objects
        elif property_type == Property.LAND:
            manager = Land.objects
        else:
            raise Http404('No property matches the type.')

        # Intent
        intent = request.GET.get(Property.INTENT)
        if intent == Property.RENT:
            queryset = manager.filter(intent=Property.RENT)
        elif intent == Property.BUY:
            queryset = manager.filter(intent=Property.BUY)
        else:
            raise Http404('No property matches the intent.')

        # City
        try:
            city_id = int(request.GET.get(Property.CITY, 0))
        except ValueError:
            city_id = 0
        if city_id > 0:
            queryset = queryset.filter(city__pk=city_id)

        # Neighborhood
        try:
            neighborhood_id = int(request.GET.get(Property.NEIGHBORHOOD, 0))
        except ValueError:
            neighborhood_id = 0
        if neighborhood_id > 0:
            queryset = queryset.filter(neighborhood__pk=neighborhood_id)

    context = {
        'results': list(queryset),
        'params': request.GET.dict(),
    }
    return render(request, 'search.html', context)


def company(request):
    return render(request, 'company.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            subject = 'Contato - De: {}'.format(form.cleaned_data['name'])
            from_ = form.cleaned_data['email']
            to = settings.DEFAULT_TO_EMAIL

            context = form.cleaned_data
            record_id, record_type = form.cleaned_data['record_id'], form.cleaned_data['record_type']
            if record_id and record_type:
                try:
                    if record_type == Property.HOUSE:
                        context['url'] = request.build_absolute_uri(House.objects.get(pk=record_id).get_absolute_url())
                    elif record_type == Property.APARTMENT:
                        context['url'] = Apartment.objects.get(pk=record_id).get_absolute_url()
                    elif record_type == Property.COMMERCIAL:
                        context['url'] = Commercial.objects.get(pk=record_id).get_absolute_url()
                    elif record_type == Property.LAND:
                        context['url'] = Land.objects.get(pk=record_id).get_absolute_url()
                except ObjectDoesNotExist:
                    pass

            content = render_to_string('core/contact_email.html', context)

            email = EmailMultiAlternatives(subject, content, from_, [to])
            email.attach_alternative(content, "text/html")
            email.send()

            # Clean form
            form = ContactForm()

            # Show success message
            messages.success(request, '<strong>Mensagem enviada com sucesso</strong><br />'
                                      'Retornaremos assim que possível.<br />Obrigado!')

        elif form.errors.get('record_id') or form.errors.get('record_type'):
            # Show error message
            messages.error(request, 'Ocorreu um erro interno. '
                                    'Por favor, tente novamente mais tarde.')

    else:
        form = ContactForm()
        if request.GET.get('id') and request.GET.get('tipo'):
            form.fields['record_id'].initial = request.GET.get('id')
            form.fields['record_type'].initial = request.GET.get('tipo')

    context = {
        'form': form
    }
    return render(request, 'contact.html', context)
