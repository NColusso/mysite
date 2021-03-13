from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib import messages
from .forms import QuestionForm

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory

from .models import Question, Choice

class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    """Return the last five published questions."""
    return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Question
  template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
  model = Question
  template_name = 'polls/results.html'

class DeleteView(generic.DeleteView):
  model = Question
  template_name = 'polls/delete.html'
  context_object_name = 'total_votes'
  success_url = reverse_lazy('polls:index')

  def get_total_votes(self):
    total_votes = 0
    for choice in Question.choice_set.all:
      total_votes += choice.votes
      print(total_votes)
    return "TEsTING"

  total_votes = get_total_votes

def add_question(request):
  if request.method == 'POST':
   
    choices = []
    choice1 = request.POST.get('choice1')
    choice2 = request.POST.get('choice2')
    choice3 = request.POST.get('choice3')
    choice4 = request.POST.get('choice4')
    if (choice1):
      choices.append(choice1)
    if (choice2):
      choices.append(choice2)
    if (choice3):
      choices.append(choice3)
    if (choice4):
      choices.append(choice4)

    question_form = QuestionForm(request.POST, instance=Question())

    if question_form.is_valid():
      new_question = question_form.save()
      print(new_question.id)
      for c in choices:
        Choice.objects.create(choice_text=c, question=new_question)
      return HttpResponseRedirect('/polls/')

  else:
    question_form = QuestionForm(request.POST, instance=Question())
    return render(request, 'polls/create.html', {'q_form': question_form})
    


def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    # in this case redisplay the question voting form
    return render(request, 'polls/detail.html', {
      'question': question,
      'error_message': "You didn't select a choice",
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    # Always return HttpResponseRedirect after successfully handling POST data.
    # This prevents data from being posted twice if user hits back button
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
