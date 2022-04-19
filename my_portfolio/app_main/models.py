from django.db import models


# Create your models here.
class Theme(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class Lesson(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.status}"
