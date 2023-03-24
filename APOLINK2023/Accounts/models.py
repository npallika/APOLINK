from django.db import models

from django.contrib.auth.models import User
# Create your models here.



class Country(models.Model):
    code = models.CharField(max_length=3, null=True)
    phoneCode = models.CharField(max_length=4, null=True)
    name = models.CharField(max_length=30, null=True)
    
    def __str__(self):
        return self.name + " : " + self.phoneCode
		
    
    def get_simple_name(self):
        return self.name    


class Address(models.Model):
    street_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=30, null=True)
    region = models.CharField(max_length=20, null=True)
    zipcode = models.CharField(max_length=30, null=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.street_address + "\n" + self.zipcode + " " + self.city + ", " + self.region + "\n" + self.country.name

class Industry_Type(models.Model):
    name = models.CharField(max_length=30, null=True)
    def __str__(self):
        return self.name


class PlatformUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50, null=True)
    industry = models.ForeignKey(Industry_Type, null=True, on_delete=models.CASCADE)
    company_position = models.CharField(max_length=20, null=True)

    main_address = models.ForeignKey(Address, null=True, related_name = 'main_address', on_delete=models.CASCADE)
   # other_addresses = models.ManyToManyField(Address, blank= True, related_name = 'other_addresses')

    phone_landline_country = models.ForeignKey(Country, null=True, blank= True, on_delete=models.CASCADE, related_name = 'landline_country')
    phone_landline_number = models.CharField(max_length=12, null=True, blank=True)
    phone_mobile_country = models.ForeignKey(Country, null=True, blank= True, on_delete=models.CASCADE, related_name = 'mobile_country')
    phone_mobile_number = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return self.user.username
