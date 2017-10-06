from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text','priority','description']
        labels = {'text': 'Topic',
                  'priority':'Priority',
                  'decription':'Description'}
 
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title','text', 'importance']
        labels = {
            'title':'title',
            'text':'content',
            'importance':'importance',
        }
        widgets = {'text': forms.Textarea(attrs={'cols':80})}