from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Project, Comment, UserProfile
from .forms import CommentForm, ProjectForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.

@login_required
def projectList(request):
    projects = Project.objects.all().order_by('-created_on')

    context={'project_list':projects}
    return render(request, 'index.html',context)

@login_required
def projectDetail(request, pk):
    project = Project.objects.get(pk=pk)
    comments = Comment.objects.filter(project=project).order_by('-created_on')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.project = project
            new_comment.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = CommentForm()

    context = {
        'project': project,
        'form': form,
        'comments': comments,
    }
    return render(request, 'project_detail.html', context)

@login_required
def projectEdit(request, pk):
    project = Project.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project-detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'project_edit.html', {'form': form})

@login_required
def projectDelete(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('project-list')  # Redirect to project list page after deletion

    return render(request, 'project_delete.html', {'project': project})

@login_required
def commentDelete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':

        comment.delete()

        return redirect('project-detail', pk=comment.project.pk)  # Redirect to project detail page after deletion
    return render(request, 'comment_delete.html', {'comment': comment})

def profile(request, pk, *args, **kwargs):
    try:
        print("Debug: Profile view accessed")
        
        # Retrieve the UserProfile object with the given primary key
        profile = get_object_or_404(UserProfile, pk=pk)
        print("Debug: UserProfile object retrieved successfully")

        # Get the associated User object
        user = profile.user
        print("Debug: User object retrieved successfully")

        # Get the posts associated with the user
        projects = Project.objects.filter(author=user).order_by('-created_on')
        print("Debug: Posts retrieved successfully")

        context = {
            'user': user,
            'profile': profile,
            'projects': projects
        }

        # Render the profile.html template with the context data
        return render(request, 'profile.html', context)

    except Exception as e:
        # Log any exceptions that occur during view execution
        print("Error occurred:", e)
