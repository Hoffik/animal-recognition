from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics
from itertools import chain
import random

from .models import User, Project, Right, Tag, Record, Weight, Identification
from .serializers import UserSerializer, BasicProjectSerializer, ProjectSerializer, RightSerializer, TagSerializer, RecordSerializer, IdentificationSerializer
from .forms import SignUpForm
from .permissions import IsProjectOwner, IsRightOwner, HasProjectRight

# Main page
# def project(request, project_dir):
#     try:
#         identified_tag = get_object_or_404(Tag, pk=request.POST['tag'])
#         current_record = get_object_or_404(Record, pk=request.POST['record'])
#         project_phase = current_record.project.phase
#         identification = Identification(record=current_record, tag=identified_tag, phase=project_phase, user=request.user)
#         identification.save()
#         return HttpResponseRedirect(request.path_info)
#     except:
#         random_record = None
#         all_tags = None
#         message = None
#         project = Project.objects.filter(directory=project_dir)
#         if len(project) == 0:
#             context = { 'message': "There is no project in " + project_dir + " directory." }
#             return render(request, 'index.html', context)
        
#         project = project[0]
#         records = Record.objects.filter(project__directory=project_dir, file_on_server=True)
#         if len(records) == 0:
#             context = { 'message': "There is no record in " + project.name + " project." }
#             return render(request, 'index.html', context)
        
#         probabilities = records.values_list('importance', flat=True)
#         random_record = random.choices(records, weights=probabilities)[0]
#         tags_with_weights = [weight.tag for weight in random_record.weights.all()]
#         tags_without_weights = list(Tag.objects.filter(project=project).exclude(id__in=[tag.id for tag in tags_with_weights]))
#         all_tags = tags_with_weights + tags_without_weights
#         if len(all_tags) == 0:
#             context = { 'message': "There is no tag in " + project.name + " project." }
#         else:
#             context = {
#                 'project': project,
#                 'random_record': random_record,
#                 'tags': all_tags,
#             }
#         return render(request, 'index.html', context)

# Application views
class ProjectListView(TemplateView):
    template_name = "project_list.html"

class ProjectTagView(LoginRequiredMixin, TemplateView):
    template_name = "project_tag.html"

class ProjectDetailView(LoginRequiredMixin, TemplateView):
    template_name = "project_detail.html"

# Authentication views
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('birds:project-list-view')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request):
    return HttpResponse("Your username is %s." % request.user.username)

