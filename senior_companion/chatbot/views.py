from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .logic_engine import ChatBotEngine
import json

@require_POST
def chat_api(request):
    """
    API Endpoint that receives a JSON message and returns a JSON response.
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        # Initialize our Logic Brain
        bot = ChatBotEngine()
        
        # Get the answer
        result = bot.process(user_message, user=request.user)
        
        return JsonResponse({
            'status': 'success',
            'response': result['response'],
            'link': result['link']
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)