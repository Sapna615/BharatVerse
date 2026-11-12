from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Submission
from culture.models import State, CulturalStory, CulturalCategory
from gamification.services import award_xp

def is_curator(user):
    return user.is_authenticated and user.role == 'curator'

def is_contributor_or_curator(user):
    return user.is_authenticated and user.role in ['contributor', 'curator']

@login_required(login_url='/accounts/login/')
def contribute(request):
    states = State.objects.all().order_by('name')
    if request.method == 'POST':
        submission_type = request.POST.get('submission_type')
        title = request.POST.get('title')
        state = request.POST.get('state')
        content = request.POST.get('content')
        source_note = request.POST.get('source_note', '')
        consent_given = request.POST.get('consent_given') == 'on'
        
        if not consent_given:
            messages.error(request, 'You must provide consent to submit.')
            return redirect('contribute')
            
        sub = Submission.objects.create(
            contributor=request.user,
            submission_type=submission_type,
            title=title,
            state=state,
            content=content,
            source_note=source_note,
            consent_given=True,
            moderation_status='pending'
        )
        
        if 'image' in request.FILES:
            sub.image = request.FILES['image']
            sub.save()
            
        return redirect('submission_success', sub.id)
        
    return render(request, 'contributions/contribute.html', {'states': states})

@login_required(login_url='/accounts/login/')
def submission_success(request, sub_id):
    sub = get_object_or_404(Submission, id=sub_id, contributor=request.user)
    return render(request, 'contributions/success.html', {'sub': sub})

@login_required(login_url='/accounts/login/')
def my_submissions(request):
    subs = Submission.objects.filter(contributor=request.user).order_by('-created_at')
    counts = {
        'total': subs.count(),
        'pending': subs.filter(moderation_status='pending').count(),
        'approved': subs.filter(moderation_status='approved').count(),
        'rejected': subs.filter(moderation_status='rejected').count(),
    }
    return render(request, 'contributions/dashboard.html', {'subs': subs, 'counts': counts})

@login_required(login_url='/accounts/login/')
def submission_detail(request, sub_id):
    sub = get_object_or_404(Submission, id=sub_id, contributor=request.user)
    
    if request.method == 'POST' and sub.moderation_status == 'rejected':
        # Resubmit
        sub.title = request.POST.get('title', sub.title)
        sub.content = request.POST.get('content', sub.content)
        sub.source_note = request.POST.get('source_note', sub.source_note)
        sub.moderation_status = 'pending'
        sub.save()
        messages.success(request, 'Submission updated and resubmitted for review.')
        return redirect('my_submissions')
        
    return render(request, 'contributions/detail.html', {'sub': sub})

# ---------------- CURATOR VIEWS ----------------

@user_passes_test(is_curator)
def curator_dashboard(request):
    status_filter = request.GET.get('status', 'pending')
    q = request.GET.get('q', '')
    
    subs = Submission.objects.all().order_by('-created_at')
    if status_filter:
        subs = subs.filter(moderation_status=status_filter)
    if q:
        subs = subs.filter(title__icontains=q)
        
    counts = {
        'pending': Submission.objects.filter(moderation_status='pending').count(),
        'approved': Submission.objects.filter(moderation_status='approved').count(),
        'rejected': Submission.objects.filter(moderation_status='rejected').count(),
        'total': Submission.objects.count()
    }
        
    return render(request, 'contributions/curator_dashboard.html', {
        'subs': subs, 'counts': counts, 'status_filter': status_filter, 'q': q
    })

@user_passes_test(is_curator)
def curator_review(request, sub_id):
    sub = get_object_or_404(Submission, id=sub_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        comment = request.POST.get('review_comment', '')
        
        sub.reviewer = request.user
        sub.reviewed_at = timezone.now()
        sub.review_comment = comment
        
        if action == 'approve':
            sub.moderation_status = 'approved'
            sub.save()
            
            # Create CulturalStory (simplified mapping)
            cat, _ = CulturalCategory.objects.get_or_create(name='Story', defaults={'description': 'Community Stories'})
            state_obj = State.objects.filter(name__icontains=sub.state).first()
            if not state_obj:
                state_obj = State.objects.first()
            
            CulturalStory.objects.create(
                title=sub.title,
                slug=f"{sub.title.lower().replace(' ', '-')}-{sub.id}",
                content=sub.content,
                author=sub.contributor,
                state=state_obj,
                category=cat,
                moderation_status='approved'
            )
            
            award_xp(sub.contributor, 100, f'Contribution Approved: {sub.title}', 'contribution', sub.id)
            messages.success(request, f'Submission {sub.id} approved and published.')
            
        elif action == 'reject':
            if not comment:
                messages.error(request, 'Review comment is required for rejection.')
                return redirect('curator_review', sub_id)
            sub.moderation_status = 'rejected'
            sub.save()
            messages.info(request, f'Submission {sub.id} rejected and returned to contributor.')
            
        return redirect('curator_dashboard')
        
    return render(request, 'contributions/curator_review.html', {'sub': sub})
