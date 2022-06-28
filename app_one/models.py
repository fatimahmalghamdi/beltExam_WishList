from django.db import models
import re

class UserManager(models.Manager):
    # Validate registration
    def basic_validator_registration(self, postData):
        reg_errors = {}
        if len(postData['the_name']) < 3:
            reg_errors["the_name"] = "The name should not be null, or less than three chars"
        if len(postData['user_name']) < 3:
            reg_errors['user_name'] = "The user_name should not be null, or less than three chars"
        if len(postData['reg_pass']) < 8:
            reg_errors['reg_pass'] = "The password should not be null, or less than eight numers"
        return reg_errors
    
    # Validate login
    def basic_validator_login(self, postData):
        login_errors = {}
        if len(postData['log_userName']) < 3:
            login_errors["log_userName"] = "The user_name should not be null, or less than three chars"
        if len(postData['login_pass']) < 8:
            login_errors['login_pass'] = "The password should not be null, or less than eight chars"
        return login_errors
    
    # Validate Product Name
    def basic_validator_productName(self, postData):
        product_errors = {}
        if len(postData['product']) < 3:
            product_errors["product"] = "The product should not be null, or less than three chars"
        return product_errors
    


class Users(models.Model):
    name= models.CharField(max_length=100)
    user_name= models.CharField(max_length=100)
    password= models.CharField(max_length=100)
    hired_date= models.DateField()
    objects = UserManager()


class Items(models.Model):
    product_name= models.CharField(max_length=150)
    added_date= models.DateField(auto_now_add=True)
    user= models.ForeignKey(Users, related_name='items', on_delete=models.CASCADE)
    fav_users= models.ManyToManyField(Users, related_name='fav_items', null=True, blank=True)





