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
from aloisioimoveis.core.helpers import is_recaptcha_valid


def home(request):
    properties = Property.objects.filter(featured=True).order_by('-updated_at')[:3]
    context = {
        'properties': properties
    }
    return render(request, 'index.html', context)


def get_context(request, intent):
    sort_key = request.GET.get('ordem')
    sort_dict = {
        'preco': 'price',
        '-preco': '-price',
    }
    props = Property.objects.filter(intent=intent).order_by(sort_dict.get(sort_key, '-id'))

    page = request.GET.get('pagina', 1)
    paginator = Paginator(props, 10)
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
    return context


def rent(request):
    return render(request, 'rent_list.html', get_context(request, Property.RENT))


def buy(request):
    return render(request, 'buy_list.html', get_context(request, Property.BUY))


def search(request):
    num_record = request.GET.get(Property.RECORD)
    if num_record is not None:
        # Record Number
        try:
            results = Property.objects.filter(num_record=int(num_record))
            if len(results) == 0:
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

        # Sorting
        sort_key = request.GET.get('ordem')
        sort_dict = {
            'preco': 'price',
            '-preco': '-price',
        }
        queryset = queryset.order_by(sort_dict.get(sort_key, '-updated_at'))

        # Pagination
        page = request.GET.get('pagina', 1)
        paginator = Paginator(queryset, 10)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

    context = {
        'results': results,
        'params': request.GET.dict(),
    }
    return render(request, 'search.html', context)


def company(request):
    return render(request, 'company.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if is_recaptcha_valid(request):
                # Send email
                subject = 'Contato - De: {}'.format(form.cleaned_data['name'])
                from_ = settings.DEFAULT_TO_EMAIL
                reply_to = form.cleaned_data['email']
                to = settings.DEFAULT_TO_EMAIL

                context = form.cleaned_data
                record_id, record_type = form.cleaned_data['record_id'], form.cleaned_data['record_type']
                if record_id and record_type:
                    try:
                        if record_type == Property.HOUSE:
                            context['url'] = request.build_absolute_uri(House.objects.get(pk=record_id).get_absolute_url())
                        elif record_type == Property.APARTMENT:
                            context['url'] = request.build_absolute_uri(Apartment.objects.get(pk=record_id).get_absolute_url())
                        elif record_type == Property.COMMERCIAL:
                            context['url'] = request.build_absolute_uri(Commercial.objects.get(pk=record_id).get_absolute_url())
                        elif record_type == Property.LAND:
                            context['url'] = request.build_absolute_uri(Land.objects.get(pk=record_id).get_absolute_url())
                    except ObjectDoesNotExist:
                        pass

                content = render_to_string('core/contact_email.html', context)

                email = EmailMultiAlternatives(subject, content, from_, [to], reply_to=[reply_to])
                email.attach_alternative(content, "text/html")
                email.send()

                # Clean form
                form = ContactForm()

                # Show success message
                messages.success(request, '<strong>Mensagem enviada com sucesso</strong><br />'
                                        'Retornaremos assim que possível.<br />Obrigado!')

            else:
                # Show error message
                messages.error(request, 'Ocorreu um erro. '
                                        'reCAPTCHA inválido. Por favor tente novamente.')

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


def credpago_rent(request):
    return render(request, 'credpago_rent.html')
