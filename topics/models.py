from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    """
    Topic 은 사용자가 공부하고 있는 주제입니다.
    """
    LOW = 'L'
    MEDIUM = 'M'
    HIGH = 'H'
    TOP = 'T'
    PROIRITY_CHOICES = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
        (TOP, 'Top'),
    )
    text = models.CharField(max_length=200)
    cre_date = models.DateTimeField('created date', auto_now_add=True)
    description = models.TextField()
    priority = models.CharField(
        max_length=1,
        choices=PROIRITY_CHOICES,
        default=MEDIUM,
    )
    owner = models.ForeignKey(User)

    def __str__(self):
        return '{}({})'.format(self.text, self.priority)
    
class Entry(models.Model):
    """ 
    Entry 는 토픽에 대한 정보 조각입니다.
    """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    cre_date = models.DateTimeField(auto_now_add=True)
    importance = models.IntegerField(default=3)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.title + ' / ' + self.text[:30] + '...'
