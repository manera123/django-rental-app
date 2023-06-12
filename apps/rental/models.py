from django.contrib.gis.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import User
from django.utils import timezone

# Create your models here.

#Defining the Room model.

#Defining the Room Image model (used whenever a room has more than one image).
# class RoomImage(models.Model):

#     room_id_img = models.ForeignKey(Room, related_name='room_img', on_delete=models.CASCADE, null=False)
#     picture = models.FileField(upload_to='user_images',blank=True,null=True)

# #Defining the Room Rating model.
# class RoomRating(models.Model):

#     room_id_rate = models.ForeignKey(Room, related_name='room_rate', on_delete=models.CASCADE, null=False)
#     renter_id_rate = models.ForeignKey(User, related_name='renter_rate', on_delete=models.CASCADE, null=False)
#     date = models.DateField(null=False)
#     rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
#     secondary_id = models.IntegerField()

# #Defining the Host Rating model.
# class HostRating(models.Model):

#     host_id_hostRate = models.ForeignKey(User, related_name='host_hostRate', on_delete=models.CASCADE, null=False)
#     renter_id_hostRate = models.ForeignKey(User, related_name='renter_hostRate', on_delete=models.CASCADE, null=False)
#     date = models.DateField(null=False)
#     rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])



#Defining the ClickedItem model (used for the Recommendation system).
# class ClickedItem(models.Model):

#     room_id_click = models.ForeignKey(Room, related_name='room_click', on_delete=models.CASCADE, null=False)
#     renter_id_click = models.ForeignKey(User, related_name='renter_click', on_delete=models.CASCADE, null=False)

# #Defining the SearchedItem model (used for the Recommendation system).
# class SearchedItem(models.Model):

#     room_id_search = models.ForeignKey(Room, related_name='room_search', on_delete=models.CASCADE, null=False)
#     renter_id_search = models.ForeignKey(User, related_name='renter_search', on_delete=models.CASCADE, null=False)

# #Defining the Recommendation model (used for the Recommendation system).
# class Recommendation(models.Model):

#     room_id_rec = models.ForeignKey(Room, related_name='room_recom', on_delete=models.CASCADE, null=False)
#     renter_id_rec = models.ForeignKey(User, related_name='renter_recom', on_delete=models.CASCADE, null=False)


class NewAdvt(models.Model):
    host = models.ForeignKey(User, related_name='host_new_advts', on_delete=models.CASCADE, null=False)
    is_completed = models.BooleanField(default=False)
    is_documents_checked = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)


class NewAdvtLocation(models.Model):
    advt = models.ForeignKey(NewAdvt, related_name='new_advt_location', on_delete=models.CASCADE, null=False)
    country = models.CharField(max_length=50, null=False)
    region = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    street = models.CharField(max_length=100, null=False)


class NewAdvtInformation(models.Model):

    NO = "Нет"
    ON_STREET = "На улице"
    IN_BUILDING = "В здании"
    
    PARKING_CHOICES = (
        (NO, "Нет"),
        (ON_STREET, "На улице"),
        (IN_BUILDING, "В здании")
    )

    advt = models.ForeignKey(NewAdvt, related_name='new_advt_information', on_delete=models.CASCADE, null=False)

    floor = models.IntegerField(null=False, default=1)
    floors_at_house = models.IntegerField(null=False, default=1)
    parking = models.CharField(choices=PARKING_CHOICES, default=NO, max_length=20)

    square_feet = models.FloatField(null=False)
    number_of_rooms = models.CharField(null=False, max_length=20)

    balcony = models.BooleanField(default=False)
    loggia = models.BooleanField(default=False)

    air_conditioner = models.BooleanField(default=False)
    dishwasher = models.BooleanField(default=False)
    fridge = models.BooleanField(default=False)
    water_heater = models.BooleanField(default=False)
    stove = models.BooleanField(default=False)
    tv = models.BooleanField(default=False)
    microwave = models.BooleanField(default=False)
    hair_dryer = models.BooleanField(default=False)
    washing_machine = models.BooleanField(default=False)
    iron = models.BooleanField(default=False)

    wi_fi = models.BooleanField(default=False)
    cabel_TV = models.BooleanField(default=False)

    bed_sheets = models.BooleanField(default=False)
    towels = models.BooleanField(default=False)
    hygiene_products = models.BooleanField(default=False)


    max_people = models.CharField(null=False, max_length=20)

    childs = models.BooleanField(default=False)
    smoking = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    events = models.BooleanField(default=False)
    accounting_documents = models.BooleanField(default=False)
    monthly_rent = models.BooleanField(default=False)

  

    
class NewAdvtLastStep(models.Model):
    advt = models.ForeignKey(NewAdvt, related_name='new_advt_last_step', on_delete=models.CASCADE, null=False)

    description = models.TextField(max_length=2000, null=False)
    video = models.URLField(null=True, blank=True)
    rep_photo = models.FileField(upload_to='new_advt_main_images',blank=True,null=False)
    price = models.IntegerField( null=False)
    deposit = models.IntegerField(blank=True, null=True)


class NewAdvtImages(models.Model):
    advt = models.ForeignKey(NewAdvt, related_name='new_advt_images', on_delete=models.CASCADE, null=False)
    image = models.FileField(upload_to='new_advt_addition_images',blank=True,null=True)

class UserFavoriteAdvt(models.Model):
    user = models.ForeignKey(User, related_name='user_favorites', on_delete=models.CASCADE, null=False)
    advt = models.ForeignKey(NewAdvt, related_name='in_user_favorites', on_delete=models.CASCADE, null=False)



#Defining the Reservation model.
class AdvtReservation(models.Model):
    UNDER_CONSID = "На рассмотрении"
    ACCEPTED = "Принят"
    CANCELED_BY_HOST = "Отклонён"
    CANCELED_BY_USER = "Отменён"
    ENDED = "Завершён"
    
    STATUS_CHOICES = (
        (UNDER_CONSID, "На рассмотрении"),
        (ACCEPTED, "Принят"),
        (CANCELED_BY_HOST, "Отклонён"),
        (CANCELED_BY_USER, "Отменён"),
        (ENDED, "Завершён"),
    )
    advt = models.ForeignKey(NewAdvt, related_name='reservations', on_delete=models.CASCADE, default=None, null=False)
    renter = models.ForeignKey(User, related_name='user_reservations', on_delete=models.CASCADE, default=None, null=False)
    time_stamp = models.DateTimeField(default=timezone.now)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    status = models.CharField(choices=STATUS_CHOICES, default=UNDER_CONSID, max_length=30)


class DocumentsCheckRequest(models.Model):
    requester = models.ForeignKey(User, related_name='user_documents_check_requests', on_delete=models.CASCADE, default=None, null=False)
    time_stamp = models.DateTimeField(default=timezone.now)
    is_processed = models.BooleanField(default=False)