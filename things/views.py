from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Thing, Schedule, Job
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.forms import ModelForm
from django.http import JsonResponse
import datetime
import json

@login_required
def stuffindex(request):
    stuff = Thing.objects.filter(user=request.user)
    return render(request, "things/index.html", {
        'stuff': stuff,
        'jobs': Job.objects.filter(schedule__thing__user=request.user, done=False)
    })


@login_required
def thing(request, thingid):
    thing = get_object_or_404(Thing.objects.accessible_by(request.user), id=thingid)
    return render(request, 'things/thing.html', {
            'object': thing,
            'undonejobs': Job.objects.filter(schedule__thing=thing, done=False)
        })


class ThingForm(ModelForm):
    class Meta:
        model = Thing
        fields = ['name']

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
        return super().form_valid(form)


class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['name', 'period']

# Don't use CreateView because we have to do current user stuff
class AddSchedule(LoginRequiredMixin, FormView):
    template_name = 'things/addschedule.html'
    form_class = ScheduleForm
    success_url = reverse_lazy("things:index")

    def get_thing(self):
        return get_object_or_404(Thing.objects.accessible_by(self.request.user), id=self.args[0])

    def get_context_data(self, **kwargs):
        if 'thing' not in kwargs:
            kwargs['thing'] = self.get_thing()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            sched = form.save(commit=False)
            sched.thing = self.get_thing()
            sched.next_job_at = datetime.date.today() + sched.period
            sched.save()
            self.success_url = sched.thing.get_absolute_url()
        return super().form_valid(form)

@login_required
def undones_json(request):
    ud = Job.objects.filter(schedule__thing__user=request.user, done=False)
    return JsonResponse({'jobs': [{
            'thing': {
                'name': j.schedule.thing.name,
                'id': j.schedule.thing.id,
                'url': j.schedule.thing.get_absolute_url(),
            },
            'schedule': {
                'name': j.schedule.name,
                'id': j.schedule.id,
                'url': j.schedule.get_absolute_url(),
            },
            'when': j.when.isoformat(),
        }
        for j in ud
        ]})

@login_required
def finishjob_json(request):
    if request.method != 'POST':
        return JsonResponse({'msg': 'Try a POST'}, status=405)  # Method Not Allowed
    obj = json.loads(request.body.decode('utf-8'))
    try:
        job = Job.objects.get(pk=obj['job'])
    except Job.DoesNotExist:
        return JsonResponse({'msg': 'Job does not exist'}, status=400)

    job.done = True
    job.save()

    return JsonResponse({'ok': True})
