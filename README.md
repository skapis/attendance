# Attendance System
This folder contains an attendance system that can be used by small companies to track employee attendance. 
The application is built using the Django framework with Bootstrap 4 for the frontend. To use the application, each employee and manager must have a created account. Due to user restrictions, only users with admin roles and managers can create accounts.

## Attendance
After logging in, users with employee roles are redirected to the attendance overview for the current month. If a user logs in for the first time, their attendance records are automatically generated for the entire month. Users can then edit records according to their worked hours. Users can also export all records to an Excel file.
The exported file will contain 2 sheets - the first sheet contains a summary where attendance is totaled by categories, and the second sheet contains detailed attendance records.
![Attendance Overview](https://github.com/skapis/appscreenshots/blob/main/Attendance/Doch%C3%A1zka.png)

### Submitting/Confirming Attendance
If a user has completed attendance for the entire month and met the required hours, the "Submit" option becomes available. After submitting attendance, the total monthly attendance is calculated and the user can no longer edit the records. If the attendance contains errors, it can be modified, but after submission, only users with manager roles can edit the attendance.

## Projects
The Projects section is used to record hours worked on individual projects. In the projects overview, users can create new entries by filling in the project name, date, and time period worked. Based on these records, the summary table is populated with total hours by project. Like attendance, users can export both summary and detailed overview to an Excel file.
If a user has recorded all worked hours on projects for the given month, they can submit the projects, which, similar to attendance, prevents further editing of records.
![Projects Overview](https://github.com/skapis/appscreenshots/blob/main/Attendance/Projekty.png)

## Employee Overview
The employee overview allows users with manager roles to check attendance and projects of employees. In the overview, managers can see all employees registered in the system. They can also create accounts for new users/employees. Users with manager roles will see the "Employees" item in the top menu, while employees (regular users) don't have this option.
![Employee Overview](https://github.com/skapis/appscreenshots/blob/main/Attendance/P%C5%99ehled%20zam%C4%9Bstnanc%C5%AF.png)

### Creating a New User
To create a new user, all fields in the form must be completed. The form checks for duplicate usernames and has password requirements. Managers also fill in the employment ratio and other information. The employment ratio is entered as a number, where 1 = full-time, 0.5 = part-time. This coefficient determines the number of hours an employee must work/fill in their attendance.
![New User](https://github.com/skapis/appscreenshots/blob/main/Attendance/Nov%C3%BD%20u%C5%BEivatel.png)

### Employee Detail
In the employee detail, managers can deactivate an employee's system access by clicking the "Deactivate User" button. This option exists for cases when an employee leaves the company and needs to have their system access revoked. Managers can also browse through employee attendance and projects, and edit their attendance/projects. If attendance/projects haven't been submitted yet, only detailed records are shown. After confirmation, summaries and the option to view details are displayed.
Managers can also export attendance/projects to an Excel file. The file has the same format as for regular users.
![Employee Detail](https://github.com/skapis/appscreenshots/blob/main/Attendance/Zam%C4%9Bstanec.png)

## Calendar Creation
For proper application functionality, the system admin must create a calendar in the database that contains individual days with marked weekends and holidays. Below is a script that creates records for all days in the year and marks weekends. Holidays must be marked manually in the admin interface, which the admin has access to.
```
from core.models import Calendar
from datetime import datetime as dt
import calendar

cur_year = dt.today().year
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

for month in months:
    num_days = calendar.monthrange(year=cur_year, month=month)[1]
    days = [dt(year=cur_year, month=month, day=day).date() for day in range(1, num_days+1)]
    
    for d in days:
        if d.weekday() in (5, 6):
            Calendar.objects.create(date=d, month=d.month, year=d.year, weekend=True, holiday=False)
        else:
            Calendar.objects.create(date=d, month=d.month, year=d.year, weekend=False, holiday=False)
```
