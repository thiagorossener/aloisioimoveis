from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        error_messages={'required': 'Por favor digite o seu nome'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Seu nome',
        })
    )
    email = forms.EmailField(
        error_messages={'required': 'Por favor digite o seu email'},
        widget=forms.EmailInput(attrs={
            'placeholder': 'Seu email',
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Seu telefone (opcional)',
        })
    )
    message = forms.CharField(
        error_messages={'required': 'Por favor digite a sua mensagem'},
        widget=forms.Textarea(attrs={
            'placeholder': 'Sua mensagem',
        })
    )
    record_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput()
    )
    record_type = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
