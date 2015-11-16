from django.shortcuts import render,RequestContext
from django.utils import timezone
from django.contrib.auth.models import User
from django_tables2   import RequestConfig

# Create your views here.
from .forms import BusForm,ScheduleForm,CarForm,ScheduleQueryForm,BookingQueryForm,PreBookingForm
from .tables import ScheduleQueryTable,BookingQueryTable,BookingShareTable,BookingNewTable
from .models import Bus,Schedule,Car,Booking
import datetime
import dateutil.parser
from datetime import timedelta

def  home(request):
	context = {'message':"",'nextBusMK':"No buses from Mandi to Kamand now",'nextBusKM':"No buses from Kamand to Mandi now"}
	print timezone.localtime(timezone.now()).time()
	temp = Schedule.objects.filter(day=timezone.localtime(timezone.localtime(timezone.now())).weekday(),source='M',dest='K',time__gte=timezone.localtime(timezone.now()).time())
	if temp.count() > 0:
		context['nextBusMK'] = "Next Bus from Mandi to Kamand is " + str(temp[0].bus_id) + " departing at " + str(temp[0].time)
	temp = Schedule.objects.filter(day=timezone.localtime(timezone.now()).weekday(),source='K',dest='M',time__gte=timezone.localtime(timezone.now()).time())
	if temp.count() > 0:
		context['nextBusKM'] = "Next Bus from Kamand to Mandi is " + str(temp[0].bus_id)  + " departing at " + str(temp[0].time)
	 

	if request.method=='POST':
		if 'scheduleQuery' in request.POST:
			scheduleQueryForm = ScheduleQueryForm(request.POST,prefix='schedule')
			if scheduleQueryForm.is_valid():
				print scheduleQueryForm.cleaned_data
				dayChoice = int(scheduleQueryForm.cleaned_data.get('day'))
				sourceChoice = scheduleQueryForm.cleaned_data.get('source')
				destChoice = scheduleQueryForm.cleaned_data.get('dest')
				schedule = ScheduleQueryTable(Schedule.objects.filter(day=dayChoice,source=sourceChoice,dest=destChoice))
				RequestConfig(request,paginate=False).configure(schedule)

			data = {'date':timezone.localtime(timezone.now()).date(),}
			bookingQueryForm = BookingQueryForm(initial=data,prefix='booking')
			dateChoice = timezone.localtime(timezone.now()).date()
			dateChoice = (dateChoice,dateChoice+timedelta(days=1))
			booking = BookingQueryTable( Booking.objects.filter(date_time__gte=timezone.localtime(timezone.now()),date_time__range=dateChoice))
			RequestConfig(request,paginate=False).configure(booking)

			context['schedule'] = schedule
			context['scheduleQueryForm'] = scheduleQueryForm
			context['booking'] = booking
			context['bookingQueryForm'] = bookingQueryForm

		elif 'bookingQuery' in request.POST:
			bookingQueryForm = BookingQueryForm(request.POST,prefix='booking')
			if bookingQueryForm.is_valid():
				print bookingQueryForm.cleaned_data
				dateChoice = bookingQueryForm.cleaned_data.get('date')
				dateChoice = (dateChoice,dateChoice+timedelta(days=1))
				sourceChoice = bookingQueryForm.cleaned_data.get('source')
				destChoice = bookingQueryForm.cleaned_data.get('dest')
				booking = BookingQueryTable( Booking.objects.filter(date_time__gte=timezone.localtime(timezone.now()),date_time__range=dateChoice,source=sourceChoice,dest=destChoice))
				RequestConfig(request,paginate=False).configure(booking)

			data = {'day':timezone.localtime(timezone.now()).weekday(),}
			scheduleQueryForm=ScheduleQueryForm(initial=data,prefix='schedule')
			schedule = ScheduleQueryTable(Schedule.objects.filter(day=timezone.localtime(timezone.now()).weekday()))
			RequestConfig(request,paginate=False).configure(schedule)
			
			context['schedule'] = schedule
			context['scheduleQueryForm'] = scheduleQueryForm
			context['booking'] = booking
			context['bookingQueryForm'] = bookingQueryForm
	else:
		data = {'date':timezone.localtime(timezone.now()).date(),}
		bookingQueryForm = BookingQueryForm(initial=data,prefix='booking')
		dateChoice = timezone.localtime(timezone.now()).date()
		dateChoiceRange = (dateChoice,dateChoice+timedelta(days=1))
		booking = BookingQueryTable( Booking.objects.filter(date_time__gte=timezone.localtime(timezone.now())))
		RequestConfig(request,paginate=False).configure(booking)
		data = {'day':timezone.localtime(timezone.now()).weekday(),}			
		scheduleQueryForm=ScheduleQueryForm(initial=data,prefix='schedule')
		schedule = ScheduleQueryTable(Schedule.objects.filter(day=timezone.localtime(timezone.now()).weekday()))
		RequestConfig(request,paginate=False).configure(schedule)
		context['schedule'] = schedule
		context['scheduleQueryForm'] = scheduleQueryForm
		context['booking'] = booking
		context['bookingQueryForm'] = bookingQueryForm

	return render(request,"home.html",context)

