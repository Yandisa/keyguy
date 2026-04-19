from django import forms
from .models import QuoteRequest

SERVICE_CHOICES = [
    ('', 'Select a service'),
    ('Spare key',             'Spare key'),
    ('Key programming',       'Key programming'),
    ('Key cutting',           'Key cutting'),
    ('Vehicle diagnostics',   'Vehicle diagnostics'),
    ('Mobile diagnostics',    'Mobile diagnostics'),
    ('Key or remote repair',  'Key or remote repair'),
    ('Other / not sure',      'Other / not sure'),
]

class QuoteForm(forms.ModelForm):
    service = forms.ChoiceField(choices=SERVICE_CHOICES)

    class Meta:
        model  = QuoteRequest
        fields = ['name', 'phone', 'vehicle', 'service', 'area', 'message']
        widgets = {
            'name':    forms.TextInput(attrs={'placeholder': 'Full name'}),
            'phone':   forms.TextInput(attrs={'placeholder': 'Cell number', 'type': 'tel'}),
            'vehicle': forms.TextInput(attrs={'placeholder': 'Make, model and year (e.g. VW Polo 2019)'}),
            'area':    forms.TextInput(attrs={'placeholder': 'Suburb or area (e.g. Midrand)'}),
            'message': forms.Textarea(attrs={'placeholder': 'Anything else we should know?', 'rows': 4}),
        }
