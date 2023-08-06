from django import forms
from gnd.widgets import GndAcWidget


class GndFormField(forms.CharField):
    widget = GndAcWidget(
        options={
            'placeholder': 'Search the GND',
            'multiple': False,
            'maximum-selection-length': 21,
            'minimumInputLength': 3,
        }
    )


class GndForm(forms.Form):
    gnd_gnd_id = GndFormField(
        label='GND',
        widget=GndAcWidget(
            options={'placeholder': 'Search the GND'}
        ),
    )


class GndModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GndModelForm, self).__init__(*args, **kwargs)
        if kwargs['instance']:
            try:
                initial = kwargs['instance'].gnd_gnd_id.split('/')[-1]
            except AttributeError:
                initial = None
            self.fields['hidden_gnd'] = forms.CharField(
                initial=initial,
                required=False,
                widget=forms.HiddenInput()
            )
        else:
            self.fields['hidden_gnd'] = forms.CharField(
                required=False,
                widget=forms.HiddenInput()
            )
