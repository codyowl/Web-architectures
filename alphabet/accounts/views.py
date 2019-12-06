from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Company, UserTable, USER_ROLES
from accounts.serializers import CompanySerializer, UserTableSerializer
from dynamic_db_router import in_database
from utilities.database_creator import database_dict, create_database, migrate_new_database
from django.conf import settings
from django.core import management
import time

'''
USER_ROLES = (
	(0, 'Owner'),
	(1, 'User'),
	)
'''

class CompanyView(APIView):
	def get(self, request):
		company = Company.objects.all()
		serializer = CompanySerializer(company, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = CompanySerializer(data=request.data)
		company_name = request.data['company_name']
		first_name = request.data['first_name']
		email_id = request.data['email_id']
		phone_no = request.data['phone_no']
		created_by = request.data['created_by']
		
		if serializer.is_valid():
			company = Company.objects.create(
					company_name = company_name,
					first_name = first_name,
					email_id = email_id,
					phone_no = phone_no,
					role = USER_ROLES[0][0],
					created_by = created_by
					)   

			
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def delete(self, request, pk, format=None):
		company = get_object_or_404(Company, pk=pk) 
		company.delete()
		return Response({'message':'company deleted'},status=status.HTTP_204_NO_CONTENT)

class UserTableView(APIView):
	

	def post(self, request):
		serializer = UserTableSerializer(data=request.data)
		company_name = request.data['company_name']
		first_name = request.data['first_name']
		email_id = request.data['email_id']
		phone_no = request.data['phone_no']
		
		if serializer.is_valid():
			try: 
				Company.objects.get(company_name=company_name)
			
				with in_database(company_name, write=True):
					UserTable.objects.create(
						company_name = company_name,
						first_name = first_name,
						email_id = email_id,
						phone_no = phone_no,
						role = USER_ROLES[1][0]
							)   

			except Company.DoesNotExist:				 
				# creating company record on Account database
				company = Company.objects.create(
					company_name = company_name,
					first_name = first_name,
					email_id = email_id,
					phone_no = phone_no,
					role = USER_ROLES[0][0],
					created_by = "usersignup"
					)   

				# creating database dynamically for the newly registered compnay in Company table
				new_database_config = database_dict(company_name)
				# automating the process of creating database on mysql end
				create_database(company_name)
				time.sleep(5)
				# updating the new database config to DATABASE in settings
				settings.DATABASES.update({company_name : new_database_config})
				# automating the process of database migrations
				migrate_new_database(company_name)
				time.sleep(20)
				print ("Database migration done !")
				# now inserting the user records into created database
				with in_database(company_name, write=True):
					UserTable.objects.create(
						company_name = company_name,
						first_name = first_name,
						email_id = email_id,
						phone_no = phone_no,
						role = USER_ROLES[0][0]
							)                   
			return Response(serializer.data, status=status.HTTP_201_CREATED)

	def delete(self, request, pk, company_name, format=None):
		with in_database(company_name, write=True): 
			user = get_object_or_404(UserTable, pk=pk) 
			user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)