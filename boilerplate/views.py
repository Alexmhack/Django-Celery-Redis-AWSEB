from django.shortcuts import render

from .tasks import add

def index_view(request):
	context = dict()
	if request.method == "POST":
		a = request.POST.get('a')
		b = request.POST.get('b')
		add.apply_async((a, b))
	return render(request, 'index.html', context)
