from datetime import datetime as dt
from django.shortcuts import render, redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from userprofile.models import UserProfile
from projects.models import Project, ProjectsAggMonth
from core.models import Attendance, AttendanceAggMonth, Calendar, AttendanceCategory
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json
import decimal
import xlwt


def access_denied(request):
    return render(request, 'staff/not_staff.html')


@login_required(login_url='/auth/login')
@staff_member_required(login_url='/staff/access-denied')
def index(request):
    if request.method == 'GET':
        emps = UserProfile.objects.all()


        context = {
            'employees': emps
        }
        return render(request, 'staff/index.html', context)


# TODO: create summary, who confirmed projects and attendance this month and who not. Choose emps, who do not have
#  any record in table aggmonth for this month

@login_required(login_url='/auth/login')
@staff_member_required(login_url='/staff/access-denied')
def emp_detail(request, id):
    if request.method == 'GET':
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)

        categories = AttendanceCategory.objects.all()
        profile = UserProfile.objects.get(profileId=id)

        if year and month:
            att_m = AttendanceAggMonth.objects.filter(owner=profile.owner,
                                                      month=dt(year=int(year), month=int(month), day=1))
            att = Attendance.objects.filter(profile=profile, year=int(year), month=int(month))
            pr_m = ProjectsAggMonth.objects.filter(owner=profile.owner,
                                                   month=dt(year=int(year), month=int(month), day=1))
            pr = Project.objects.filter(owner=profile.owner, year=int(year), month=int(month))
        else:
            year = dt.today().year
            month = dt.today().month
            att_m = AttendanceAggMonth.objects.filter(owner=profile.owner, month=dt(year=year, month=month, day=1))
            att = Attendance.objects.filter(profile=profile, year=year, month=month)
            pr_m = ProjectsAggMonth.objects.filter(owner=profile.owner, month=dt(year=year, month=month, day=1))
            pr = Project.objects.filter(owner=profile.owner, year=year, month=month)

        project_hours = pr.aggregate(sum=Sum('duration'))
        project_hours_month = pr_m.aggregate(sum=Sum('duration'))
        att_hours = att.aggregate(sum=Sum('duration'))
        
        if att_hours['sum']:
            att_total = decimal.Decimal(round(att_hours['sum'] / 3600, 2))
        else:
            att_total = 0

        if project_hours['sum']:
            pr_total = round(project_hours['sum'] / 3600, 2)
        else:
            pr_total = 0

        if project_hours_month['sum']:
            m_total = round(project_hours_month['sum'] / 3600, 2)
        else:
            m_total = 0

        cal = Calendar.objects.filter(month=month, year=year, weekend=False).count()
        extra_hours = att_total - (cal * decimal.Decimal(8.5) * profile.fteValue)

        context = {
            'profile': profile,
            'attendance': att,
            'projects': pr,
            'prTotal': pr_total,
            'projectMonth': pr_m,
            'attendanceMonth': att_m,
            'monthTotal': m_total,
            'attTotal': att_total,
            'extraHours': extra_hours,
            'categories': categories
        }
        return render(request, 'staff/empDetail.html', context)


@login_required(login_url='/auth/login')
@staff_member_required(login_url='/staff/access-denied')
def create_new_user(request):
    if request.method == 'POST':
        data = request.POST
        username = data['userName']
        password = data['pass1']
        confirm_password = data['pass2']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']
        emp_num = data['empNum']
        fte = data['fte']
        position = data['position']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Uživatel již existuje')
            return redirect('staff')

        if password != confirm_password:
            messages.error(request, 'Zadaná hesla se neshodují')
            return redirect('staff')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,
                                        password=password)
        UserProfile.objects.create(owner=user, workerId=emp_num, fteValue=fte, position=position)

        messages.success(request, 'Uživatel byl vytvořen')
        return redirect('staff')


@login_required(login_url='/auth/login')
@staff_member_required(login_url='/staff/access-denied')
def toggle_user_active(request, id):
    if request.method == 'POST':
        profile = UserProfile.objects.get(profileId=id)
        user = User.objects.get(pk=profile.owner.pk)

        if user.is_active:
            user.is_active = False
            messages.success(request, 'Uživatel byl deaktivován, nyní se nemůže přihlásit')
        else:
            user.is_active = True
            messages.success(request, 'Uživatel byl aktivován')
        user.save()
        return redirect('employee', id)


@login_required(login_url='/auth/login')
def check_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': False}, status=400)

        return JsonResponse({'message': True}, status=200)


@login_required(login_url='/auth/login')
@staff_member_required(login_url='/staff/access-denied')
def edit_emp_attendance(request, id):
    if request.method == 'POST':
        att = Attendance.objects.get(attendanceId=id)
        data = request.POST
        date = data['date']
        start = data['start']
        end = data['end']

        if not date or not start or not end:
            messages.error(request, 'Chybí povinné informace')
            return redirect('attendance')

        if len(start) == 5:
            start = f'{start}:00'

        if len(end) == 5:
            end = f'{end}:00'

        att.date = date
        att.start = start
        att.end = end
        att.save()

        att_month = AttendanceAggMonth.objects.get(month=dt(year=att.year, month=att.month, day=1),
                                                   owner=att.owner, category=att.category.name)

        att_all = Attendance.objects.filter(month=att.month, year=att.year, owner=att.owner, category=att.category)
        new_dur = att_all.aggregate(sum=Sum('duration'))

        att_month.duration = new_dur['sum']
        att_month.save()

        d = dt.strptime(date, '%Y-%m-%d')
        messages.success(request, 'Záznam byl úspěšně změněn')
        return redirect(reverse('employee', args=[att.profile.profileId]) + f'?year={d.year}&month={d.month}')