def staffBook(request):
	context = {'message':"",'date_time':timezone.localtime(timezone.now()),'seats':1,'source':'u','dest':'u'}
	print request.user
	if request.method=='POST':
		if 'preBookBtn' in request.POST:
			preBookingForm = PreBookingForm(request.POST,prefix='preBook')
			if preBookingForm.is_valid():
				dateTimeChoice = preBookingForm.cleaned_data.get('date_time')
				dateChoice = dateTimeChoice.date()
				dateChoice = (dateChoice,dateChoice+timedelta(days=1))
				sourceChoice = preBookingForm.cleaned_data.get('source')
				destChoice = preBookingForm.cleaned_data.get('dest')
				seats = preBookingForm.cleaned_data.get('seats')
				booking = BookingShareTable( Booking.objects.filter(date_time__gte=timezone.localtime(timezone.now()),date_time__range=dateChoice,source=sourceChoice,dest=destChoice,seats_left__gte=seats).filter(date_time__gte=dateTimeChoice))
				new = BookingNewTable( Car.objects.filter(capacity__gte=seats).exclude(avail_from__gte=dateTimeChoice,avail_till__lte=dateTimeChoice))
				RequestConfig(request,paginate=False).configure(booking)
				RequestConfig(request,paginate=False).configure(new)
				context['date_time'] = str(dateTimeChoice)
				context['preBookingForm'] = preBookingForm
				context['booking'] = booking
				context['new'] = new				
			else:
				dateTimeChoice = timezone.localtime(timezone.now())
				dateChoice = timezone.localtime(timezone.now()).date()
				dateChoice = (dateChoice,dateChoice+timedelta(days=1))
				booking = BookingShareTable( Booking.objects.filter(date_time__gte=dateTimeChoice,date_time__range=dateChoice,seats_left__gte=1))
				new = BookingNewTable( Car.objects.filter(capacity__gte=1).exclude(avail_from__gte=dateTimeChoice,avail_till__lte=dateTimeChoice))
				RequestConfig(request,paginate=False).configure(booking)
				RequestConfig(request,paginate=False).configure(new)
				context['seats'] = 1
				context['date_time'] = str(dateTimeChoice)
				context['preBookingForm'] = preBookingForm
				context['booking'] = booking
				context['new'] = new

		elif 'bookBtn' in request.POST:
			if 'select' in request.POST:
				option = str(request.POST['select'])
				dateTime =  str(request.POST['date_time'])
				dateTime = dateutil.parser.parse(dateTime)
				seats = int(request.POST['seats'])
				sourceChoice = request.POST['source']
				destChoice = request.POST['dest']
					
				[typ,pk] = option.split("|")
				if typ=='s':
					obj = Booking.objects.get(id=pk)
					print obj
					if obj.seats_left > 0:
						obj.resv.add(User.objects.get(username=request.user))
						seats = obj.seats_left - seats
						if seats<0:
							seats =0
						obj.seats_left = seats
					obj.save()
					context['message']="Your seats were reserved with book id = " + str(pk)
				elif typ=='n':
					obj = Car.objects.get(vehicle_id=pk)
					print obj
					obj.parked_at=destChoice
					obj.avail_from=dateTime + timedelta(hours=3)
					obj.avail_till = dateTime - timedelta(hours=2)
					obj.save()
					bookObj = Booking.objects.create(date_time=dateTime,source=sourceChoice,dest=destChoice,vehicle_id=obj,seats_left=obj.capacity-seats)
					if bookObj.seats_left < 0:
						bookObj.seats_left=0
					bookObj.resv.add(User.objects.get(username=request.user))
					bookObj.save()
					context['message'] = "Car was booked with id = "+str(bookObj.id)

			else:
				context['message'] = "Please choose at least one entry for booking."
			data = {'date':timezone.localtime(timezone.now()).date(),}
			bookingQueryForm = BookingQueryForm(initial=data,prefix='booking')
			dateChoice = timezone.localtime(timezone.now()).date()
			dateChoice = (dateChoice,dateChoice+timedelta(days=1))
			booking = BookingQueryTable( Booking.objects.filter(date_time__gte=timezone.localtime(timezone.now()),date_time__range=dateChoice))
			RequestConfig(request,paginate=False).configure(booking)
			data = {'day':timezone.localtime(timezone.now()).weekday(),}
			scheduleQueryForm=ScheduleQueryForm(initial=data,prefix='schedule')
			schedule = ScheduleQueryTable(Schedule.objects.filter(day=timezone.localtime(timezone.now()).weekday()))
			RequestConfig(request,paginate=False).configure(schedule)
			context['schedule'] = schedule
			context['scheduleQueryForm'] = scheduleQueryForm
			context['booking'] = booking
			context['bookingQueryForm'] = bookingQueryForm

			return render(request,"bookSuccess.html",context)
	else:
		dateTimeChoice = timezone.localtime(timezone.now())
		data = {'date_time':dateTimeChoice,'seats':1}
		preBookingForm = PreBookingForm(initial=data,prefix='preBook')
		dateChoice = timezone.localtime(timezone.now()).date()
		dateChoice = (dateChoice,dateChoice+timedelta(days=1))
		booking = BookingShareTable( Booking.objects.filter(date_time__gte=dateTimeChoice,seats_left__gte=1))
		new = BookingNewTable( Car.objects.filter(capacity__gte=1).exclude(avail_from__gte=dateTimeChoice,avail_till__lte=dateTimeChoice))
		RequestConfig(request,paginate=False).configure(booking)
		RequestConfig(request,paginate=False).configure(new)
		context['seats'] = 1
		context['date_time'] = str(dateTimeChoice)
		context['preBookingForm'] = preBookingForm
		context['booking'] = booking
		context['new'] = new
	


	return render(request,"staffBook.html",context)

