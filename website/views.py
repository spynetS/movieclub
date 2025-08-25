from django.shortcuts import render

from accounts.models import Profile
from clubs.models import Club

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html",{})
    return render(request, "index.html",{})

def add_member_modal(request):
    query = request.GET.get("search", "")
    users = Profile.objects.none()
    if query:
        users = Profile.objects.filter(username__icontains=query)[:10]
    return render(request, "components/add_member_modal.html", {"users": users})
