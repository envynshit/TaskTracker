from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Task, Reminder
from .forms import TaskForm, ReminderForm
from django.db.models import Q


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
    selected_id = request.GET.get('task')

    base_qs = Task.objects.filter(owner=request.user)

    search_query = request.GET.get('q', '').strip()
    sort_option = request.GET.get('sort', '')

    # Apply filtering based on the 'filter' parameter
    if flt == 'all':
        tasks = base_qs
    elif flt == 'today':
        tasks = base_qs.filter(due_date__date=today)
    elif flt == 'week':
        tasks = base_qs.filter(
            due_date__gte=today,
            due_date__lte=today + timezone.timedelta(days=7),
        )
    elif flt == 'completed':
        tasks = base_qs.filter(status='done')
    elif flt == 'overdue':
        tasks = base_qs.filter(
            status__in=['todo', 'in_progress'],
            due_date__lt=today,
        )
    else:
        tasks = base_qs.none()

    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    allowed_sorts = ['due_date', '-due_date', 'title', '-title']
    if sort_option in allowed_sorts:
        tasks = tasks.order_by(sort_option)

    selected_task = None
    if selected_id:
        selected_task = get_object_or_404(base_qs, pk=selected_id)

    reminders = Reminder.objects.filter(
        task__owner=request.user,
        remind_at__gte=timezone.now(),
    ).order_by('remind_at')

    

    return render(request, 'core/dashboard.html', {
        'tasks': tasks,
        'filter': flt,
        'reminders': reminders,
        'selected_task': selected_task,
        'search_query': search_query,
        'sort_option': sort_option,
    })


@login_required
def reminder_create(request, selected_task_pk):
    selected_task = get_object_or_404(Task, pk=selected_task_pk, owner=request.user)
    if request.method == "POST":
        form = ReminderForm(request.POST, user=request.user, )
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