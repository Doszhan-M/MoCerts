from allauth.account.forms import LoginForm


class MyLoginForm(LoginForm):

    def save(self, request):
        user = super(MyLoginForm, self).save(request)
        return user