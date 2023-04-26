from django import forms
from captcha.fields import CaptchaField
from .models import Contact, Newsletter

class NameForm(forms.Form):
    name = forms.CharField(max_length=255)


class ContactForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['subject'].required = False


class NewsletterForm(forms.ModelForm):

    class Meta():
        model = Newsletter
        fields = '__all__'

    def is_valid(self):
        email = self.data["email"]
        if Newsletter.objects.filter(email=email).exists():
            self.add_error("email", "your email already exists.")
        return super().is_valid()
