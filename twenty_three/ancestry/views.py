import requests

from django.shortcuts import redirect, render
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView


def home(request):
    data = {
        'logged_in': 'access_token' in request.session
    }
    return render(request, 'ancestry/home.html', data)


def api_login(request):
    return redirect('https://api.23andme.com/authorize/?'
                    + 'redirect_uri='+settings.GENEOLOGY['redirect_uri']
                    + '&response_type=code'
                    + '&client_id='+settings.GENEOLOGY['client_id']
                    + '&scope='+settings.GENEOLOGY['scope'])


def api_logout(request):
    del request.session['access_token']
    del request.session['user_id']

    return redirect('ancestry:home')


def api_callback(request):
    if 'code' in request.GET:
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


def get_headers(request):
    return {
        'Authorization': 'Bearer '+request.session['access_token']
    }


def get_id(request):
    if 'user_id' in request.session:
        return request.session['user_id']
    else:
        r = requests.get('https://api.23andme.com/1/user/',
                         headers=get_headers(request))
        request.session['user_id'] = r.json()['profiles'][0]['id']
        return request.session['user_id']


class HaplogroupsAPIView(APIView):

    def get(self, request, *args, **kwargs):

        r = requests.get('https://api.23andme.com/1/haplogroups/{0}/'.format(get_id(request)),
                         headers=get_headers(request))

        return Response(r.json())


class AncestryAPIView(APIView):

    def get(self, request, *args, **kwargs):

        r = requests.get('https://api.23andme.com/1/ancestry/{0}/'.format(get_id(request)),
                         headers=get_headers(request))

        return Response(r.json())


class NeanderthalAPIView(APIView):

    def get(self, request, *args, **kwargs):

        r = requests.get('https://api.23andme.com/1/neanderthal/{0}/'.format(get_id(request)),
                         headers=get_headers(request))

        return Response(r.json())


class GenotypesAPIView(APIView):

    def get(self, request, *args, **kwargs):

        locations = [
            'rs2853518',
            'i3001947',
            'i5050606',
        ]
        params = {
            'locations': ' '.join(locations)
        }

        r = requests.get('https://api.23andme.com/1/genotypes/{0}/'.format(get_id(request)),
                         headers=get_headers(request),
                         params=params)

        return Response(r.json())

