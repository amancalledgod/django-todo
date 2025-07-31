from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Task
from .forms import RegisterForm

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    total = tasks.count()
    completed = tasks.filter(complete=True).count()
    progress = int((completed / total) * 100) if total > 0 else 0

    context = {
        'tasks': tasks,
        'progress': progress,
        'completed': completed,
        'total': total,
    }
    return render(request, 'todo/task_list.html', context)


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority', 'M')
        if title:
            Task.objects.create(
                title=title,
                priority=priority,
                user=request.user
            )
        return redirect('task_list')


@login_required
def toggle_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.complete = not task.complete
    task.save()
    return redirect('task_list')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.due_date = request.POST.get('due_date') or None
        task.priority = request.POST.get('priority') or 'M'
        task.save()
        return redirect('task_list')
    return render(request, 'todo/edit_task.html', {'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'todo/delete_task.html', {'task': task})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = RegisterForm()
    return render(request, 'todo/register.html', {'form': form})
