from django.db import models

# Create your models here.
class Profile(models.Model):
    employee_id = models.IntegerField()
    name = models.CharField(
        max_length=64, null=True,
        blank=True
    )
    email = models.EmailField(
        null=True,
        blank=True
    )


class ProfileLogs(models.Model):
    profile_id = models.ForeignKey(
        'demo.Profile',
        on_delete=models.CASCADE,
    )
    LOG_CHOICES = (
        ('1', 'entry'),
        ('2', 'exit'),
    )
    log_type = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        choices=LOG_CHOICES
    )
    log_timestamp = models.DateTimeField(
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)