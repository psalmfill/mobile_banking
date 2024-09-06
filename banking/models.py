from django.db import models
from authentication.models import CustomUser

class Account(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    account_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.user.username} - {self.account_number}'

# class Transaction(models.Model):
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     transaction_type = models.CharField(max_length=50)
#     date = models.DateTimeField(auto_now_add=True)


# class Account(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     account_number = models.CharField(max_length=20, unique=True)
#     balance = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)
    description = models.TextField()
    recipient = models.CharField(max_length=100, null=True, blank=True)
    sender = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.transaction_type} - {self.amount}'

# from django.db import models
# from django.contrib.auth.models import User
