from django.shortcuts import render
from .models import Visit
from django.db.models import Q
from datetime import timedelta
import datetime
from django.contrib.admin.views.decorators import staff_member_required

# only staff (admins and superadmins) can see the stats
@staff_member_required
def stats(request):
    # get the input data 
    date        = request.GET.get('date', False)
    start_date  = request.GET.get('start_date', False)
    end_date    = request.GET.get('end_date', False)

    # check if the we are going to filter by the date
    if date:
        # we count the number of rows in our visit table in the corresponding date ==> SELECT COUNT(*) FROM visits_visit WHERE created_date=date
        all_visits                  = Visit.objects.filter(created_at__date=date).count()
        # we count the number of rows in our visit table in the corresponding date for only anonymous ==> SELECT COUNT(*) FROM visits_visit WHERE created_date=date AND user=null
        anonymous_visits            = Visit.objects.filter(user=None, created_at__date=date).count()
        # we count the number of rows in our visit table in the corresponding date for only users ==> SELECT COUNT(*) FROM visits_visit WHERE created_date=date AND user<>null
        user_visits                 = Visit.objects.filter(~Q(user=None), created_at__date=date).count()
        # we count the number of unique rows in our visit table in the corresponding date  ==> SELECT COUNT(DISTICT ip_address) FROM visits_visit WHERE created_date=date
        all_unique_visits           = Visit.objects.filter(created_at__date=date).values_list('ip_address').order_by('ip_address').distinct().count()
        # we count the number of unique rows in our visit table in the corresponding date for only anonymous ==> SELECT COUNT(DISTICT ip_address) FROM visits_visit WHERE created_date=date AND user=null
        anonymous_unique_visits     = Visit.objects.filter(user=None, created_at__date=date).values_list('anonymous').order_by('ip_address').distinct().count()
        # we count the number of unique rows in our visit table in the corresponding date for only users ==> SELECT COUNT(DISTICT ip_address) FROM visits_visit WHERE created_date=date AND user<>null
        user_unique_visits          = Visit.objects.filter(~Q(user=None), created_at__date=date).values_list('ip_address').order_by('ip_address').distinct().count()
    # check if the we are going to filter by the start date and the end date
    elif start_date and end_date:
        # we count the number of rows in our visit table in the range of dates ==> SELECT COUNT(*) FROM visits_visit WHERE created_date=date
        all_visits                  = Visit.objects.filter(created_at__range=(start_date, end_date)).count()
        # we count the number of rows in our visit table in the range of dates for only anonymous ==> SELECT COUNT(*) FROM visits_visit WHERE created_date=date AND user=null
        anonymous_visits            = Visit.objects.filter(user=None, created_at__range=(start_date, end_date)).count()
        # we count the number of rows in our visit table in the range of dates for only users ==> SELECT COUNT(*) FROM visits_visit WHERE created_date=date AND user<>null
        user_visits                 = Visit.objects.filter(~Q(user=None), created_at__range=(start_date, end_date)).count()
        # we count the number of unique rows in our visit table in the range of dates  ==> SELECT COUNT(DISTICT ip_address) FROM visits_visit WHERE created_date=date
        all_unique_visits           = Visit.objects.filter(created_at__range=(start_date, end_date)).values_list('ip_address').order_by('ip_address').distinct().count()
        # we count the number of unique rows in our visit table in the range of datese for only anonymous ==> SELECT COUNT(DISTICT ip_address) FROM visits_visit WHERE created_date=date AND user=null
        anonymous_unique_visits     = Visit.objects.filter(user=None, created_at__range=(start_date, end_date)).values_list('ip_address').order_by('ip_address').distinct().count()
        # we count the number of unique rows in our visit table in the range of dates for only users ==> SELECT COUNT(DISTICT ip_address) FROM visits_visit WHERE created_date=date AND user<>null
        user_unique_visits          = Visit.objects.filter(~Q(user=None), created_at__range=(start_date, end_date)).values_list('ip_address').order_by('ip_address').distinct().count()
    # check if there are no request parameters we are going to send all the data 
    else:
        # we count the number of rows in our visit table ==> SELECT COUNT(*) FROM visits_visit WHERE created_date=date
        all_visits                  = Visit.objects.all().count()
        # we count the number of rows in our visit table for only anonymous ==> SELECT COUNT(*) FROM visits_visit WHERE created_date=date AND user=null
        anonymous_visits            = Visit.objects.filter(user=None).count()
        # we count the number of rows in our visit table for only users ==> SELECT COUNT(*) FROM visits_visit WHERE created_date=date AND user<>null
        user_visits                 = Visit.objects.filter(~Q(user=None)).count()
        # we count the number of unique rows in our visit table  ==> SELECT COUNT(DISTICT ip_address) FROM visits_visit WHERE created_date=date
        all_unique_visits           = Visit.objects.values_list('ip_address').order_by('ip_address').distinct().count()
        # we count the number of unique rows in our visit table for only anonymous ==> SELECT COUNT(DISTICT ip_address) FROM visits_visit WHERE created_date=date AND user=null
        anonymous_unique_visits     = Visit.objects.filter(user=None).values_list('ip_address').order_by('ip_address').distinct().count()
        # we count the number of unique rows in our visit table for only users ==> SELECT COUNT(DISTICT ip_address) FROM visits_visit WHERE created_date=date AND user<>null
        user_unique_visits          = Visit.objects.filter(~Q(user=None)).values_list('ip_address').order_by('ip_address').distinct().count()
        
    # format the JSON result object in the required format
    context = {
        "date": date, 
        "start_date": start_date, 
        "end_date": end_date, 
        "all_visits": all_visits, 
        "user_visits": user_visits,
        "anonymous_visits": anonymous_visits,
        "all_unique_visits": all_unique_visits,
        "user_unique_visits": user_unique_visits,
        "anonymous_unique_visits": anonymous_unique_visits,
        }
    # return the result to the stats template (where we will draw the chart)
    return render(request, 'stats.html', context)
