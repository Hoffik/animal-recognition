from django.http import HttpResponseRedirect, HttpResponse
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

# General view for any project
def project(request, project_dir):
    try:
        identified_tag = get_object_or_404(Tag, pk=request.POST['tag'])
        current_record = get_object_or_404(Record, pk=request.POST['record'])
        project_phase = current_record.project.phase
        identification = Identification(record=current_record, tag=identified_tag, phase=project_phase)
        identification.save()
        return HttpResponseRedirect(request.path_info)
    except:
        random_record = None
        all_tags = None
        message = None
        project = Project.objects.filter(directory=project_dir)
        if len(project) == 0:
            context = { 'message': "There is no project in " + project_dir + " directory." }
            return render(request, 'birds/index.html', context)
        
        project = project[0]
        records = Record.objects.filter(project__directory=project_dir, file_on_server=True)
        if len(records) == 0:
            context = { 'message': "There is no record in " + project.name + " project." }
            return render(request, 'birds/index.html', context)
        
        probabilities = records.values_list('importance', flat=True)
        random_record = random.choices(records, weights=probabilities)[0]
        tags_with_weights = [weight.tag for weight in random_record.weights.all()]
        tags_without_weights = list(Tag.objects.filter(project=project).exclude(id__in=[tag.id for tag in tags_with_weights]))
        all_tags = tags_with_weights + tags_without_weights
        if len(all_tags) == 0:
            context = { 'message': "There is no tag in " + project.name + " project." }
        else:
            context = {
                'project': project,
                'random_record': random_record,
                'tags': all_tags,
            }
        return render(request, 'birds/index.html', context)