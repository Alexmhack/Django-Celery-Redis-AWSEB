from django.shortcuts import render

from .tasks import add

def index_view(request):
	context = dict()
	if request.method == "POST":
		a = request.POST.get('a')
		b = request.POST.get('b')
		result = add.apply_async((a, b))
		context['result'] = result.get()
	return render(request, 'index.html', context)
