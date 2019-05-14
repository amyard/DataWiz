from django import forms
from datetime import date


class SearchDateForm(forms.Form):
    start_period = forms.DateField(label = 'Начальная дата', widget = forms.DateInput(format = ('%Y-%m-%d'), attrs = {'type':'date'}))
    end_date = forms.DateField(label = 'Конечная дата', widget = forms.DateInput(format = ('%Y-%m-%d'), attrs = {'type':'date'}))


    def clean(self):
        start_period = self.cleaned_data['start_period']
        end_date = self.cleaned_data['end_date']

        if start_period > date.today() or end_date > date.today():
            raise forms.ValidationError('Вы не можете использовать дату больше Сегодняшней даты.')

        if start_period == end_date:
            raise forms.ValidationError('Для корректого отобржения статистики конечная дата должна быть больше хотя бы на один день, чем начальная дата.')

        if start_period > end_date:
            raise forms.ValidationError('Начальная дата не может быть больше Конечной даты.')