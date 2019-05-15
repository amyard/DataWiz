from django.shortcuts import render
from django.views.generic import View

from core.implement.forms import SearchDateForm
from core.utils.mainscript import mainscript
import datetime



class MainPageView(View):
    template_name = 'implement/main.html'
    form = SearchDateForm

    def get(self, request, *args, **kwargs):
        context = {
            'form':self.form,
        }
        return render(self.request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        if form.is_valid():
            start_date = form.cleaned_data['start_period']
            end_date = form.cleaned_data['end_date']

            dates= [start_date + datetime.timedelta(n) for n in range(int((end_date - start_date).days)+1)]
            general_df, grow_df, drop_df = mainscript(start_date)

            context = {
                'form': self.form(request.POST or None),
                'dates': dates,
                'general_df':general_df, 'grow_df':grow_df, 'drop_df':drop_df
            }
            return render(self.request, self.template_name, context)
        context = {
            'form': self.form(request.POST or None)
        }
        return render(self.request, self.template_name, context)

