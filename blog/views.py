import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import urllib.request

# Add this function to your views.py
def article(request):
    return render(request, 'blog/article.html')  # Create this template or change to an existing one

# Get API key from environment or settings
def get_api_key():
    return os.environ.get("OPENAI_API_KEY", "")

@csrf_exempt
def chat_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message:
                return JsonResponse({"reply": "Please send a valid message."}, status=400)

            # OpenAI API endpoint
            url = "https://api.openai.com/v1/chat/completions"
            
            # Request data
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": user_message}]
            }
            
            # Convert payload to JSON string
            data = json.dumps(payload).encode('utf-8')
            
            # Create request
            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json')
            req.add_header('Authorization', f'Bearer {get_api_key()}')
            
            # Make request
            response = urllib.request.urlopen(req, data=data)
            response_data = json.loads(response.read().decode('utf-8'))
            
            reply = response_data["choices"][0]["message"]["content"].strip()
            return JsonResponse({"reply": reply})
            
        except json.JSONDecodeError:
            return JsonResponse({"reply": "Invalid JSON data."}, status=400)
        except Exception as e:
            return JsonResponse({"reply": f"An error occurred: {str(e)}"}, status=500)
    
    return JsonResponse({"reply": "Only POST requests are allowed."}, status=405)

# Function to render your existing index page
def index(request):
    return render(request, 'blog/index.html')