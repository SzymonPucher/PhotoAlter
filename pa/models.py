from django.db import models
from django import forms
# Create your models here.


class User(models.Model):
    isGraphicDesigner = models.BooleanField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=18)
    name = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(null=True, blank=True)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return str(self.email) + ' | ' + str(self.name)

    class Meta:
        ordering = ('email',)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='m_sender')
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='m_receiver')
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.sender) + ' -> ' + str(self.receiver)


class Offer(models.Model):
    maker = models.ForeignKey(User, on_delete=models.PROTECT, related_name='o_maker')
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='o_receiver')
    status = models.CharField(max_length=32,
                              choices=(('Active', 'Active'), ('Taken', 'Taken'), ('Paid', 'Paid')))
    description = models.TextField(max_length=2000)

    def __str__(self):
        return str(self.maker) + ' -> ' + str(self.receiver)


class Payment(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='p_sender')
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='p_receiver')
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT)
    status = models.CharField(max_length=32,
                              choices=(('Pending', 'Pending'), ('Finalized', 'Finalized')))
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.amount) + ' | ' + str(self.sender) + ' -> ' + str(self.receiver)


class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT, null=True, blank=True)
    file = models.ImageField()
    important_image_part = models.CharField(max_length=200)

    def __str__(self):
        return str(self.owner) + ' | ' + str(self.offer)
