import decimal
from django.shortcuts import render, redirect, reverse
from datetime import datetime as dt, timedelta
from django.contrib import messages
from .models import Attendance, AttendanceCategory, Calendar, AttendanceAggMonth
from django.contrib.auth.decorators import login_required
from userprofile.models import UserProfile
from django.db.models import Sum


@login_required(login_url='/auth/login')
def attendance(request):
    if request.method == 'GET':
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)

        profile = UserProfile.objects.get(owner=request.user)
        att_categories = AttendanceCategory.objects.exclude(name='Státní svátek')

        if year and month:
            att = Attendance.objects.filter(owner=request.user, month=month, year=year)
            cal = Calendar.objects.filter(month=month, year=year, weekend=False)
            if not att.exists():
                for day in cal:
                    if day.holiday:
                        cat = AttendanceCategory.objects.get(name='Státní svátek')
                        Attendance.objects.create(owner=request.user, profile=profile, category=cat, date=day.date,
                                                  start='08:00:00', end='16:30:00')
                    else:
                        cat = AttendanceCategory.objects.get(name='Výkon práce')
                        Attendance.objects.create(owner=request.user, profile=profile, category=cat, date=day.date,
                                                  start='00:00:00', end='00:00:00')
        else:
            month = dt.today().month
            year = dt.today().year
            att = Attendance.objects.filter(owner=request.user, month=month, year=year)
            cal = Calendar.objects.filter(month=month, year=year, weekend=False)
            if not att.exists():
                for day in cal:
                    if day.holiday:
                        cat = AttendanceCategory.objects.get(name='Státní svátek')
                        Attendance.objects.create(owner=request.user, profile=profile, category=cat, date=day.date,
                                                  start='08:00:00', end='16:30:00')
                    else:
                        cat = AttendanceCategory.objects.get(name='Výkon práce')
                        Attendance.objects.create(owner=request.user, profile=profile, category=cat, date=day.date,
                                                  start='00:00:00', end='00:00:00')
        if AttendanceAggMonth.objects.filter(owner=request.user, month=dt(year=int(year), month=int(month), day=1)).\
                exists():
            messages.warning(request, 'Docházka již byla odeslána a záznamy nelze editovat')
            confirmed = True
        else:
            confirmed = False

        att_hours = att.aggregate(sum=Sum('duration'))
        cal_hours = cal.count() * decimal.Decimal(8.5) * profile.fteValue

        context = {
            'attendance': att,
            'categories': att_categories,
            'total': round(att_hours['sum'] / 3600, 2),
            'required': round(decimal.Decimal(att_hours['sum'] / 3600), 2) - cal_hours,
            'confirmed': confirmed
        }
        return render(request, 'attendance/index.html', context)


@login_required(login_url='/auth/login')
def edit_attendance(request, id):
    if request.method == 'POST':
        att = Attendance.objects.get(attendanceId=id)
        data = request.POST
        date = data['date']
        start = data['start']
        end = data['end']
        category = data['category']

        if not date or not start or not end or not category:
            messages.error(request, 'Chybí povinné informace')
            return redirect('attendance')

        if len(start) == 5:
            start = f'{start}:00'

        if len(end) == 5:
            end = f'{end}:00'

        att_category = AttendanceCategory.objects.get(pk=category)
        att.date = date
        att.start = start
        att.end = end
        att.category = att_category
        att.save()

        d = dt.strptime(date, '%Y-%m-%d')
        messages.success(request, 'Záznam byl úspěšně změněn')
        return redirect(reverse('attendance') + f'?year={d.year}&month={d.month}')


@login_required(login_url='/auth/login')
def delete_attendance(request, id):
    att = Attendance.objects.get(attendanceId=id)
    att.delete()

    messages.success(request, 'Záznam byl smazán')
    return redirect('attendance')


@login_required(login_url='/auth/login')
def confirm_attendance(request):
    if request.method == 'GET':
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)

        if year and month:
            att = Attendance.objects.filter(owner=request.user, month=int(month), year=int(year))
        else:
            month = dt.today().month
            year = dt.today().year
            att = Attendance.objects.filter(owner=request.user, month=month, year=year)

        if AttendanceAggMonth.objects.filter(month=dt(year=int(year), month=int(month), day=1), owner=request.user) \
                .exists():
            messages.error(request, 'Docházka pro tento měsíc byla již potvrzena')
            return redirect(reverse('attendance') + f'?year={year}&month={month}')

        att_hours = att.values('category').annotate(sum=Sum('duration'))

        for category in att_hours:
            date = dt(year=int(year), month=int(month), day=1).date()
            att_category = AttendanceCategory.objects.get(pk=category['category'])
            AttendanceAggMonth.objects.create(month=date, owner=request.user, category=att_category.name,
                                              first_name=request.user.first_name, last_name=request.user.last_name,
                                              duration=category['sum'])

        for a in att:
            a.confirmed = True
            a.confirmed_at = dt.now()
            a.save()

        messages.success(request, 'Docházka byla potvrzena')
        return redirect(reverse('attendance') + f'?year={year}&month={month}')
