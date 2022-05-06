from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db import connection


def get_bsr(request):
    labels = []
    with connection.cursor() as cursor:
        cursor.execute("Select distinct label from portfolio_task")
        for row in cursor.fetchall():
            labels.append(row[0])

    date_limit = datetime.today() - timedelta(days=120)
    sql = """ 
    select count(*), TO_CHAR(friday, 'DD/MM/YYYY') , label from portfolio_task 
    where friday >= %s
    group by friday, label 
    order by friday """
    result = []
    with connection.cursor() as cursor:
        cursor.execute(sql, [date_limit])
        for row in cursor.fetchall():
            result.append(
                {'friday': row[1], 'label': row[2], 'count': row[0]}
            )
    return JsonResponse({'labels': labels, 'results': result}, safe=False)


def get_bsr_by_id(request, id):
    labels = []
    with connection.cursor() as cursor:
        cursor.execute("Select distinct label from portfolio_task")
        for row in cursor.fetchall():
            labels.append(row[0])

    date_limit = datetime.today() - timedelta(days=150)
    sql = """ 
    select count(*), TO_CHAR(friday, 'DD/MM/YYYY') , label from portfolio_task 
    where board_id = %s and friday >= %s   group by friday, label   order by friday """
    result = []
    total = 0
    with connection.cursor() as cursor:
        cursor.execute(sql, [id, date_limit])
        for row in cursor.fetchall():
            result.append(
                {'friday': row[1], 'label': row[2], 'count': row[0]}
            )
            total += row[0]
    return JsonResponse({'labels': labels, 'results': result, 'total': total}, safe=False)

