from django.db import models

# Create your models here.
class TERM_TYPE(models.IntegerChoices):

    PRIVACY = (0, 'privacy')
    T_AND_C = (1, 't&c')
    

class Term(models.Model):

    title = models.CharField(max_length=250)
    description = models.TextField()
    datetime = models.DateTimeField(auto_now=True)

    term_type = models.PositiveSmallIntegerField(choices=TERM_TYPE.choices, default=TERM_TYPE.PRIVACY)

    class Meta:

        verbose_name = 'term'
        verbose_name_plural = 'terms'
    
    def __str__(self):
        return self.title