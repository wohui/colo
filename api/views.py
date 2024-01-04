from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def test_view(request):
    res= {
        'data':[1,2,3]
    }
    return JsonResponse(res,safe=False)

git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/wohui/colo.git
git push -u origin main