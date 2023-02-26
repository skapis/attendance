from django.shortcuts import render, redirect, reverse
from .models import Project, ProjectsAggMonth
from datetime import datetime as dt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth.models import User
import xlwt


@login_required(login_url='/auth/login')
def projects(request):
    if request.method == 'GET':
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        if year and month:
            pr = Project.objects.filter(owner=request.user, month=int(month), year=int(year))
        else:
            year = dt.today().year
            month = dt.today().month
            pr = Project.objects.filter(owner=request.user, month=month, year=year)
        total_hours = 0
        if pr.count != 0:
            for p in pr:
                total_hours += p.work_hours()
        project_hours = pr.values('name').annotate(sum=Sum('duration')/3600)

        if ProjectsAggMonth.objects.filter(owner=request.user, month=dt(year=int(year), month=int(month), day=1))\
                .exists():
            confirmed = True
            messages.warning(request, 'Tento měsíc byl již potvrzen a záznamy již nelze editovat')
        else:
            confirmed = False

        context = {
            'projects': pr,
            'total': total_hours,
            'projectHours': project_hours,
            'confirmed': confirmed
        }
        return render(request, 'projects/index.html', context)

    if request.method == 'POST':
        data = request.POST
        name = data['name']
        date = data['date']
        start = data['start']
        end = data['end']

        if len(start) == 5:
            start = f'{start}:00'

        if len(end) == 5:
            end = f'{end}:00'

        if not date or not start or not end or not name:
            messages.error(request, 'Chybí povinné informace')
            return redirect('projects')

        d = dt.strptime(date, '%Y-%m-%d')

        if ProjectsAggMonth.objects.filter(owner=request.user, month=dt(year=d.year, month=d.month, day=1)).exists():
            messages.error(request, 'Projekty pro tento měsíc již byly potvrzeny a nelze přidat další záznam')
            return redirect('projects')

        Project.objects.create(name=name, date=date, start=start, end=end, owner=request.user)

        messages.success(request, 'Záznam byl vytvořen')

        return redirect(reverse('projects') + f'?year={d.year}&month={d.month}')


@login_required(login_url='/auth/login')
def edit_project(request, id):
    if request.method == 'POST':
        project = Project.objects.get(projectId=id)
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

        if project.confirmed:
            messages.error(request, 'Tento záznam již nelze editovat')
            return redirect(reverse('projects') + f'?year={d.year}&month={d.month}')

        project.name = name
        project.date = date
        project.start = start
        project.end = end
        project.save()

        messages.success(request, 'Záznam byl úspěšně změněn')
        return redirect(reverse('projects') + f'?year={d.year}&month={d.month}')


@login_required(login_url='/auth/login')
def confirm_projects(request):
    if request.method == 'GET':
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)

        if year and month:
            pr = Project.objects.filter(owner=request.user, month=int(month), year=int(year))
        else:
            month = dt.today().month
            year = dt.today().year
            pr = Project.objects.filter(owner=request.user, month=month, year=year)

        project_hours = pr.values('name').annotate(sum=Sum('duration'))
        user = User.objects.get(pk=request.user.pk)

        if ProjectsAggMonth.objects.filter(owner=request.user, month=dt(year=int(year), month=int(month), day=1))\
                .exists():
            messages.error(request, 'Projekty již byly jednou potvrzeny')
            return redirect(reverse('projects') + f'?year={year}&month={month}')

        for p in pr:
            p.confirmed = True
            p.confirmed_at = dt.now()
            p.save()

        for project in project_hours:
            date = dt(year=int(year), month=int(month), day=1).date()
            ProjectsAggMonth.objects.create(owner=user, name=project['name'], first_name=user.first_name,
                                            last_name=user.last_name, month=date, duration=project['sum'])

        messages.success(request, 'Projekty byly potvrzeny')
        return redirect(reverse('projects') + f'?year={year}&month={month}')


@login_required(login_url='/auth/login')
def export_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Projekty_' + str(dt.now().date()) + '.xls'
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    if year and month:
        prs = Project.objects.filter(owner=request.user, month=int(month), year=int(year))
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
        duration = round(row[4]/3600, 2)

        for col_num, col in enumerate([project, date, start, end, duration]):
            ws.write(row_num, col_num, col, font_style)

    wb.save(response)
    return response
