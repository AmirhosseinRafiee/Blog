from django.http import HttpResponseRedirect
from django.shortcuts import render
from website.forms import ContactForm, NewsletterForm
from django.contrib import messages

def index(request):
  return render(request, 'website/index.html')

def about(request):
  return render(request, 'website/about.html')

def contact(request):
  if request.method == 'POST':
    form = ContactForm(request.POST)
    if form.is_valid():
      newform = form.save(commit=False)
      newform.name = 'anonymous'
      newform.save()
      messages.success(request, 'your ticket submited successfully.')
    else:
      messages.error(request, "your ticket didn't submited.")
  else:
    form = ContactForm()
  return render(request, 'website/contact.html', {'form': form})


def newsletter(request):
  if request.method == 'POST':
    form = NewsletterForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'your ticket submited successfully.')
      return HttpResponseRedirect('/')
  messages.error(request, "your ticket didn't submited.")
  return HttpResponseRedirect('/')


