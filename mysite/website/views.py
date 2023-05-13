from django.shortcuts import redirect
from django.views.generic import View, TemplateView, CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ContactForm, NewsletterForm


# def index(request):
#   return render(request, 'website/index.html')


class IndexView(TemplateView):
    template_name = "website/index.html"


# def about(request):
#   return render(request, 'website/about.html')


class AboutView(TemplateView):
    template_name = "website/about.html"


# def contact(request):
#   if request.method == 'POST':
#     form = ContactForm(request.POST)
#     if form.is_valid():
#       newform = form.save(commit=False)
#       newform.name = 'anonymous'
#       newform.save()
#       messages.success(request, 'your ticket submitted successfully.')
#     else:
#       messages.error(request, "your ticket didn't submitted.")
#   else:
#     form = ContactForm()
#   return render(request, 'website/contact.html', {'form': form})


class ContactView(SuccessMessageMixin, CreateView):
    template_name = "website/contact.html"
    form_class = ContactForm
    success_url = "/contact/"
    success_message = "your ticket submitted successfully."

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


# def newsletter(request):
#   if request.method == 'POST':
#     form = NewsletterForm(request.POST)
#     if form.is_valid():
#       form.save()
#       messages.success(request, 'your ticket submitted successfully.')
#       return HttpResponseRedirect('/')
#   messages.error(request, "your ticket didn't submitted.")
#   return HttpResponseRedirect('/')


class NewsletterView(SuccessMessageMixin, View):
    form_class = NewsletterForm

    def post(self, request, *args, **kwarg):
        form = self.form_class(request.POST)
        if form.is_valid():
            messages.success(request, "your ticket submitted successfully.")
            form.save()
        else:
            for error in form.errors.values():
                messages.error(request, error)
        path = "/"
        if last_page := request.GET.get("lastPage"):
            path = last_page
        return redirect(path)
