from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse

from .forms import NameForm, ContactForm
from .models import Question, Choice, QuestionForm
from django.views import generic

from django.contrib import messages

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

    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        print(request.POST['choice'])
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))  

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'polls/name.html', {'form': form})


def get_contact(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['info@example.com']
            if cc_myself:
                recipients.append(sender)

            print(subject, message, sender, recipients, cc_myself)
            return HttpResponseRedirect('/thanks/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, 'polls/contact.html', {'form': form})    

def question_create(request):
   
    if request.method == 'POST':

        form = QuestionForm(request.POST)

        if form.is_valid():
            form.save()
            messages.info(request, 'Question has been created.')
            return render(request, 'polls/index.html')
            #return HttpResponseRedirect(reverse('polls:index')) 
    else:
        form = QuestionForm()

    return render(request, 'polls/question_create.html', {'form': form})           

def question_edit(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':

        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():

            form.save()

            messages.info(request, 'Question has been successfully saved')

            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))  

        else:
            messages.error(request, 'Question has not been saved.')             

    else:
        form = QuestionForm(instance=question)

    return render(request, 'polls/question_edit.html', {'form': form, 'question_id': question_id})           


def question_delete(reques, question_id):
    question = get_object_or_404(Question, pk=question_id)

    question.delete()

    messages.info(request, 'Question has been deleted.')

    return HttpResponseRedirect(reverse('polls:index')) 