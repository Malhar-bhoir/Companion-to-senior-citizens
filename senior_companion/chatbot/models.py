from django.db import models
from django.conf import settings

class LogicRule(models.Model):
    """
    Represents a rule in our logic system.
    IF user input matches 'pattern' -> THEN respond with 'response'.
    """
    MATCH_CHOICES = [
        ('contains', 'Contains Keyword'),
        ('exact', 'Exact Match'),
        ('regex', 'Regular Expression (Advanced)'),
    ]
    
    # The "If" part
    pattern = models.CharField(max_length=255, help_text="The keyword or phrase to look for (e.g., 'register', 'password')")
    match_type = models.CharField(max_length=20, choices=MATCH_CHOICES, default='contains')
    
    # The "Then" part
    response = models.TextField(help_text="The answer to give.")
    
    # Optional: Guide the user to a page
    suggested_link = models.CharField(max_length=200, blank=True, null=True, help_text="Optional: URL path to redirect user (e.g., '/accounts/login/')")
    
    priority = models.IntegerField(default=1, help_text="Higher numbers are checked first.")

    def __str__(self):
        return f"Rule: {self.pattern} -> {self.response[:30]}..."

class UnansweredQuery(models.Model):
    """
    Stores queries that the bot could not understand.
    Admins can review these to improve the rules.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    query_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Unanswered: {self.query_text[:50]}..."