@login_required(login_url='/auth/login')
@staff_member_required(login_url='/staff/access-denied')
def edit_emp_projects(request, id):
    if request.method == 'POST':
        project = Project.objects.get(projectId=id)
        profile = UserProfile.objects.get(owner=project.owner)
        data = request.POST
        name = data['name']
        date = data['date']
        start = data['start']
        end = data['end']

        if not date or not start or not end or not name:
            messages.error(request, 'Chybí povinné informace')
            return redirect('projects')

        if len(start) == 5:
            start = f'{start}:00'

        if len(end) == 5:
            end = f'{end}:00'

        d = dt.strptime(date, '%Y-%m-%d')

        project.name = name
        project.date = date
        project.start = start
        project.end = end
        project.save()

        project_month = ProjectsAggMonth.objects.get(owner=profile.owner, name=project.name,
                                                     month=dt(year=project.year, month=project.month, day=1))

        pr = Project.objects.filter(owner=profile.owner, name=project.name, year=project.year, month=project.month)

        new_dur = pr.aggregate(sum=Sum('duration'))

        project_month.duration = new_dur['sum']
        project_month.save()

        messages.success(request, 'Záznam byl úspěšně změněn')
        return redirect(reverse('employee', args=[profile.profileId]) + f'?year={d.year}&month={d.month}')


@login_required(login_url='/auth/login')
@staff_member_required(login_url='/staff/access-denied')
def export_emp_projects(request, id):
    profile = UserProfile.objects.get(profileId=id)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Projekty_' + str(dt.now().date()) + '.xls'
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    if year and month:
        prs = Project.objects.filter(owner=profile.owner, month=int(month), year=int(year))
    else:
        prs = Project.objects.filter(owner=request.user, month=dt.today().month, year=dt.today().year)
    wb = xlwt.Workbook(encoding='utf-8')
    font_style = xlwt.XFStyle()

    ws_sum = wb.add_sheet('Souhrn')
    header = ['Projekt', 'Měsíc']
    font_style.font.bold = True
    for col in range(len(header)):
        ws_sum.write(0, col, header[col], font_style)

    project_hours = prs.values('name').annotate(sum=Sum('duration') / 3600)
    font_style = xlwt.XFStyle()
    row_n = 0

    for pr in project_hours:
        row_n += 1

        for col_num, col in enumerate([pr['name'], pr['sum']]):
            ws_sum.write(row_n, col_num, col)

    ws = wb.add_sheet('Detail')
    row_num = 0
    columns = ['Projekt', 'Datum', 'Začátek', 'Konec', 'Počet hodin']
    font_style.font.bold = True

    for col in range(len(columns)):
        ws.write(row_num, col, columns[col], font_style)

    font_style = xlwt.XFStyle()
    rows = prs.values_list('name', 'date', 'start', 'end', 'duration')
    for row in rows:
        row_num += 1
        project = row[0]
        date = str(row[1])
        start = str(row[2])
        end = str(row[3])
        duration = round(row[4] / 3600, 2)

        for col_num, col in enumerate([project, date, start, end, duration]):
            ws.write(row_num, col_num, col, font_style)

    wb.save(response)
    return response


@login_required(login_url='/auth/login')
@staff_member_required(login_url='/staff/access-denied')
def export_emp_attendance(request, id):
    profile = UserProfile.objects.get(profileId=id)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Docházka_' + str(dt.now().date()) + '.xls'
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    if year and month:
        date = dt(year=int(year), month=int(month), day=1)
        att_m = AttendanceAggMonth.objects.filter(owner=profile.owner, month=date)
        att = Attendance.objects.filter(owner=profile.owner, month=int(month), year=int(year))
    else:
        t = dt.today()
        att_m = AttendanceAggMonth.objects.filter(owner=profile.owner, month=dt(year=t.year, month=t.month, day=1))
        att = Attendance.objects.filter(owner=request.user, month=dt.today().month, year=dt.today().year)
    wb = xlwt.Workbook(encoding='utf-8')
    font_style = xlwt.XFStyle()

    ws_sum = wb.add_sheet('Souhrn')
    header = ['Měsíc', 'Kategorie', 'Počet hodin']
    font_style.font.bold = True
    for col in range(len(header)):
        ws_sum.write(0, col, header[col], font_style)

    font_style = xlwt.XFStyle()
    row_n = 0

    for a in att_m:
        row_n += 1
        data = [str(a.month), a.category, round(a.duration/3600, 2)]
        for col_num, col in enumerate(data):
            ws_sum.write(row_n, col_num, col)

    ws = wb.add_sheet('Detail')
    row_num = 0
    columns = ['Datum', 'Kategorie', 'Začátek', 'Konec', 'Počet hodin', 'Saldo']
    font_style.font.bold = True
    for col in range(len(columns)):
        ws.write(row_num, col, columns[col], font_style)
    font_style = xlwt.XFStyle()

    for at in att:
        row_num += 1
        category = at.category.name
        d = str(at.date)
        start = str(at.start)
        end = str(at.end)
        duration = round(at.duration / 3600, 2)
        saldo = at.saldo()

        data = [d, category, start, end, duration, saldo]
        for col_num, col in enumerate(data):
            ws.write(row_num, col_num, col, font_style)

    wb.save(response)
    return response
