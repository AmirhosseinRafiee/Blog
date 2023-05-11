from django.db import models
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name