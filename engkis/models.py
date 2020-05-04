from django.db import models

class Word(models.Model):
    english = models.CharField(max_length=150)
    kiswahili = models.CharField(max_length=150)
    translatedyes = models.IntegerField(default=0)

    def __str__(self):
        return self.english
