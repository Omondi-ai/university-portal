from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Application
from departments.models import Department

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'department', 'profile_picture', 'student_id', 'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'role': forms.Select(attrs={'class': 'form-control', 'id': 'role-select'}),
            'department': forms.Select(attrs={'class': 'form-control', 'id': 'department-select'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID (if applicable)'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set up department choices - all departments for professors, only some for students?
        self.fields['department'].queryset = Department.objects.all()
        self.fields['department'].required = False
        
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in ['profile_picture']:
                field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'
        
        # Special handling for profile picture
        self.fields['profile_picture'].widget.attrs['class'] = 'form-control'

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture', 'phone_number', 'department']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove department field for visitors
        if self.instance.role == User.VISITOR:
            del self.fields['department']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'email', 'phone_number', 'intended_department', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number'}),
            'intended_department': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Why do you want to join this department?', 'rows': 4}),
        }