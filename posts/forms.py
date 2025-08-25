from django import forms
from .models import Post
from departments.models import Department, Course
from accounts.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'target_type', 'department', 'course', 'professor', 'file', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a descriptive title for your post'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 5
            }),
            'target_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'target-type-select',
                'onchange': 'togglePostFields()'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control',
                'id': 'department-select'
            }),
            'course': forms.Select(attrs={
                'class': 'form-control',
                'id': 'course-select'
            }),
            'professor': forms.Select(attrs={
                'class': 'form-control',
                'id': 'professor-select'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.txt'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        
        if user:
            # Hide form for visitors
            if user.role == User.VISITOR:
                for field_name in list(self.fields.keys()):
                    del self.fields[field_name]
                return
                
            # Limit department choices to user's department if they're not a visitor
            if user.role != User.VISITOR and user.department:
                self.fields['department'].queryset = Department.objects.filter(id=user.department.id)
                self.fields['course'].queryset = Course.objects.filter(department=user.department)
                self.fields['professor'].queryset = User.objects.filter(
                    role=User.PROFESSOR, 
                    department=user.department
                )
            else:
                # Show all departments, courses, and professors
                self.fields['department'].queryset = Department.objects.all()
                self.fields['course'].queryset = Course.objects.all()
                self.fields['professor'].queryset = User.objects.filter(role=User.PROFESSOR)