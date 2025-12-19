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
    flt = request.GET.get('filter', 'today')

    base_qs = Task.objects.filter(owner=request.user)

    if flt == 'today':
        tasks = base_qs.filter(due_date=today)
    elif flt == 'week':
        tasks = base_qs.filter(
            due_date__gte=today,
            due_date__lte=today + timezone.timedelta(days=7),
        )
    elif flt == 'upcoming':
        tasks = base_qs.filter(due_date__gt=today)
    elif flt == 'completed':
        tasks = base_qs.filter(status='done')
    elif flt == 'overdue':
        tasks = base_qs.filter(
            status__in=['todo', 'in_progress'],
            due_date__lt=today,
        )
    else:
        tasks = base_qs.none()

    reminders = Reminder.objects.filter(
        task__owner=request.user,
        remind_at__gte=timezone.now(),
    ).order_by('remind_at')

    return render(request, 'core/dashboard.html', {
        'tasks': tasks,
        'filter': flt,
        'reminders': reminders,
    })


@login_required
def reminder_create(request):
    if request.method == "POST":
        form = ReminderForm(request.POST, user=request.user)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.save()
            return redirect('dashboard')
    else:
        form = ReminderForm(user=request.user)
    return render(request, 'core/reminder_form.html', {'form': form})

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
    return render(request, 'core/update_form.html', {'form': form})






