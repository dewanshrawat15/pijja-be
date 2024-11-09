from django.db import models
from django.utils import timezone
import random
import string
from .constants import pizza_names

GENDER_CHOICES = (
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("NONE", "Prefer not to disclose"),
)

PIZZA_STATES = (
    ("CREATED", "Created"),
    ("PURCHASED", "Purchased"),
    ("LOGGED", "Logged"),
)

def random_generate_id(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def generate_user_id():
    return random_generate_id(11)

def generate_pizza_id():
    return random_generate_id(20)


def generate_money_paise(start, end):
    return random.randrange(start, end)

def generate_random_pizza_price():
    return generate_money_paise(25000, 99900)

def generate_wallet_amount():
    return generate_money_paise(2500000, 9990000)

def pick_random_pizza_name():
    return random.choice(pizza_names)

class Pijja(models.Model):
    name = models.CharField(max_length=192, default=pick_random_pizza_name)
    pijja_id = models.CharField(max_length=32, primary_key=True, default=generate_pizza_id)
    price = models.FloatField(default=generate_random_pizza_price)
    purchased_by = models.ForeignKey('DumDumUser', on_delete=models.CASCADE, default=None, null=True)
    purchased_at = models.DateTimeField(default=timezone.now)
    state = models.CharField(choices=PIZZA_STATES, max_length=20, default="CREATED")
    last_modified_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.pijja_id
    
    def mark_pijja_bought(self, user):
        self.state = "PURCHASED"
        self.last_modified_at = timezone.now()
        self.purchased_by = user
        self.save()
    
    def mark_pijja_logged(self):
        self.state = "LOGGED"
        self.last_modified_at = timezone.now()
        self.save()


class DumDumUser(models.Model):
    user_id = models.CharField(max_length=12, primary_key=True,default=generate_user_id)
    user_name = models.CharField(max_length=128)
    age = models.IntegerField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=32, default="NONE")
    wallet_amount = models.FloatField(default=generate_wallet_amount)

    def __str__(self) -> str:
        return self.user_name
    
    def bought_pizza(self, pijja: Pijja):
        updatedWalletAmount = self.wallet_amount - pijja.price
        self.wallet_amount = updatedWalletAmount
        pijja.mark_pijja_bought(self)
        self.save()