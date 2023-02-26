# insert records to calendar
# from core.models import Calendar
# from datetime import datetime as dt
# import calendar
#
# cur_year = dt.today().year
# months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
#
# for month in months:
#     num_days = calendar.monthrange(year=cur_year, month=month)[1]
#     days = [dt(year=cur_year, month=month, day=day).date() for day in range(1, num_days+1)]
#
#     for d in days:
#         if d.weekday() in (5, 6):
#             Calendar.objects.create(date=d, month=d.month, year=d.year, weekend=True, holiday=False)
#         else:
#             Calendar.objects.create(date=d, month=d.month, year=d.year, weekend=False, holiday=False)


