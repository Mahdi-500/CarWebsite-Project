from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import *
from .templatetags.custom_tags import driver_team, team_first_last_race
import datetime

def main_view(request):
    season_races = []
    for i in races.objects.filter(year=2025):
        season_races.append(i.race_id)
    race_results = results.objects.filter(race_id__in=season_races, final_position=1).order_by("race_id")
    return render(request, "F1_main.html", {"results":race_results})


def circuit_list_view(request):
    country_no = circuits.objects.distinct("country")
    circuit_data = circuits.objects.values('name', 'country', 'circuit_id').order_by("country")
    context = {
        "total_circuits":len(circuit_data),
        "total_countries":len(country_no),
        "all_circuits":circuit_data,
    }
    return render(request, "F1_circuit_list.html", context)


def circuit_detail_view(request, id):
    detail_data = circuits.objects.get(circuit_id=id)
    circuit_races_info = detail_data.races.all().order_by("year")
    context = {
        "circuit_details":detail_data,
        "circuit_race_info":circuit_races_info,
        "c_id":id,
        "total_races":len(circuit_races_info)
    }
    return render(request, "F1_circuit_detail.html", context)


def race_list_view(request):
    total_races = races.objects.values_list('race_id', 'name', 'round', 'year', 'race_time', 'race_date', 'circuit_id__name',
                                            'circuit_id__country').order_by('race_id')
    
    total_circuits = circuits.objects.values('circuit_id')
    # if datetime.datetime.now().month == 12:
    #     total_seasons = int(datetime.datetime.now().year) - 1950 + 1
    # else:
    #     total_seasons = (int(datetime.datetime.now().year) - 1 - 1950) + 1

    races_per_year = {}
    for i in total_races:
        races_per_year.setdefault(i[3], []).append(i)

    races_per_year = dict(sorted(races_per_year.items(), reverse=True))

    context = {
        "total_races":len(total_races),
        "total_years":len(races_per_year),
        "total_circuits":len(total_circuits),
        "races_per_year":races_per_year,
        "latest_year":list(races_per_year.keys())[0],
    }
    return render(request, "F1_race_list.html", context)


def race_details_view(request, r_id, c_id=None):
    race_info = races.objects.get(race_id=r_id)
    race_results = race_info.results.all().order_by("result_id")
    context = {
        "race_info":race_info,
        "race_results":race_results,
        "circuit_id":c_id
    }
    return render(request, "F1_race_detail.html", context)


def driver_list_view(request):

    search_query = request.GET.get('search', '').strip()
    queryset = driver_team()
    
    if search_query:
        q = Q()
        terms = search_query.split()
        for term in terms:
            q &= (
                Q(first_name__icontains=term) |
                Q(last_name__icontains=term) |
                Q(number__icontains=term) |
                Q(nationality__icontains=term)
            )
        queryset = queryset.filter(q)

    teams = constructors.objects.distinct('constructor_id')
    nationalities = drivers.objects.distinct('nationality')
    paginator = Paginator(queryset, per_page=20)
    page_number = request.GET.get('page')
    all_drivers = paginator.get_page(page_number)
    context = {
        "total_teams":len(teams),
        "total_nationalities":len(nationalities),
        "total_drivers":len(queryset),
        "all_drivers":all_drivers,
    }
    return render(request, "F1_driver_list.html", context)


def driver_details_view(request, id):
    driver_data = drivers.objects.get(driver_id=id)
    driver_results = driver_data.results.all().order_by("race_id__year")
    years = driver_results.values("race_id__year").distinct("race_id__year")
    
    # ? --- teams during driver cereer ---
    key = ""
    #last_team = ""
    temp_data = {}
    for i in range(len(list(years.values()))):
        team = driver_results.filter(race_id=list(years.values())[i]['race_id_id'])[0].constructor_id
        key = driver_results.filter(constructor_id=team.constructor_id).values('race_id__year').distinct('race_id__year')
        temp_data[team] = [i["race_id__year"] for i in key]
        if i + 1 == len(list(years.values())):
            last_team = team
    team_data = {}
    for i,j in temp_data.items():
        if len(j) > 1:
            team_data[i] = f"{j[0]} - {j[-1]}"
        elif j[0] == datetime.date.today().year:
            team_data[i] = f"{j[0]} - present"
        else:
            team_data[i] = f"{j[0]}"

    result_data = {}
    for i in years:
        result_data[i['race_id__year']] = driver_results.filter(race_id__year = i['race_id__year']).order_by("result_id")

    context = {
        "driver":driver_data,
        "last_team":last_team,
        "career_history":team_data,
        "seasons":sorted([i["race_id__year"] for i in years], reverse=True),
        "results_by_season":result_data

    }
    return render(request, "F1_driver_details.html", context)


def teams_list_view(request):
    teams_data = constructors.objects.all().order_by("name")
    nationalities = constructors.objects.distinct('nationality')
    active_teams = results.objects.filter(race_id__year=datetime.date.today().year).distinct('constructor_id')

    search_query = request.GET.get('search', '').strip()
    if search_query:
        q = Q()
        queries = search_query.split()
        for i in queries:
            q &= (Q(name__icontains=i))
        teams_data = teams_data.filter(q)

    paginator = Paginator(teams_data, per_page=20)
    page_number = request.GET.get("page")
    all_teams = paginator.get_page(page_number)

    context = {
        "total_teams":len(teams_data),
        "total_nationalities":len(nationalities),
        "active_teams":len(active_teams),
        "all_teams":all_teams,
    }
    return render(request, "F1_teams_list.html", context)