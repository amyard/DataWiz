from django.shortcuts import render
from django.views.generic import View

from core.implement.forms import SearchDateForm

import datetime



class MainPageView(View):
    template_name = 'implement/main.html'
    form = SearchDateForm

    def get(self, request, *args, **kwargs):
        context = {
            'form':self.form,
            # 'dates': [datetime.date(2019, 5, 1), datetime.date(2019, 5, 2), datetime.date(2019, 5, 3), datetime.date(2019, 5, 4)]
        }
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        if form.is_valid():
            start_date = form.cleaned_data['start_period']
            end_date = form.cleaned_data['end_date']

            dates= [start_date + datetime.timedelta(n) for n in range(int((end_date - start_date).days)+1)]

            context = {
                'form': self.form,
                'dates': dates
            }
            return render(self.request, self.template_name, context)
        context = {
            'form': self.form(request.POST or None)
        }
        return render(self.request, self.template_name, context)