def about(request):
	return render(request,"about.html",{})

def contact(request):
	return render(request,"contact.html",{})


# def staff(request):
# 	context = {'message':""}
# 	if request.method=='POST':
# 		if 'scheduleQuery' in request.POST:
# 			scheduleQueryForm = ScheduleQueryForm(request.POST,prefix='schedule')
# 			if scheduleQueryForm.is_valid():
# 				print scheduleQueryForm.cleaned_data
# 				dayChoice = int(scheduleQueryForm.cleaned_data.get('day'))
# 				sourceChoice = scheduleQueryForm.cleaned_data.get('source')
# 				destChoice = scheduleQueryForm.cleaned_data.get('dest')
# 				schedule = ScheduleQueryTable(Schedule.objects.filter(day=dayChoice,source=sourceChoice,dest=destChoice))
# 				RequestConfig(request,paginate=False).configure(schedule)
# 			data = {'date':timezone.localtime(timezone.now()).date(),'source':'M','dest':'K'}
# 			bookingQueryForm = BookingQueryForm(initial=data,prefix='booking')
# 			dateChoice = timezone.localtime(timezone.now()).date()
# 			dateChoice = (dateChoice,dateChoice+timedelta(days=1))
# 			booking = BookingQueryTable( Booking.objects.filter(date_time__range=dateChoice))
# 			RequestConfig(request,paginate=False).configure(booking)
# 			context['schedule'] = schedule
# 			context['scheduleQueryForm'] = scheduleQueryForm
# 			context['booking'] = booking
# 			context['bookingQueryForm'] = bookingQueryForm

# 		elif 'bookingQuery' in request.POST:
# 			bookingQueryForm = BookingQueryForm(request.POST,prefix='booking')
# 			if bookingQueryForm.is_valid():
# 				print bookingQueryForm.cleaned_data
# 				dateChoice = bookingQueryForm.cleaned_data.get('date')
# 				dateChoice = (dateChoice,dateChoice+timedelta(days=1))
# 				sourceChoice = bookingQueryForm.cleaned_data.get('source')
# 				destChoice = bookingQueryForm.cleaned_data.get('dest')
# 				booking = BookingQueryTable( Booking.objects.filter(date_time__range=dateChoice,source=sourceChoice,dest=destChoice))
# 				RequestConfig(request,paginate=False).configure(booking)
# 			data = {'day':timezone.localtime(timezone.now()).weekday(),'source':'M','dest':'K'}
# 			scheduleQueryForm=ScheduleQueryForm(initial=data,prefix='schedule')
# 			schedule = ScheduleQueryTable(Schedule.objects.filter(day=timezone.localtime(timezone.now()).weekday()))
# 			RequestConfig(request,paginate=False).configure(schedule)
# 			context['schedule'] = schedule
# 			context['scheduleQueryForm'] = scheduleQueryForm
# 			context['booking'] = booking
# 			context['bookingQueryForm'] = bookingQueryForm
# 	else:
# 		data = {'date':timezone.localtime(timezone.now()).date(),'source':'M','dest':'K'}
# 		bookingQueryForm = BookingQueryForm(initial=data,prefix='booking')
# 		dateChoice = timezone.localtime(timezone.now()).date()
# 		dateChoice = (dateChoice,dateChoice+timedelta(days=1))
# 		booking = BookingQueryTable( Booking.objects.filter(date_time__range=dateChoice))
# 		RequestConfig(request,paginate=False).configure(booking)
# 		data = {'day':timezone.localtime(timezone.now()).weekday(),'source':'M','dest':'K'}			
# 		scheduleQueryForm=ScheduleQueryForm(initial=data,prefix='schedule')
# 		schedule = ScheduleQueryTable(Schedule.objects.filter(day=timezone.localtime(timezone.now()).weekday()))
# 		RequestConfig(request,paginate=False).configure(schedule)
# 		context['schedule'] = schedule
# 		context['scheduleQueryForm'] = scheduleQueryForm
# 		context['booking'] = booking
# 		context['bookingQueryForm'] = bookingQueryForm
# 	return render(request,"staffHome.html",context)
