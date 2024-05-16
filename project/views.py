from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Project, Comment, UserProfile, Star
from .forms import NewProjectForm, CommentForm, ProjectForm, UserProfileForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib import messages


# Create your views here.

@login_required
def projectList(request):
    projects = Project.objects.all().order_by('-created_on')

    context={'project_list':projects}
    return render(request, 'index.html',context)
    
@login_required
def createProject(request):
    if request.method == 'POST':
        # If the form is submitted, process the data
        form = NewProjectForm(request.POST)
        if form.is_valid():
            # Save the form data to create a new project
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            # Redirect to the project detail page after creation
            return redirect('project-detail', pk=project.pk)
    else:
        # If the request is GET, render the form
        form = NewProjectForm()
    return render(request, 'create_project.html', {'form': form})

@login_required
def projectDetail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    comments = Comment.objects.filter(project=project).order_by('-created_on')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                new_comment = form.save(commit=False)
                new_comment.author = request.user
                new_comment.project = project
                new_comment.save()
                messages.success(request, 'Comment added successfully.')
                return redirect('project_detail', pk=project.pk)
            except Exception as e:
                messages.error(request, f'Error saving comment: {e}')
        else:
            messages.error(request, 'Invalid form data. Please check the form.')
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

        followers = profile.followers.all()
        if len(followers) == 0:
            is_following = False
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False
        numbers_of_followers = len(followers)

        context = {
            'user': user,
            'profile': profile,
            'projects': projects,
            'numbers_of_followers':numbers_of_followers,
            'is_following':is_following,
        }

        # Render the profile.html template with the context data
        return render(request, 'profile.html', context)

    except Exception as e:
        # Log any exceptions that occur during view execution
        print("Error occurred:", e)

@login_required
def profileEdit(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=profile.pk)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form, 'profile': profile})

@login_required
def addFollower(request, pk, *args, **kwargs):
    try:
        print("Debug: addFollower view accessed")
        
        # Retrieve the UserProfile object with the given primary key
        profile = get_object_or_404(UserProfile, pk=pk)
        print("Debug: UserProfile object retrieved successfully")

        # Add the current user as a follower to the profile
        profile.followers.add(request.user)
        print("Debug: User added as follower successfully")

        # Redirect to the profile page after adding the follower
        return redirect('profile', pk=profile.pk)

    except Exception as e:
        # Log any exceptions that occur during view execution
        print("Error occurred:", e)

@login_required
def removeFollower(request, pk, *args, **kwargs):
    try:
        print("Debug: removeFollower view accessed")
        
        # Retrieve the UserProfile object with the given primary key
        profile = get_object_or_404(UserProfile, pk=pk)
        print("Debug: UserProfile object retrieved successfully")

        # Remove the current user from the followers of the profile
        profile.followers.remove(request.user)
        print("Debug: User removed from followers successfully")

        # Redirect to the profile page after removing the follower
        return redirect('profile', pk=profile.pk)

    except Exception as e:
        # Log any exceptions that occur during view execution
        print("Error occurred:", e)

@login_required
def addLike(request, pk):
    try:
        print("Debug: addLike view accessed")

        # Retrieve the project object with the given primary key
        project = get_object_or_404(Project, pk=pk)
        print("Debug: Project object retrieved successfully")

        is_like = False
        for like in project.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            project.likes.add(request.user)
            print("Debug: User added as like to project successfully")
        else:
            project.likes.remove(request.user)
            print("Debug: User removed as like from project successfully")

        # Redirect to the project detail page after handling the like action
        return redirect('project-detail', pk=pk)

    except Exception as e:
        # Log any exceptions that occur during view execution
        print("Error occurred:", e)

def search(request):
    try:
        print("Debug: search view accessed")
        
        # Retrieve the query parameter from the request
        query = request.GET.get('query', '')
        print("Debug: Query:", query)

        # Check if the query length exceeds 78 characters
        if len(query) > 78:
            allProjects = Project.objects.none()
        else:
            # Filter projects by various fields containing the query
            allProjectName = Project.objects.filter(project_name__icontains=query)
            allProjectAuthor = Project.objects.filter(author__username__icontains=query)
            allProjectDescription = Project.objects.filter(project_description__icontains=query)
            allProjectInstitute = Project.objects.filter(institute__icontains=query)
            allProjectUniversity = Project.objects.filter(university__icontains=query)
            
            # Union all filtered querysets to get the final queryset
            allProjects = allProjectName.union(allProjectDescription, allProjectAuthor, allProjectInstitute, allProjectUniversity)
            print("Debug: Projects filtered successfully")

        # Check if any projects were found
        if allProjects.count() == 0:
            messages.warning(request, "No search results found. Please refine your query.")
        
        # Prepare parameters for rendering the template
        params = {'allProjects': allProjects, 'query': query}
        
        # Render the search.html template with the filtered projects and query
        return render(request, 'search.html', params)

    except Exception as e:
        # Log any exceptions that occur during view execution
        print("Error occurred:", e)

@login_required
def save_memory(request, pk):
    project = get_object_or_404(Project, pk=pk)
    memory, created = Memory.objects.get_or_create(user=request.user, project=project)
    if created:
        messages.success(request, 'Project saved as memory.')
    else:
        messages.warning(request, 'Project is already saved as memory.')
    return redirect('project-detail', pk=pk)

@login_required
def unsave_memory(request, pk):
    project = get_object_or_404(Project, pk=pk)
    try:
        memory = Memory.objects.get(user=request.user, project=project)
        memory.delete()
        messages.success(request, 'Project removed from memories.')
    except Memory.DoesNotExist:
        messages.warning(request, 'Project was not saved as memory.')
    return redirect('project-detail', pk=pk)