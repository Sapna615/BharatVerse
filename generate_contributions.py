import os

BASE_DIR = '/Users/sapnarai/BharatVerse'
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

contributions_views = """from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Submission
from culture.models import State, CulturalStory, CulturalCategory
from gamification.services import award_xp

def is_curator(user):
    return user.is_authenticated and user.role == 'curator'

@login_required
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

@login_required
def submission_success(request, sub_id):
    sub = get_object_or_404(Submission, id=sub_id, contributor=request.user)
    return render(request, 'contributions/success.html', {'sub': sub})

@login_required
def my_submissions(request):
    subs = Submission.objects.filter(contributor=request.user).order_by('-created_at')
    counts = {
        'total': subs.count(),
        'pending': subs.filter(moderation_status='pending').count(),
        'approved': subs.filter(moderation_status='approved').count(),
        'rejected': subs.filter(moderation_status='rejected').count(),
    }
    return render(request, 'contributions/dashboard.html', {'subs': subs, 'counts': counts})

@login_required
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
            
            CulturalStory.objects.create(
                entry=None, # if we had a specific entry mapping
                title=sub.title,
                content=sub.content,
                contributor=sub.contributor,
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
"""

with open(os.path.join(BASE_DIR, 'contributions', 'views.py'), 'w') as f:
    f.write(contributions_views)

contributions_urls = """from django.urls import path
from . import views

urlpatterns = [
    # Contributor
    path('', views.contribute, name='contribute'),
    path('success/<int:sub_id>/', views.submission_success, name='submission_success'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
    path('submissions/<int:sub_id>/', views.submission_detail, name='submission_detail'),
    
    # Curator
    path('curator/', views.curator_dashboard, name='curator_dashboard'),
    path('curator/submissions/<int:sub_id>/', views.curator_review, name='curator_review'),
]
"""

with open(os.path.join(BASE_DIR, 'contributions', 'urls.py'), 'w') as f:
    f.write(contributions_urls)

with open(os.path.join(BASE_DIR, 'bharatverse', 'urls.py'), 'r') as f:
    bv_urls = f.read()
if "'contributions.urls'" not in bv_urls:
    bv_urls = bv_urls.replace(
        "path('gamification/', include('gamification.urls')),",
        "path('gamification/', include('gamification.urls')),\n    path('contribute/', include('contributions.urls')),"
    )
    with open(os.path.join(BASE_DIR, 'bharatverse', 'urls.py'), 'w') as f:
        f.write(bv_urls)

