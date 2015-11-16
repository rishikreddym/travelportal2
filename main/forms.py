from django import forms
from django.utils import timezone

import django_tables2 as tables
from datetimewidget.widgets import DateTimeWidget,DateWidget
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import SelectDateWidget
from .models import Bus,Schedule,Car,Booking

class BusForm(forms.ModelForm):
	class Meta:
		model = Bus
		exclude = []

class ScheduleForm(forms.ModelForm):
	class Meta:
		model = Schedule
		fields = ['day','time','bus_id','source','dest']

class CarForm(forms.ModelForm):
	class Meta:
		model = Car
		exclude = []

class PreBookingForm(forms.ModelForm):
	SEATS  = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'))
	seats = forms.ChoiceField(widget=forms.Select,choices=SEATS)
	SOURCES = (('u','-----------'),('M','Mandi'),('K','Kamand'),)
	DESTS  = (('u','------------'),('K','Kamand'),('M','Mandi'),)
	source = forms.ChoiceField(widget=forms.Select, choices=SOURCES)
	dest = forms.ChoiceField(widget=forms.Select, choices=DESTS)
	class Meta:
		model = Booking
		fields = ('date_time',)
		widgets = {
			'date_time': DateTimeWidget(attrs={'id':"date_time"}, usel10n = True, bootstrap_version=3)
		}

class ScheduleQueryForm(forms.Form):
	DAYS = (
			(0,'Monday'),
			(1,'Tuesday'),
			(2,'Wednesday'),
			(3,'Thursday'),
			(4,'Friday'),
			(5,'Saturday'),
			(6,'Sunday'),
	)
	day = forms.ChoiceField(widget=forms.Select, choices=DAYS,initial=timezone.now().weekday())
	SOURCES = (('u','-----------'),('M','Mandi'),('K','Kamand'),)
	DESTS  = (('u','------------'),('K','Kamand'),('M','Mandi'),)
	source = forms.ChoiceField(widget=forms.Select, choices=SOURCES)
	dest = forms.ChoiceField(widget=forms.Select, choices=DESTS)
	

class BookingQueryForm(forms.Form):
    date = forms.DateField(widget = DateWidget(attrs={'id':"date",},usel10n=True,bootstrap_version=3),initial=timezone.now().date())
    SOURCES = (('u','-----------'),('M','Mandi'),('K','Kamand'),)
    DESTS  = (('u','------------'),('K','Kamand'),('M','Mandi'),)
    source = forms.ChoiceField(widget=forms.Select, choices=SOURCES)
    dest = forms.ChoiceField(widget=forms.Select, choices=DESTS)