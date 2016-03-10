from django.shortcuts import render

def frontpage(request):
	if request.user.is_authenticated():
		return render(request, 'index.html')
	else:
		return render(request, 'splash.html')