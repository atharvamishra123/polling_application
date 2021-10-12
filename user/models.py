from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=250, null=False)
    name = models.CharField(max_length=50, null=False)
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=15, null=False)
    user = models.ManyToManyField('self', through='Relationship', symmetrical=False, related_name='related_to')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    def get_all_polls(self):
        pass

    def create_relationship(self, person):
        status, obj = Relationship.objects.get_or_create(
            to_person=person,
            from_person=self,
        )
        return status

    def remove_relationship(self, person):
        Relationship.objects.filter(
            from_person=self,
            to_person=person
        ).delete()
        return 'dummy_value'

    def get_all_followings(self):
        return self.user.all()


class Relationship(models.Model):
    from_person = models.ForeignKey(CustomUser, related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(CustomUser, related_name='to_person', on_delete=models.CASCADE)
