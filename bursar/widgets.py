from django import forms
from django.conf import settings

class DatePickerWidget(forms.DateInput):
    class Media:
        js = ('/assets/bursar/js/date-picker.js',)

    def __init__(self, attrs={}, format=None):
        super(DatePickerWidget, self).__init__(attrs={'class':'dpDateField','size':'10'}, format=format)
