from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chair.secrets import SECRET_VARIABLE
# Create your views here.
@login_required()
def console(request):
	return render(request, "console.html", context={"secret": SECRET_VARIABLE})