from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import User, Project, Right, Tag, Record, Weight, Identification
import random

# Application view
def index(request):
    try:
        identified_tag = get_object_or_404(Tag, pk=request.POST['tag'])
        current_record = get_object_or_404(Record, pk=request.POST['record'])
        project_phase = current_record.project.phase
        identification = Identification(record=current_record, tag=identified_tag, phase=project_phase)
        identification.save()
        return HttpResponseRedirect(request.path_info)
    except:
        recordings = Record.objects.filter(file_on_server=True)
        probabilities = recordings.values_list('importance', flat=True)
        random_record = random.choices(recordings, weights=probabilities)[0]

        tags_with_weights = [weight.tag for weight in random_record.weights.all()]
        tags_without_weights = list(Tag.objects.exclude(id__in=[tag.id for tag in tags_with_weights]))
        all_tags = tags_with_weights + tags_without_weights

        context = {
            'random_record': random_record,
            'tags': all_tags,
        }
        return render(request, 'birds/index.html', context)