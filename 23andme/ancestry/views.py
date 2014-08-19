from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.conf import settings
import json
import requests


def home(request):
    data = {
        'logged_in': request.session.has_key('access_token')
    }
    return render(request, 'ancestry/home.html', data)


def api_login(request):
    return redirect('https://api.23andme.com/authorize/?'
                    +'redirect_uri='+settings.GENEOLOGY['redirect_uri']
                    +'&response_type=code'
                    +'&client_id='+settings.GENEOLOGY['client_id']
                    +'&scope='+settings.GENEOLOGY['scope'])


def api_logout(request):
    del request.session['access_token']

    return redirect('ancestry:home')


def api_callback(request):
    if request.GET.has_key('code'):
        post_data = {
            'client_id': settings.GENEOLOGY['client_id'],
            'client_secret': settings.GENEOLOGY['client_secret'],
            'grant_type': 'authorization_code',
            'code': request.GET['code'],
            'redirect_uri': settings.GENEOLOGY['redirect_uri'],
            'scope': settings.GENEOLOGY['scope'],
        }
        r = requests.post('https://api.23andme.com/token/', data=post_data)

        response = r.json()

        request.session['access_token'] = response['access_token']

    return redirect('ancestry:home')


def call(request):
    headers = {
        'Authorization': 'Bearer '+request.session['access_token']
    }
    locations = [
        'rs8176719',
        'rs8176746',
        'rs8176747',
        'rs590787',
    ]
    params = {
        # 'locations': ' '.join(locations)
    }
    
    r = requests.get('https://api.23andme.com/1/haplogroups/ec9db3635fd20e95/',
                     headers=headers,
                     params=params)
    
    return HttpResponse(json.dumps(r.json(), indent=3))
