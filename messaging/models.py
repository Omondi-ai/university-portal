from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()

class Thread(models.Model):
    participants = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated']
    
    def __str__(self):
        # Show participant names instead of "Thread object"
        participant_names = ", ".join([user.username for user in self.participants.all()])
        return f"Conversation with {participant_names}"
    
    def get_other_participant(self, user):
        """Get the other participant in the thread"""
        return self.participants.exclude(id=user.id).first()

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    attachment = models.FileField(
        upload_to='message_attachments/',
        null=True,
        blank=True,
        max_length=500,  # Increased for longer filenames
        validators=[
            FileExtensionValidator(allowed_extensions=[
                'jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'
            ])
        ]
    )
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created']
    
    def __str__(self):
        # Show a meaningful preview instead of "Message object"
        preview = self.text[:50] + "..." if self.text and len(self.text) > 50 else (self.text or "[Attachment]")
        return f"{self.sender.username}: {preview}"
    
    def is_image(self):
        if self.attachment:
            return self.attachment.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        return False
    
    def get_preview(self):
        """Get a shortened preview of the message"""
        if self.text:
            return self.text[:75] + "..." if len(self.text) > 75 else self.text
        elif self.attachment:
            return f"📎 {self.attachment.name}"
        return "[No content]"