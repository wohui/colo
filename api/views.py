from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def test_view(request):
    res= {
        'data':[1,2,3]
    }
    return JsonResponse(res,safe=False)