from django.db import models 

# Create your models here.

import datetime
from django.utils import timezone

class Poll(models.Model):
   questions=models.CharField(max_length=200)
   pub_date=models.DateTimeField('date published')
   def __unicode__(self):
      return self.questions
   def was_published_recently(self):
      now=timezone.now()
      return now-datetime.timedelta(days=1)<=self.pub_date<=now
   def test_was_published_recently_with_old_poll(self):
      old_poll=Poll(pub_date=timezone.now()-datetime.timedelta(days=30))
      self.assertEqual(old_poll.was_published_recently(),False)
   def test_was_published_recently_with_recent_poll(self):
      recent_poll=Poll(pub_date=timezone.now()-datetime.timedelta(hours=1))
      self.assertEqual(recent_poll.was_published_recently(),True)
   was_published_recently.admin_order_field='pub_date'
   was_published_recently.boolean=True
   was_published_recently.short_description='published recentaly?'

class Choice(models.Model):
   poll=models.ForeignKey(Poll)
   choice_text=models.CharField(max_length=200)
   votes=models.IntegerField(default=0)
   def __unicode__(self):
      return self.choice_text