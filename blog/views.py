from django.shortcuts import render

def article(request):
    return render(request, 'blog/index.html')