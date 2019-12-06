from rest_framework import serializers
from accounts.models import Company, UserTable


class CompanySerializer(serializers.Serializer):
	company_name = serializers.CharField(max_length=200)
	first_name = serializers.CharField(max_length=200)
	email_id = serializers.EmailField(max_length=200)
	phone_no = serializers.CharField(max_length=200)
	created_by = serializers.CharField(max_length=200)

	# # for creating data from views
	# def create(self, validated_data):
 #        return Company.objects.create(**validated_data)


class UserTableSerializer(serializers.Serializer):
	company_name = serializers.CharField(max_length=200)
	first_name = serializers.CharField(max_length=200)
	email_id = serializers.EmailField(max_length=200)
	phone_no = serializers.CharField(max_length=200)
	
	# for creating records from views
	# def create(self, validated_data):
	# 	return UserTable.objects.create(**validated_data)