templates = {
    'contributions/contribute.html': """{% extends 'base.html' %}
{% block title %}Preserve a Tradition - BharatVerse{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-16 text-center">
    <h1 class="text-4xl md:text-5xl font-serif font-bold text-white mb-4">Preserve a Tradition</h1>
    <p class="text-xl text-gray-300 font-light max-w-3xl mx-auto">Every family has a story. Every community has a tradition. Help preserve yours.</p>
</div>
<div class="max-w-4xl mx-auto px-4 py-16">
    <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-8">
        <p class="text-sm text-blue-800">
            <strong>Privacy Notice:</strong> Do not submit private family information, sensitive personal data, or information belonging to another person without permission. Your submission will be reviewed by a curator before being published.
        </p>
    </div>
    
    <form method="POST" action="{% url 'contribute' %}" enctype="multipart/form-data" class="bg-white rounded-xl shadow-lg border border-gray-100 p-8 space-y-6">
        {% csrf_token %}
        <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">Title</label>
            <input type="text" name="title" required class="w-full border-gray-300 rounded-md focus:ring-bharat-saffron focus:border-bharat-saffron" placeholder="A Traditional Harvest Celebration in My Village">
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <label class="block text-sm font-bold text-gray-700 mb-1">Category</label>
                <select name="submission_type" required class="w-full border-gray-300 rounded-md focus:ring-bharat-saffron focus:border-bharat-saffron">
                    <option value="tradition">Tradition</option>
                    <option value="story">Cultural Story</option>
                    <option value="festival">Festival</option>
                    <option value="cuisine">Cuisine</option>
                    <option value="folk_art">Folk Art</option>
                    <option value="craft">Craft</option>
                    <option value="other">Other</option>
                </select>
            </div>
            <div>
                <label class="block text-sm font-bold text-gray-700 mb-1">State</label>
                <select name="state" required class="w-full border-gray-300 rounded-md focus:ring-bharat-saffron focus:border-bharat-saffron">
                    <option value="">Select State</option>
                    {% for s in states %}
                    <option value="{{ s.name }}">{{ s.name }}</option>
                    {% endfor %}
                </select>
            </div>
        </div>
        
        <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">The Story / Description</label>
            <textarea name="content" required rows="6" class="w-full border-gray-300 rounded-md focus:ring-bharat-saffron focus:border-bharat-saffron" placeholder="What is this cultural practice? Tell the story behind it..."></textarea>
        </div>
        
        <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">Source / Reference Note (Optional)</label>
            <input type="text" name="source_note" class="w-full border-gray-300 rounded-md focus:ring-bharat-saffron focus:border-bharat-saffron" placeholder="e.g. Learned from my grandmother">
        </div>
        
        <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">Upload Image (Optional)</label>
            <input type="file" name="image" accept="image/*" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-bold file:bg-gray-100 file:text-bharat-navy hover:file:bg-gray-200">
        </div>
        
        <div class="flex items-start">
            <div class="flex items-center h-5">
                <input id="consent" name="consent_given" type="checkbox" required class="focus:ring-bharat-saffron h-4 w-4 text-bharat-saffron border-gray-300 rounded">
            </div>
            <div class="ml-3 text-sm">
                <label for="consent" class="font-medium text-gray-700">Contributor Consent</label>
                <p class="text-gray-500">I confirm that I have permission to submit this content and that it does not intentionally contain private or sensitive personal information.</p>
            </div>
        </div>
        
        <div class="pt-6 border-t border-gray-100">
            <button type="submit" class="w-full bg-bharat-saffron text-white font-bold py-4 rounded-xl shadow hover:bg-orange-600 transition text-lg">Submit for Review</button>
        </div>
    </form>
</div>
{% endblock %}""",

    'contributions/success.html': """{% extends 'base.html' %}
{% block title %}Submission Received{% endblock %}
{% block content %}
<div class="max-w-2xl mx-auto px-4 py-20 text-center">
    <div class="w-20 h-20 mx-auto bg-green-100 rounded-full flex items-center justify-center mb-6">
        <svg class="w-10 h-10 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
    </div>
    <h1 class="text-4xl font-serif font-bold text-bharat-navy mb-4">Your story is now in review.</h1>
    <p class="text-gray-600 mb-8">Thank you for helping preserve India's cultural memory. A BharatVerse curator will review your contribution before it becomes publicly visible.</p>
    
    <div class="bg-gray-50 p-6 rounded-xl border border-gray-200 text-left mb-8 space-y-3">
        <div class="flex justify-between border-b border-gray-200 pb-2">
            <span class="text-gray-500 text-sm font-bold">Submission ID</span>
            <span class="text-bharat-navy font-mono font-bold">BV-SUB-{{ sub.id|stringformat:"06d" }}</span>
        </div>
        <div class="flex justify-between border-b border-gray-200 pb-2">
            <span class="text-gray-500 text-sm font-bold">Title</span>
            <span class="text-bharat-navy font-bold">{{ sub.title }}</span>
        </div>
        <div class="flex justify-between border-b border-gray-200 pb-2">
            <span class="text-gray-500 text-sm font-bold">Status</span>
            <span class="text-blue-600 font-bold bg-blue-100 px-2 py-0.5 rounded text-xs uppercase">{{ sub.get_moderation_status_display }}</span>
        </div>
    </div>
    
    <a href="{% url 'my_submissions' %}" class="bg-bharat-navy text-white font-bold py-3 px-8 rounded-full shadow hover:bg-gray-800 transition inline-block">View My Contributions</a>
</div>
{% endblock %}""",

    'contributions/dashboard.html': """{% extends 'base.html' %}
{% block title %}My Contributions{% endblock %}
{% block content %}
<div class="bg-bharat-navy py-12 text-center">
    <h1 class="text-4xl font-serif font-bold text-white mb-2">My Contributions</h1>
    <p class="text-gray-300 font-light">Your submitted cultural stories and traditions.</p>
</div>
<div class="max-w-6xl mx-auto px-4 py-16">
    <!-- Summary -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 text-center">
            <div class="text-3xl font-black text-bharat-navy">{{ counts.total }}</div>
            <div class="text-xs text-gray-500 uppercase font-bold mt-1">Total</div>
        </div>
        <div class="bg-white p-6 rounded-xl shadow-sm border border-blue-200 text-center">
            <div class="text-3xl font-black text-blue-600">{{ counts.pending }}</div>
            <div class="text-xs text-blue-500 uppercase font-bold mt-1">Pending</div>
        </div>
        <div class="bg-white p-6 rounded-xl shadow-sm border border-green-200 text-center">
            <div class="text-3xl font-black text-green-600">{{ counts.approved }}</div>
            <div class="text-xs text-green-500 uppercase font-bold mt-1">Approved</div>
        </div>
        <div class="bg-white p-6 rounded-xl shadow-sm border border-red-200 text-center">
            <div class="text-3xl font-black text-red-600">{{ counts.rejected }}</div>
            <div class="text-xs text-red-500 uppercase font-bold mt-1">Rejected</div>
        </div>
    </div>

    <!-- List -->
    <div class="space-y-4">
        {% for sub in subs %}
        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col md:flex-row justify-between items-center gap-4 hover:border-bharat-saffron transition">
            <div>
                <span class="text-xs font-mono font-bold text-gray-400 block mb-1">BV-SUB-{{ sub.id|stringformat:"06d" }}</span>
                <h3 class="text-lg font-bold text-bharat-navy">{{ sub.title }}</h3>
                <div class="text-sm text-gray-500 flex gap-4 mt-2">
                    <span>{{ sub.get_submission_type_display }}</span>
                    <span>&middot;</span>
                    <span>{{ sub.state }}</span>
                    <span>&middot;</span>
                    <span>{{ sub.created_at|date:"M d, Y" }}</span>
                </div>
            </div>
            <div class="flex items-center gap-4">
                {% if sub.moderation_status == 'pending' %}
                <span class="bg-blue-100 text-blue-700 text-xs font-bold px-3 py-1 rounded uppercase">Pending</span>
                {% elif sub.moderation_status == 'approved' %}
                <span class="bg-green-100 text-green-700 text-xs font-bold px-3 py-1 rounded uppercase">Approved</span>
                {% elif sub.moderation_status == 'rejected' %}
                <span class="bg-red-100 text-red-700 text-xs font-bold px-3 py-1 rounded uppercase">Rejected</span>
                {% else %}
                <span class="bg-gray-100 text-gray-700 text-xs font-bold px-3 py-1 rounded uppercase">{{ sub.get_moderation_status_display }}</span>
                {% endif %}
                
                <a href="{% url 'submission_detail' sub.id %}" class="bg-gray-50 text-bharat-navy font-bold px-4 py-2 rounded border border-gray-200 hover:bg-gray-100">View</a>
            </div>
        </div>
        {% empty %}
        <div class="text-center py-16 bg-gray-50 rounded-xl border border-gray-200">
            <h3 class="text-2xl font-serif text-gray-500 mb-4">You haven't submitted anything yet.</h3>
            <a href="{% url 'contribute' %}" class="bg-bharat-saffron text-white font-bold py-2 px-6 rounded shadow hover:bg-orange-600">Preserve a Tradition</a>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}""",

    'contributions/detail.html': """{% extends 'base.html' %}
{% block title %}Submission Detail{% endblock %}
{% block content %}
<div class="max-w-4xl mx-auto px-4 py-16">
    <a href="{% url 'my_submissions' %}" class="text-bharat-saffron font-bold text-sm mb-6 inline-block">&larr; Back to My Contributions</a>
    
    <div class="bg-white rounded-2xl shadow-lg border border-gray-200 p-8">
        <div class="flex justify-between items-start mb-6 border-b border-gray-100 pb-6">
            <div>
                <span class="text-sm font-mono font-bold text-gray-400 block mb-1">BV-SUB-{{ sub.id|stringformat:"06d" }}</span>
                <h1 class="text-3xl font-serif font-bold text-bharat-navy">{{ sub.title }}</h1>
            </div>
            <div>
                {% if sub.moderation_status == 'pending' %}
                <span class="bg-blue-100 text-blue-700 text-sm font-bold px-4 py-2 rounded uppercase shadow-sm">Pending</span>
                {% elif sub.moderation_status == 'approved' %}
                <span class="bg-green-100 text-green-700 text-sm font-bold px-4 py-2 rounded uppercase shadow-sm">Approved</span>
                {% elif sub.moderation_status == 'rejected' %}
                <span class="bg-red-100 text-red-700 text-sm font-bold px-4 py-2 rounded uppercase shadow-sm">Rejected</span>
                {% endif %}
            </div>
        </div>
        
        {% if sub.moderation_status == 'rejected' %}
        <div class="bg-red-50 border-l-4 border-red-500 p-6 mb-8 rounded-r-lg">
            <h3 class="text-red-800 font-bold mb-2">Curator Feedback</h3>
            <p class="text-red-700">{{ sub.review_comment }}</p>
            <div class="mt-4 text-sm text-red-600 font-bold">You can edit your submission below and resubmit for review.</div>
        </div>
        
        <form method="POST" action="{% url 'submission_detail' sub.id %}" class="space-y-6">
            {% csrf_token %}
            <div>
                <label class="block text-sm font-bold text-gray-700 mb-1">Title</label>
                <input type="text" name="title" value="{{ sub.title }}" required class="w-full border-gray-300 rounded-md">
            </div>
            <div>
                <label class="block text-sm font-bold text-gray-700 mb-1">Content</label>
                <textarea name="content" required rows="8" class="w-full border-gray-300 rounded-md">{{ sub.content }}</textarea>
            </div>
            <button type="submit" class="bg-bharat-navy text-white font-bold py-3 px-8 rounded shadow hover:bg-gray-800 transition">Edit & Resubmit</button>
        </form>
        {% else %}
        <!-- Read Only View -->
        <div class="space-y-6">
            <div class="grid grid-cols-2 gap-4 text-sm bg-gray-50 p-4 rounded-lg">
                <div><span class="font-bold text-gray-500">Type:</span> <span class="text-bharat-navy font-bold">{{ sub.get_submission_type_display }}</span></div>
                <div><span class="font-bold text-gray-500">State:</span> <span class="text-bharat-navy font-bold">{{ sub.state }}</span></div>
                <div><span class="font-bold text-gray-500">Submitted:</span> <span class="text-bharat-navy font-bold">{{ sub.created_at|date:"M d, Y" }}</span></div>
                <div><span class="font-bold text-gray-500">Source:</span> <span class="text-bharat-navy font-bold">{{ sub.source_note|default:"-" }}</span></div>
            </div>
            
            <div class="prose max-w-none text-gray-700 leading-relaxed">
                {{ sub.content|linebreaks }}
            </div>
            
            {% if sub.image %}
            <div class="mt-8">
                <img src="{{ sub.image.url }}" class="rounded-lg shadow max-w-full h-auto">
            </div>
            {% endif %}
            
            {% if sub.moderation_status == 'approved' %}
            <div class="mt-12 bg-green-50 p-6 rounded-lg text-center border border-green-200">
                <h3 class="text-green-800 font-bold mb-2">Published on BharatVerse</h3>
                <p class="text-green-700 text-sm mb-4">Your contribution is now part of the public knowledge base.</p>
                <a href="/search/?q={{ sub.title }}" class="bg-green-600 text-white font-bold py-2 px-6 rounded shadow hover:bg-green-700">Search for it</a>
            </div>
            {% endif %}
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}""",

    'contributions/curator_dashboard.html': """{% extends 'base.html' %}
{% block title %}Curator Dashboard{% endblock %}
{% block content %}
<div class="bg-gray-900 py-12 text-center">
    <h1 class="text-4xl font-serif font-bold text-white mb-2">BharatVerse Curator Console</h1>
    <p class="text-gray-400 font-light">Review, preserve and responsibly publish India's cultural memories.</p>
</div>

<div class="max-w-7xl mx-auto px-4 py-12 flex flex-col md:flex-row gap-8">
    <!-- Sidebar -->
    <div class="w-full md:w-1/4 space-y-6">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 class="font-bold text-gray-800 border-b border-gray-100 pb-3 mb-3">Moderation Queue</h3>
            <ul class="space-y-2">
                <li><a href="?status=pending" class="flex justify-between items-center text-sm font-bold {% if status_filter == 'pending' %}text-blue-600{% else %}text-gray-600 hover:text-gray-900{% endif %}">Pending <span class="bg-blue-100 text-blue-700 py-0.5 px-2 rounded">{{ counts.pending }}</span></a></li>
                <li><a href="?status=approved" class="flex justify-between items-center text-sm font-bold {% if status_filter == 'approved' %}text-green-600{% else %}text-gray-600 hover:text-gray-900{% endif %}">Approved <span class="bg-green-100 text-green-700 py-0.5 px-2 rounded">{{ counts.approved }}</span></a></li>
                <li><a href="?status=rejected" class="flex justify-between items-center text-sm font-bold {% if status_filter == 'rejected' %}text-red-600{% else %}text-gray-600 hover:text-gray-900{% endif %}">Rejected <span class="bg-red-100 text-red-700 py-0.5 px-2 rounded">{{ counts.rejected }}</span></a></li>
            </ul>
        </div>
    </div>
    
    <!-- Main -->
    <div class="w-full md:w-3/4">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="p-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
                <h3 class="font-bold text-gray-800 capitalize">{{ status_filter }} Submissions</h3>
                <form method="GET" class="flex">
                    <input type="hidden" name="status" value="{{ status_filter }}">
                    <input type="text" name="q" value="{{ q }}" placeholder="Search ID or Title..." class="border border-gray-300 rounded-l text-sm p-2 w-64">
                    <button type="submit" class="bg-gray-800 text-white px-3 py-2 rounded-r text-sm font-bold">Search</button>
                </form>
            </div>
            
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm text-gray-600">
                    <thead class="bg-gray-50 text-gray-700 text-xs uppercase border-b border-gray-200">
                        <tr>
                            <th class="p-4">ID</th>
                            <th class="p-4">Title / Contributor</th>
                            <th class="p-4">Type / State</th>
                            <th class="p-4">Date</th>
                            <th class="p-4">Action</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        {% for sub in subs %}
                        <tr class="hover:bg-gray-50 transition">
                            <td class="p-4 font-mono font-bold text-gray-500">BV-SUB-{{ sub.id|stringformat:"06d" }}</td>
                            <td class="p-4">
                                <div class="font-bold text-gray-900">{{ sub.title }}</div>
                                <div class="text-xs text-gray-500">by {{ sub.contributor.username }}</div>
                            </td>
                            <td class="p-4">
                                <div class="font-bold">{{ sub.get_submission_type_display }}</div>
                                <div class="text-xs">{{ sub.state }}</div>
                            </td>
                            <td class="p-4 text-xs">{{ sub.created_at|date:"M d, Y" }}</td>
                            <td class="p-4">
                                <a href="{% url 'curator_review' sub.id %}" class="bg-indigo-600 text-white font-bold py-1.5 px-3 rounded text-xs shadow-sm hover:bg-indigo-700 transition">Review</a>
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="5" class="p-8 text-center text-gray-500">No submissions found in this queue.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",

    'contributions/curator_review.html': """{% extends 'base.html' %}
{% block title %}Review BV-SUB-{{ sub.id|stringformat:"06d" }}{% endblock %}
{% block content %}
<div class="bg-gray-900 py-6 border-b border-gray-800">
    <div class="max-w-7xl mx-auto px-4 flex justify-between items-center">
        <a href="{% url 'curator_dashboard' %}" class="text-gray-400 font-bold text-sm hover:text-white transition">&larr; Back to Dashboard</a>
        <span class="text-white font-mono font-bold bg-gray-800 px-3 py-1 rounded">BV-SUB-{{ sub.id|stringformat:"06d" }}</span>
    </div>
</div>

<div class="max-w-7xl mx-auto px-4 py-8 flex flex-col lg:flex-row gap-8">
    <!-- LEFT: Content -->
    <div class="w-full lg:w-2/3 bg-white rounded-xl shadow border border-gray-200 p-8">
        <div class="mb-8 pb-6 border-b border-gray-100 flex justify-between items-start">
            <div>
                <h1 class="text-3xl font-serif font-bold text-gray-900 mb-2">{{ sub.title }}</h1>
                <div class="text-sm text-gray-600">Submitted by <strong class="text-gray-900">{{ sub.contributor.username }}</strong> on {{ sub.created_at|date:"M d, Y" }}</div>
            </div>
            <div class="text-right">
                <div class="bg-gray-100 text-gray-800 text-xs font-bold px-2 py-1 rounded mb-1 uppercase">{{ sub.get_submission_type_display }}</div>
                <div class="text-gray-500 text-sm font-bold">{{ sub.state }}</div>
            </div>
        </div>
        
        <div class="prose max-w-none text-gray-800">
            {{ sub.content|linebreaks }}
        </div>
        
        {% if sub.source_note %}
        <div class="mt-8 bg-gray-50 p-4 rounded border-l-4 border-gray-300 text-sm text-gray-600">
            <strong>Source Note:</strong> {{ sub.source_note }}
        </div>
        {% endif %}
        
        {% if sub.image %}
        <div class="mt-8">
            <img src="{{ sub.image.url }}" class="rounded shadow border border-gray-200 max-w-full">
        </div>
        {% endif %}
    </div>
    
    <!-- RIGHT: Moderation Panel -->
    <div class="w-full lg:w-1/3">
        <div class="bg-indigo-50 rounded-xl shadow-sm border border-indigo-100 p-6 sticky top-24">
            <h3 class="font-bold text-indigo-900 border-b border-indigo-200 pb-3 mb-4 flex justify-between items-center">
                Moderation Action
                {% if sub.moderation_status == 'pending' %}
                <span class="bg-blue-600 text-white text-xs px-2 py-0.5 rounded">Pending</span>
                {% elif sub.moderation_status == 'approved' %}
                <span class="bg-green-600 text-white text-xs px-2 py-0.5 rounded">Approved</span>
                {% elif sub.moderation_status == 'rejected' %}
                <span class="bg-red-600 text-white text-xs px-2 py-0.5 rounded">Rejected</span>
                {% endif %}
            </h3>
            
            <form method="POST" action="{% url 'curator_review' sub.id %}">
                {% csrf_token %}
                <div class="mb-6">
                    <label class="block text-sm font-bold text-indigo-900 mb-2">Review Notes (Required for Rejection)</label>
                    <textarea name="review_comment" rows="4" class="w-full border border-indigo-200 rounded p-3 text-sm focus:ring-indigo-500 focus:border-indigo-500" placeholder="Add curator feedback for the contributor...">{{ sub.review_comment }}</textarea>
                </div>
                
                <div class="space-y-3">
                    <button type="submit" name="action" value="approve" class="w-full bg-green-600 text-white font-bold py-3 rounded shadow hover:bg-green-700 transition text-sm">✓ Approve & Publish</button>
                    <button type="submit" name="action" value="reject" class="w-full bg-red-600 text-white font-bold py-3 rounded shadow hover:bg-red-700 transition text-sm">✕ Return for Changes (Reject)</button>
                </div>
            </form>
            
            <div class="mt-6 text-xs text-indigo-700 bg-indigo-100 p-3 rounded">
                <strong>Important:</strong> Approving will make this content publicly searchable and award XP to the contributor.
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
}

for path, content in templates.items():
    full_path = os.path.join(BASE_DIR, 'templates', path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content)
    print(f"Generated {full_path}")
