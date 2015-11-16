from django.contrib import admin

# Register your models here.
from .models import Bus,Schedule,Car,Booking

class BusAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","reg_no","capacity"]
	class Meta:
		model = Bus

admin.site.register(Bus,BusAdmin)

class ScheduleAdmin(admin.ModelAdmin):
	list_display = ["id","weekday","time","bus_id","source","dest"]
	class Meta:
		model = Schedule

admin.site.register(Schedule,ScheduleAdmin)

class CarAdmin(admin.ModelAdmin):
	list_display = ["vehicle_id","reg_no","capacity","avail_till","avail_from","parked_at"]
	class Meta:
		model = Car

admin.site.register(Car,CarAdmin)

class BookingAdmin(admin.ModelAdmin):
	list_display = ["id","date_time","vehicle_id","resv_by","seats_left","source","dest"]
	class Meta:
		model = Booking

admin.site.register(Booking,BookingAdmin)
