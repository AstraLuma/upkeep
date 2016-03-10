from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Thing, ThingForm, Schedule, Job
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404

@login_required
def stuffindex(request):
    stuff = Thing.objects.filter(user=request.user)
    return render(request, "things/index.html", {
        'stuff': stuff,
    })

@login_required
def thing(request, thingid):
    thing = get_object_or_404(Thing, id=thingid)
    if request.user.is_superuser or thing.user == request.user:
        return render(request, 'things/thing.html', {
                'object': thing,
            })

# Don't use CreateView because we have to do current user stuff
class AddThing(LoginRequiredMixin, FormView):
    template_name = 'things/addthing.html'
    form_class = ThingForm
    success_url = reverse_lazy("things:index")

    def form_valid(self, form):
        if form.is_valid():
            thing = form.save(commit=False)
            thing.user = self.request.user
            thing.save()
            self.success_url = thing.get_absolute_url()
        return super(AddThing, self).form_valid(form)