from django.shortcuts import render
from . forms import UserForm, UserProfileForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect
from django.views.generic import CreateView

from . forms import UserForm

from . models import UserProfile

class signup(CreateView):
    form_class = UserForm
    model = UserProfile

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(User.objects.make_random_password())
        obj.save()

        # This form only requires the "email" field, so will validate.
        reset_form = PasswordResetForm(self.request.POST)
        reset_form.is_valid()  # Must trigger validation
        # Copied from django/contrib/auth/views.py : password_reset
        opts = {
            'use_https': self.request.is_secure(),
            'email_template_name': 'verification.html',
            'subject_template_name': 'verification_subject.txt',
            'request': self.request,
            # 'html_email_template_name': provide an HTML content template if you desire.
        }
        # This form sends the email on save()
        reset_form.save(**opts)

        return redirect('home:signup-done')

def home(request):
    return render(
        request,
        'home.html',
    )