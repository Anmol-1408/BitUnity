from django import forms
from .models import Project, Comment, UserProfile

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'institute', 'university', 'project_url']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))

    class Meta:
        model = Comment
        fields = ['comment']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'project_url']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'birth_date', 'location', 'picture']