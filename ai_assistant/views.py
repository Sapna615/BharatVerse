from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services import AIService

@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            
            ai = AIService()
            response_text = ai.ask_cultural_question(message)
            
            return JsonResponse({
                'success': True,
                'mode': 'demo' if ai.demo_mode else 'live',
                'message': response_text,
                'sources': ['BharatVerse Knowledge Base']
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
