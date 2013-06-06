from django.db import models
from datetime import datetime

class Comment(models.Model):
    text = models.TextField()
    ts = models.DateField(auto_now_add = True, default = datetime.now())    
    user = models.CharField(max_length = 256, default = 'anon')    

class Idea(models.Model):
    title = models.TextField(null = False)
    text = models.TextField(null = False)
    upvotes = models.IntegerField(default = 0)
    ts = models.DateField(auto_now = True, default = datetime.now())
    repo = models.URLField(default = '')
    user = models.CharField(max_length = 256, default = 'anon')   
    comments = models.ManyToManyField(Comment, blank=True)
    tags = models.TextField(blank=True)
    
    def tagsplit(self):
        return self.tags.split('<sep>')
    
    def get_suggestions(self):
        return Suggestion.objects.filter(idea=self)
    
    def __json__(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'upvotes': self.upvotes,
            'ts': self.ts.isoformat(),
            'repo': self.repo,
            'user': self.user,
            'tags': self.tags.split('<sep>'),
        }

class Suggestion(models.Model):
    idea = models.ForeignKey(Idea)
    upvotes = models.IntegerField(default = 0)    
    text = models.TextField(null = False)
    ts = models.DateField(auto_now = True, default = datetime.now())    
    user = models.CharField(max_length = 256, default = 'anon')
    comments = models.ManyToManyField(Comment, blank=True)
    
    def get_comments(self):
        return []

