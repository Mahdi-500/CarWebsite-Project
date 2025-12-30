from django import template
from ..models import results

register = template.Library()

@register.simple_tag(name="race_career")
def first_last_race_of_team(id):
    result_data = results.objects.filter(constructor_id=id).order_by("race_id__year")
    return [result_data.first()['race_id__year'], result_data.last()['race_id__year']]