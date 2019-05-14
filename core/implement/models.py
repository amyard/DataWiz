# from django.db import models
# from django.conf import settings
# from datetime import date, timedelta
#
#
#
#
#
# class SearchDateModel(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'user', blank = True)
#     start_period = models.DateField(blank = True, default = date.today() - timedelta(days = 7))
#     end_date = models.DateField(blank = True, default = date.today)
#
#     def __str__(self):
#         return f'{self.start_period}-{self.end_date}'
#
#     class Meta:
#         ordering = ['-id']