from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    return render(request, 'topics/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-cre_date')
    context = {
        'topics': topics,
    }
    return render(request, 'topics/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-cre_date')
    context = {
        'topic': topic,
        'entries': entries,
    }
    return render(request, 'topics/topic.html', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
        print('new_topic:GET')
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics:topics'))
    context = {
        'form': form,
    }

    return render(request, 'topics/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topics:topic', args=[topic.id]))
    context = {
        'form': form,
        'topic': topic
    }

    return render(request, 'topics/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics:topic', args=[topic.id]))
    context = {
        'form': form,
        'entry': entry,
        'topic': topic,
    }

    return render(request, 'topics/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    entry.delete()
    return HttpResponseRedirect(reverse('topics:topic', args=[topic.id]))