from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Bird, Recording, Evaluation
import random

# Application view
def index(request):
    try:
        selected_bird = get_object_or_404(Bird, pk=request.POST['bird'])
        selected_recording = get_object_or_404(Recording, pk=request.POST['record'])
        evaluation = Evaluation(recording=selected_recording, bird=selected_bird)
        evaluation.save()
    except:
        pass
    recordings = Recording.objects.filter(has_file=True)
    probabilities = recordings.values_list('weight', flat=True)
    random_record = random.choices(recordings, weights=probabilities)[0]
    other_birds = Bird.objects.exclude(no1_recordings=random_record).exclude(no2_recordings=random_record).exclude(name="Other animal").exclude(name="Noise").order_by('name')
    context = {
        'random_record': random_record,
        'other_birds': other_birds,
    }
    return render(request, 'birds/index.html', context)