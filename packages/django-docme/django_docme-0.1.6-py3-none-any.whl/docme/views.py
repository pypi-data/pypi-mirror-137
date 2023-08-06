from django.conf import settings
from django.core.management import call_command
from pkg_resources import resource_string
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from jinja2 import Template
import json

def json_script():
    json_scripts = [json.load(open(json_script))
                    for json_script in settings.AUTO_TOUR_SCRIPTS]
    json_doc = {}
    for json_script in json_scripts:
        json_doc.update(json_script)
    return json_doc

def auto_tour_index(request):
    return render(request, 'docme/index.html', {'json_doc':json_script()})

def start_tour(request):
    scenario = json_script()[request.GET['app']][request.GET['feature_name']
                                                 ]['scenarios'][request.GET['scenario_name']]
    call_command('flush')
    for fixture in scenario['fixtures']:
        call_command('loaddata', fixture, skip_checks=True)
    return JsonResponse({'next_path': scenario['first_path']})


def get_steps(request):
    scenario = json_script()[request.GET['app']][request.GET['feature_name']
                                                 ]['scenarios'][request.GET['scenario_name']]
    return JsonResponse({'steps': scenario['steps'][request.GET['current_path']]})
