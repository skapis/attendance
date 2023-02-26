from django.shortcuts import render
from .models import UserProfile
from django.contrib.auth.decorators import login_required


@login_required(login_url='/authentication/login')
def account(request):
    profile = UserProfile.objects.get(owner=request.user)
    context = {
        'profile': profile
    }
    return render(request, 'user/index.html', context)


# TODO: user can change password
