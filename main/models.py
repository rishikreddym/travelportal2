from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.

#Bus Model with BusID (Primary Key), Registration No. and Capacity
class Bus(models.Model):
	bus_id = models.CharField(verbose_name="Bus ID",max_length=10,primary_key=True)
	reg_no = models.CharField(verbose_name="Registration No.",max_length=50,null = False, blank = False)
	capacity = models.IntegerField(verbose_name="Capacity",null=True,blank=True,validators=[MinValueValidator(1)])

	def __unicode__(self):
		return self.bus_id

#Schedule Model to stores the schedules of buses
class Schedule(models.Model):
	DAYS = (
			(0,'Monday'),
			(1,'Tuesday'),
			(2,'Wednesday'),
			(3,'Thursday'),
			(4,'Friday'),
			(5,'Saturday'),
			(6,'Sunday'),
	)
	PLACES = (('M','Mandi'),('K','Kamand'),)

	time = models.TimeField(verbose_name="Time",null=False)
	day = models.IntegerField(verbose_name="Weekday",choices=DAYS)
	bus_id = models.ForeignKey(Bus,verbose_name="Bus ID")
	source = models.CharField(verbose_name="Source",max_length=10,choices=PLACES)
	dest = models.CharField(verbose_name="Destination",max_length=10,choices=PLACES)

	def weekday(self):
		return self.DAYS[self.day][1]

	def __unicode__(self):
		return str(self.day)+' '  + str(self.time) +' ' + str(self.bus_id)+' ' + str(self.source)

#Car Model to store details of cars
class Car(models.Model):	
	vehicle_id = models.CharField(verbose_name="Vehicle ID",max_length=20,primary_key=True)
	reg_no = models.CharField(verbose_name="Registration No.",max_length=50,null = False, blank = False)
	capacity = models.IntegerField(verbose_name="Capacity",validators=[MinValueValidator(1)])
	avail_from = models.DateTimeField(verbose_name="Available After")
	avail_till = models.DateTimeField(verbose_name="Available Before")
	PLACES = (('M','Mandi'),('K','Kamand'),)
	parked_at = models.CharField(verbose_name="Parked At",max_length=10,choices=PLACES)
	def __unicode__(self):
		return str(self.vehicle_id)

#Booking Model to store the Bookings
class Booking(models.Model):
	date_time  = models.DateTimeField(verbose_name="Date-Time",)
	PLACES = (('M','Mandi'),('K','Kamand'),)
	source = models.CharField(verbose_name="Source",max_length=10,choices=PLACES)
	dest = models.CharField(verbose_name="Destination",max_length=10,choices=PLACES)
	vehicle_id = models.ForeignKey(Car,verbose_name="Vehicle ID")
	seats_left =  models.IntegerField(verbose_name="Seats Left",validators=[MinValueValidator(0)])
	resv = models.ManyToManyField(User,verbose_name="Reserved By")

	def resv_by(self):
		return ', '.join([a.username for a in self.resv.all()])
	resv_by.short_description = "Reserved By"
	
	def __unicode__(self):
		return str(self.vehicle_id)+' ' + str(self.date_time)+' ' + str(self.source)
	

