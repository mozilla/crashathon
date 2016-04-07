from django import forms

DATE_INPUT_FORMATS = ('%Y-%m-%d', '%Y%m%d')


class StatsForm(forms.Form):
    start = forms.DateField(required=True, input_formats=DATE_INPUT_FORMATS)
    end = forms.DateField(required=True, input_formats=DATE_INPUT_FORMATS)
