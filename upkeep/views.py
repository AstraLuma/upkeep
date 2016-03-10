from django.shortcuts import render

def frontpage(request):
	if request.user.is_authenticated():
		from things.views import stuffindex
		return stuffindex(request)
	else:
		return render(request, 'splash.html')