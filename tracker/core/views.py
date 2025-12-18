from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Task, Reminder
from .forms import TaskForm, ReminderForm


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def dashboard(request):
    today = timezone.now().date()
    task_today = Task.objects.filter(owner=request.user, due_date=today)
    tasks_week = Task.objects.filter(
        owner=request.user,
        due_date__gte=today,
        due_date__lte=today + timezone.timedelta(days=7)
    )
    tasks_completed = Task.objects.filter(owner=request.user, status='done')

    return render(request, 'core/dashboard.html', {
        'tasks_today': task_today,
        'tasks_week': tasks_week,
        'tasks_completed': tasks_completed,
    })

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'core/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'core/task_form.html', {'form': form})

@login_required
def reminder_create(request):
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.task.owner = request.user
            reminder.save()
            return redirect('dashboard')
    else:
        form = ReminderForm()
    return render(request, 'core/reminder_form.html', {'form': form})




