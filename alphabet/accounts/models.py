from django.db import models


USER_ROLES = (
	('Owner', 'Owner'),
	('User', 'User'),
	)

class Company(models.Model):
	company_name = models.CharField(max_length=120)
	first_name = models.CharField(max_length=120)
	email_id = models.EmailField()
	phone_no = models.CharField(max_length=120)
	role = models.CharField(max_length=250)
	created_by = models.CharField(max_length=120)

	def __str__(self):
		return self.company_name


class UserTable(models.Model):
	company_name = models.CharField(max_length=120)
	first_name = models.CharField(max_length=120)
	email_id = models.EmailField()
	phone_no = models.CharField(max_length=120)
	role = models.CharField(max_length=250,)