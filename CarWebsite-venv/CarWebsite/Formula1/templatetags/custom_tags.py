from django import template
from django.db.models import Subquery, OuterRef
from ..models import races, drivers, results, constructors
from django.utils.dateparse import parse_duration
import datetime

register = template.Library()

@register.filter(name="has_sprint")
def sprint_status(value):
    try:
        query = races.objects.get(race_id=value)
    except TypeError:
        query = value
    return  query.sprint_race_date is not None

@register.filter(name="is_completed")
def race_status(value):
    return value < datetime.date.today()

@register.simple_tag(name="time_calculator")
def calculator(original, id):
    if original is not None:
        first_place_time = results.objects.get(race_id=id, final_position='1').time
        converted_first_place_time = parse_duration(first_place_time)
        if original.startswith("+") and not original.endswith("lap"):
            if original.endswith("s"):
                original = original.replace("s", "")
            converted_original_time = parse_duration(original[1:])
            return str(converted_first_place_time + converted_original_time)
        else:
            return original

@register.simple_tag(name="total_season")
def season_calculator(first, last):
    return last - first + 1

def driver_team():
    return drivers.objects.annotate(last_team=Subquery(results.objects.filter(driver_id=OuterRef('driver_id')).order_by("-result_id").values('constructor_id__name')[:1])).order_by("first_name", "last_name")

@register.simple_tag(name="race_career")
def team_first_last_race(id):
    constructor_data = constructors.objects.get(constructor_id=id)
    return [constructor_data.results.values("race_id__year").distinct("race_id__year").order_by("race_id__year")[0]['race_id__year'], 
            constructor_data.results.values("race_id__year").distinct("race_id__year").order_by("-race_id__year")[0]['race_id__year']]
    # return constructors.objects.annotate(first_race_year=Subquery(results.objects.filter(constructor_id=OuterRef('constructor_id')).order_by("result_id").values("race_id__year")[:1]), 
    #                                                         last_race_year=Subquery(results.objects.filter(constructor_id=OuterRef('constructor_id')).order_by("-result_id").values("race_id__year")[:1])).order_by("name")
