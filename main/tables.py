from django import forms
import django_tables2 as tables
from django.contrib.admin.widgets import AdminDateWidget 
from .models import Bus,Schedule,Car,Booking

class ScheduleQueryTable(tables.Table):
    class Meta:
        model = Schedule
        #fields = ['time','bus_id','source','dest']
        attrs = {"class": "table our table-fixed"}

class BookingQueryTable(tables.Table):
	
	class Meta:
		model = Booking
		fields = ('id','date_time','vehicle_id','seats_left','resv_by','source','dest')
		attrs = {"class": "table our"}
	


class BookingShareTable(tables.Table):
	selection = tables.TemplateColumn('<input type="radio" name="select" value="s|{{ record.pk }}" />', verbose_name="Select")
	class Meta:
		model = Booking
		fields = ('selection','id','date_time','vehicle_id','seats_left','resv_by','source','dest')
		attrs = {"class": "table our"}

class BookingNewTable(tables.Table):
	selection = tables.TemplateColumn('<input type="radio" name="select" value="n|{{ record.pk }}" />', verbose_name="Select")
	class Meta:
		model = Car
		fields = ('selection','vehicle_id','reg_no','capacity','avail_till','avail_from','parked_at')
		attrs = {"class": "table our"}




