import datetime, csv, io
from django.contrib.auth.models import User
from courses.models import Trainer
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'schedule/index.html', {'fuser' : request.user})

class TrainerEvent:
    def __init__(self, name, user_name, start_date, end_date, start_time=None, end_time=None):
        self.name = name
        self.user_name = user_name
        self.is_all_day = start_time == None
        self.start_date = start_date
        self.end_date = end_date

        if self.is_all_day:
            self.start_time = datetime.time(0,0,0)
            self.end_time = datetime.time(0,0,0)
        else:
            self.start_time = start_time
            self.end_time = end_time

    def generate_reminder(self):
        if self.is_all_day:
            return [self.start_date - datetime.timedelta(days=1), datetime.time(0, 0, 0)]
        else:
            temp_date = datetime.datetime.combine(self.start_date, self.start_time)
            temp_date = temp_date - datetime.timedelta(minutes=30)
            return [datetime.date(temp_date.year, temp_date.month, temp_date.day),
                    datetime.time(temp_date.hour, temp_date.minute, temp_date.second)]

def download(request):
    events = [
        #TrainerEvent('Test Event C', 'Muizz Siddique', datetime.date(2020, 4, 23), datetime.date(2020, 5, 1)),
        #TrainerEvent('Test Event D', 'Muizz Siddique', datetime.date(2020, 4, 25), datetime.date(2020, 4, 26), datetime.time(9), datetime.time(10, 30))
    ]

    for trainer in Trainer.objects.all():
        if request.user == trainer.user:
            events.append(
                TrainerEvent(trainer.schedule.course.course_info, request.user.username, trainer.schedule.start, trainer.schedule.end)# datetime.date(2020, 4, 25), datetime.date(2020, 4, 26))
            )

    output = io.StringIO()
    header = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'All day event',
              'Reminder on/off', 'Reminder Date', 'Reminder Time', 'Meeting Organizer', 'Required Attendees',
              'Optional Attendees', 'Meeting Resources', 'Billing Information', 'Categories', 'Description',
              'Location', 'Mileage', 'Priority', 'Private', 'Sensitivity', 'Show time as']

    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerow(header)
    for event in events:
        reminder_date, reminder_time = event.generate_reminder()
        writer.writerow([event.name, event.start_date.strftime('%Y/%m/%d'), event.start_time, event.end_date.strftime('%Y/%m/%d'), event.end_time, event.is_all_day,
                         True, reminder_date.strftime('%Y/%m/%d'), reminder_time, None, None,
                         None, None, None, None, None,
                         None, None, 'Normal', False, 'Normal', 2 if not event.is_all_day else 3])

    print(output.getvalue())

    response = HttpResponse(output.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=schedule.csv'
    return response
