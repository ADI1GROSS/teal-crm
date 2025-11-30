from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Userprofile
from .forms import UserprofileForm
from .forms import CustomSignupForm
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import UserprofileSerializer


class UserprofileViewSet(viewsets.ModelViewSet):
    queryset = Userprofile.objects.all()
    serializer_class = UserprofileSerializer
    permission_classes = [IsAuthenticated]
    
def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/log-in/')
    else:
        form = CustomSignupForm()
    return render(request, 'userprofile/signup.html', {'form': form})

@login_required
def edit_profile(request):
    userprofile = get_object_or_404(Userprofile, user=request.user)

    if request.method == 'POST':
        form = UserprofileForm(request.POST, request.FILES , instance=userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "הפרטים עודכנו בהצלחה!")
            return redirect('userprofile:edit_profile')  
    else:
        form = UserprofileForm(instance=userprofile)
    return render(request, 'userprofile/edit_profile.html', {'form': form, 'userprofile': userprofile})