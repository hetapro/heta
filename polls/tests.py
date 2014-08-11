import datetime
from django.utils import timezone
from django.test import TestCase

 # Create your tests here.

from polls.models import Poll
from django.core.urlresolvers import reverse

def create_poll(question, days):
   return Poll.objects.create(questions=questions, pub_date=timezone.now()+datetime.timedelta(days=days))


class PollViewTests(TestCase):
   def test_index_view_with_no_poll(self):
      """If no polls exist, an appropriate message should be displayed."""
      response=self.client.get(reverse('polls:index'))
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, "No polls are available.")
      self.assertQuerysetEqual(response.context['latest_poll_list'],[])

   def test_index_view_with_a_past_poll(self):
      create_poll(questions="Past poll.", days=-30)
      response=self.client.get(reverse('polls:index'))
      self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: Past poll.>'])
   
   def test_index_view_with_a_future_poll(self):
      create_poll(questions="Future poll.", days=30)
      response=self.client.get(reverse('polls:index'))
      self.assertContains(response, "No polls are available.", status_code=200)
      self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: Past poll.>'])

   def test_index_view_with_future_poll_and_past_poll(self):
      create_poll(questions="Past poll.", days=-30)
      create_poll(questions="Future poll.", days=30)
      response=self.client.get(reverse('polls:index'))
      self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll:Past poll.>'])

   def test_index_view_with_two_past_polls(self):
      create_poll(questions="Past poll 1.", days=-30)
      create_poll(questions="Past poll 2.", days=-5)
      response=self.client.get(reverse('polls:index'))
      self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll:Past poll2.>'] ,['<Poll:Past poll1.>'])

class PollIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_poll(self):
        """
        The detail view of a poll with a pub_date in the future should
        return a 404 not found.
        """
        future_poll = create_poll(question='Future poll.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_poll(self):
        """
        The detail view of a poll with a pub_date in the past should display
        the poll's question.
        """
        past_poll = create_poll(question='Past Poll.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
        self.assertContains(response, past_poll.question, status_code=200)
