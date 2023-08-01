from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'permissions': FilteredSelectMultiple("Permission", False, attrs={'rows':'2'}),
        }

class UserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
            queryset=Group.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','groups','is_active')

