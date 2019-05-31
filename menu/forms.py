from django import forms

from .models import Menu


class MenuForm(forms.ModelForm):

    expiration_date = forms.DateField(
        help_text='valid date formats are YYYY-MM-DD, MM/DD/YYYY, MM/DD/YY')

    def clean_season(self):
        data = self.cleaned_data['season']
        season = ['autumn', 'fall', 'winter', 'spring', 'summer']
        if data.lower() not in season[:]:
            raise forms.ValidationError('you have not entered a proper'
                                        ' season please do so')
        return data

    class Meta:
        model = Menu
        exclude = ('created_date',)