# Rest API views
class IdentificationList(LoginRequiredMixin, generics.ListCreateAPIView):
    model = Identification
    raise_exception = True
    serializer_class = IdentificationSerializer
    # permission_classes = [CanCRUDMeal]

    def perform_create(self, serializer):
        """Force identification.user to the current user on save"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        project = get_object_or_404(Project, directory=self.kwargs['project_dir'])
        return Identification.objects.filter(record__in=project.records.all())

        # """Filter instances in list based on user rights"""
        # user = self.request.user
        # if user.is_staff:
        #     return Meal.objects.all()
        # elif user.is_manager:
        #     return Meal.objects.filter(user__is_staff=False)
        # return Meal.objects.filter(user__id=user.id)
    

class UserMixin(object):
    """Common configuration for ProjectList and ProjectDetail"""
    model = User
    raise_exception = True
    serializer_class = UserSerializer
    # permission_classes = [CanCRUDMeal]

    # def perform_create(self, serializer):
    #     """Force meal.user to the current user on save"""
    #     serializer.save(user=self.request.user)

    def get_queryset(self):
        return User.objects.all()

        # """Filter instances in list based on user rights"""
        # user = self.request.user
        # if user.is_staff:
        #     return Meal.objects.all()
        # elif user.is_manager:
        #     return Meal.objects.filter(user__is_staff=False)
        # return Meal.objects.filter(user__id=user.id)

class UserList(UserMixin, generics.ListCreateAPIView):    #LoginRequiredMixin, 
    pass

class UserDetail(UserMixin, generics.RetrieveUpdateDestroyAPIView):   #LoginRequiredMixin, 
    pass


class RightMixin(object):
    model = Right
    raise_exception = True
    serializer_class = RightSerializer
    permission_classes = [IsRightOwner]

    def get_queryset(self):
        user = self.request.user
        projects_with_owner_rights = Right.objects.filter(user=self.request.user, role=0).values_list('project', flat=True)
        return Right.objects.filter(project_id__in=projects_with_owner_rights)

class RightList(LoginRequiredMixin, RightMixin, generics.ListCreateAPIView):
    pass

class RightDetail(LoginRequiredMixin, RightMixin, generics.RetrieveUpdateDestroyAPIView):
    pass


class RecordTagList(LoginRequiredMixin, generics.ListAPIView):
    model = Tag
    raise_exception = True
    serializer_class = TagSerializer
    permission_classes = [HasProjectRight]

    def get_queryset(self):
        project = get_object_or_404(Project, directory=self.kwargs['project_dir'])
        record = get_object_or_404(Record, pk=self.kwargs['record_id'])
        record_weights = record.weights.all()
        weight_values = record_weights.values_list('value', flat=True)
        tags_with_weights = Tag.objects.filter(weights__in=record_weights)
        tags_without_weights = list(Tag.objects.filter(project=project).exclude(id__in=tags_with_weights).order_by('-prior'))
        tags_with_weights = [t for _,t in sorted(zip(weight_values, tags_with_weights), reverse=True)]
        all_tags = tags_with_weights + tags_without_weights
        return all_tags

    # def get_tags(self, obj):
    #     return TagSerializer(Tag.objects.filter(weights__in=obj.weights.all()), many=True).data
    #     tags_with_weights = [weight.tag for weight in obj.weights.all()]
    #     tags_without_weights = list(Tag.objects.filter(project=obj.project).exclude(id__in=[tag.id for tag in tags_with_weights]))
    #     all_tags = tags_with_weights + tags_without_weights
    #     return TagSerializer(all_tags, many=True).data

class RecordRandom(LoginRequiredMixin, generics.RetrieveAPIView):
    model = Record
    raise_exception = True
    serializer_class = RecordSerializer
    permission_classes = [HasProjectRight]

    def get_object(self):
        project = get_object_or_404(Project, directory=self.kwargs['project_dir'])
        records = Record.objects.filter(project__directory=project.directory, file_on_server=True)
        if len(records) == 0:
            raise Exception("There is no record in " + project.name + " project.")
        probabilities = records.values_list('importance', flat=True)
        random_record = random.choices(records, weights=probabilities)[0]
        return random_record

    # def get_queryset(self):
    #     project = self.kwargs['project_dir']
    #     user = self.request.user
    #     projects_with_owner_rights = Right.objects.filter(user=self.request.user, role=0).values_list('project', flat=True)
    #     return Right.objects.filter(project_id__in=projects_with_owner_rights)

        # year = self.kwargs['year']

        # random_record = None
        # all_tags = None
        # message = None
        # project = Project.objects.filter(directory=project_dir)
        # if len(project) == 0:
        #     context = { 'message': "There is no project in " + project_dir + " directory." }
        #     return render(request, 'index.html', context)
        
        # project = project[0]
        # records = Record.objects.filter(project__directory=project_dir, file_on_server=True)
        # if len(records) == 0:
        #     context = { 'message': "There is no record in " + project.name + " project." }
        #     return render(request, 'index.html', context)
        
        # probabilities = records.values_list('importance', flat=True)
        # random_record = random.choices(records, weights=probabilities)[0]
        # tags_with_weights = [weight.tag for weight in random_record.weights.all()]
        # tags_without_weights = list(Tag.objects.filter(project=project).exclude(id__in=[tag.id for tag in tags_with_weights]))
        # all_tags = tags_with_weights + tags_without_weights
        # if len(all_tags) == 0:
        #     context = { 'message': "There is no tag in " + project.name + " project." }
        # else:
        #     context = {
        #         'project': project,
        #         'random_record': random_record,
        #         'tags': all_tags,
        #     }
        # return render(request, 'index.html', context)




class ProjectList(generics.ListAPIView):
    model = Project
    raise_exception = True
    serializer_class = BasicProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


class ProjectMixin(object):
    """Common configuration for ProjectList and ProjectDetail"""
    model = Project
    lookup_field = 'directory'
    raise_exception = True
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwner]

    def get_queryset(self):
        return Project.objects.all()

class ProjectDetail(LoginRequiredMixin, ProjectMixin, generics.RetrieveUpdateDestroyAPIView):
    pass


