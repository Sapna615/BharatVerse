from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CulturalJourney, JourneyItem

@login_required
def my_journey(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            CulturalJourney.objects.create(user=request.user, title=title)
            messages.success(request, 'Journey created successfully.')
        return redirect('my_journey')
        
    journeys = CulturalJourney.objects.filter(user=request.user).order_by('-created_at')
    active_journey = journeys.first() if journeys.exists() else None
    items = JourneyItem.objects.filter(journey=active_journey).order_by('order') if active_journey else []
    
    # calc progress dynamically
    progress = 0
    if items:
        completed = items.filter(completed=True).count()
        progress = int((completed / items.count()) * 100)
    
    return render(request, 'journeys/my_journey.html', {
        'journeys': journeys,
        'active_journey': active_journey,
        'items': items,
        'progress': progress
    })

@login_required
def toggle_journey_item(request, item_id):
    item = get_object_or_404(JourneyItem, id=item_id, journey__user=request.user)
    item.completed = not item.completed
    item.save()
    
    if item.completed:
        request.user.xp += 10
        request.user.save()
        messages.success(request, 'Item marked complete! +10 XP')
    return redirect('my_journey')
