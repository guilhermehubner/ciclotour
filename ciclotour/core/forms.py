from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=254)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': 'Por favor informe e-mail e senha válidos!',
        'inactive': 'Este e-mail ainda não foi confirmado.',
    }

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(username=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': 'E-mail'},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache
