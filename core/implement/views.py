from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

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

            if not self.request.user.username == '':
                general_df, grow_df, drop_df = mainscript(start_date, log=self.request.user.email, pas=self.request.user.pass_for_api)
            else:
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




class CurrDateTableView(View):
    def get(self, request, *args, **kwargs):
        curr_date = self.request.GET.get('curr_date')
        curr_date = '-'.join([curr_date.split('-')[2], curr_date.split('-')[1], curr_date.split('-')[0]])
        curr_date = datetime.datetime.strptime(curr_date, '%Y-%m-%d').date()

        if not self.request.user.username == '':
            general_df, grow_df, drop_df = mainscript(curr_date, log=self.request.user.email,pas=self.request.user.pass_for_api)
        else:
            general_df, grow_df, drop_df = mainscript(curr_date)

        data = [{
            'general_df':general_df,
            'grow_df':grow_df,
            'drop_df':drop_df
        }]
        return JsonResponse(data, safe = False)