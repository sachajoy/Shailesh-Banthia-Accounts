from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def index(request):
    if request.user.is_authenticated:
        return render(
            request,
            'authentication/index.html',
            {
                'name': 'User is loged in'
            }
        )
    context = {
        'user': request.user
    }
    return render(
        request, 
        'authentication/index.html',
        context
    )
