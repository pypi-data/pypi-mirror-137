import datetime

from django import forms
from django.forms import widgets
from django_kirui.widgets import CheckboxSwitch, SimpleFileInput
from kirui_devserver.backend.models import Topic, Activity


class SampleForm(forms.ModelForm):
    elso = forms.CharField(label='Első mező', required=True, disabled=False, initial='charfield')
    masodik = forms.ChoiceField(label='Második mező', choices=[(None, '-----------------'), (1, 'One'), (2, 'Two'), (3, 'Three')], initial=1, disabled=False)
    harmadik = forms.MultipleChoiceField(label='Harmadik', choices=[(1, "One\\aaaasdfsdfsdf'"), (2, 'Two'), (3, 'Three')], initial=[2, 3],
                                         widget=widgets.CheckboxSelectMultiple, disabled=False, required=True)
    negyedik = forms.BooleanField(label='Negyedik mező', widget=CheckboxSwitch, disabled=False)
    otodok = forms.CharField(label='Ötödik', widget=widgets.Textarea)
    hatodik = forms.IntegerField(label='Hatodik', disabled=False)
    hetedik = forms.DateField(label='Hetedik', disabled=False)
    nyolcadik = forms.FileField(label='Nyolcadik', widget=SimpleFileInput)

    class Meta:
        model = Activity
        fields = [] #'topics', 'reason'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['elso'].initial = str(datetime.datetime.now())


class FilterForm(forms.Form):
    field = forms.CharField(label='Filter field', required=False)
