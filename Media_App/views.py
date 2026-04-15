from django.shortcuts import render
from .models import *
from django.db import connection


def index(request):
    return render(request, 'index.html')


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def QueryResults(request):
    with connection.cursor() as cursor:
        sql1 = """SELECT P.genre,P.title,P.duration
                FROM Programs P
                WHERE SUBSTRING(P.genre,1,1) = 'A' and
                    P.title = ANY (SELECT distinct RR.title
                        FROM Households HH,RecordReturns RR
                        WHERE HH.hid=RR.hID and  HH.ChildrenNum = 0
                        GROUP BY RR.title
                        HAVING COUNT(RR.hID)>=1
                        ) and
                        P.duration >= ALL (SELECT P1.duration
                         FROM Programs P1
                        where P1.genre=P.genre)
                        GROUP BY P.title,P.duration,P.genre
                        ORDER BY P.genre ASC, P.title"""
        cursor.execute(sql1)
        result_sql1=dictfetchall(cursor)
        sql2 = """select PR.title, cast(avg(cast((PR.rank)as decimal)) as decimal (10,2)) as Average_Rank
                from ProgramRanks PR inner join kosherProgram KP on PR.title = KP.Title
                group by PR.title
                ORDER BY Average_Rank desc,PR.title"""
        cursor.execute(sql2)
        result_sql2=dictfetchall(cursor)
        sql3 = """SELECT DISTINCT YS.title
                FROM YokratitShow YS
                    WHERE YS.title NOT IN(
                    (SELECT DISTINCT PR.title
                    FROM ProgramRanks PR
                    WHERE PR.rank<2))
                    ORDER BY YS.title"""
        cursor.execute(sql3)
        result_sql3=dictfetchall(cursor)
    return render(request, 'QueryResults.html',{'result_sql2':result_sql2,'result_sql1':result_sql1,'result_sql3':result_sql3})


def RecordsManagement(request):
    flag = 0
    sql_result=ShowRecordReturns()
    if request.method == "POST" and request.POST:
        new_hid = request.POST["hID"]
        new_title = request.POST["title"]
        with connection.cursor() as cursor:
            cursor.execute("select hID from Households where hID= %s", (new_hid,))
            condition1 = dictfetchall(cursor)
            if len(condition1) == 0:
                flag = 1
                return render(request, 'RecordsManagement.html', {'flag': flag, 'sql_result': sql_result})
            else:
                cursor.execute("select title from Programs where title=%s", (new_title,))
                condition2 = dictfetchall(cursor)
                if len(condition2) == 0:
                    flag = 2
                    return render(request, 'RecordsManagement.html', {'flag': flag, 'sql_result': sql_result})
                else:
                    cursor.execute(
                        "select distinct hID from RecordOrders where hID= any(select hid from RecordOrders GROUP BY hID having (count(distinct title)=3)) and hID=%s",
                        (new_hid,))
                    condition3 = dictfetchall(cursor)
                    if len(condition3) != 0:
                        flag = 3
                        return render(request, 'RecordsManagement.html', {'flag': flag, 'sql_result': sql_result})
                    else:
                        cursor.execute("select hID from RecordOrders WHERE hID!=%s AND title=%s", (new_hid, new_title))
                        condition4 = dictfetchall(cursor)
                        if len(condition4) != 0:
                            flag = 4
                            return render(request, 'RecordsManagement.html', {'flag': flag, 'sql_result': sql_result})
                        else:
                            cursor.execute("SELECT * FROM RecordOrders WHERE (hID = %s AND title = %s)",
                                           (new_hid, new_title))
                            condition5 = dictfetchall(cursor)
                            if len(condition5) != 0:
                                flag = 5
                                return render(request, 'RecordsManagement.html', {'flag': flag, 'sql_result': sql_result})
                            else:
                                cursor.execute("select * from RecordReturns where (hID = %s AND title = %s)",
                                               (new_hid, new_title))
                                condition6 = dictfetchall(cursor)
                                if len(condition6) != 0:
                                    flag = 6
                                    return render(request, 'RecordsManagement.html',
                                                  {'flag': flag, 'sql_result': sql_result})
                                else:
                                    cursor.execute(
                                        "select distinct h.hID from Households H,Programs P where ChildrenNum!=0 and P.title = ANY(select p.title from Programs P where p.genre='Adults only' or p.genre='Reality') and P.title=%s",
                                        (new_title,))
                                    condition7 = dictfetchall(cursor)
                                    if len(condition7) != 0:
                                        flag = 7
                                        return render(request, 'RecordsManagement.html',
                                                      {'flag': flag, 'sql_result': sql_result})
                                    else:
                                        insert_sql = """Insert into RecordOrders (title, hID) values (%s, %s)"""
                                        cursor.execute(insert_sql, [new_title, new_hid])
    sql_result=ShowRecordReturns()
    return render(request, 'RecordsManagement.html', {'sql_result': sql_result})


def returnOrder(request):
    flag_of_return = 0
    sql_result=ShowRecordReturns()
    if request.method == "POST" and request.POST:
        new_hid = request.POST["return_hID"]
        new_title = request.POST["return_title"]
        with connection.cursor() as cursor:
            cursor.execute("select hID from Households where hID= %s", (new_hid,))
            result = dictfetchall(cursor)
            if len(result) == 0:
                flag_of_return = 1
                return render(request, 'RecordsManagement.html',
                              {'flag_of_return': flag_of_return, 'sql_result': sql_result})
            else:
                cursor.execute("select title from Programs where title=%s", (new_title,))
                result = dictfetchall(cursor)
                if len(result) == 0:
                    flag_of_return = 2
                    return render(request, 'RecordsManagement.html',
                                  {'flag_of_return': flag_of_return, 'sql_result': sql_result})
                else:
                    cursor.execute("select hID from RecordOrders WHERE (hID!=%s AND title=%s)", (new_hid, new_title))
                    result = dictfetchall(cursor)
                    cursor.execute("select title from RecordOrders WHERE %s=title", (new_title,))
                    result1 = dictfetchall(cursor)
                    if len(result) != 0 or len(result1)==0:
                        flag_of_return = 3
                        return render(request, 'RecordsManagement.html',
                                      {'flag_of_return': flag_of_return, 'sql_result': sql_result})
                    else:
                        delete_from_orders_sql = """DELETE FROM RecordOrders where title = %s and hID = %s"""
                        cursor.execute(delete_from_orders_sql, [new_title, new_hid])
                        insert_to_returns_sql = """INSERT INTO RecordReturns (title, hID) values (%s, %s)"""
                        cursor.execute(insert_to_returns_sql, [new_title, new_hid])
    sql_result=ShowRecordReturns()
    return render(request, 'RecordsManagement.html', {'sql_result': sql_result})

def ShowRecordReturns():
    with connection.cursor() as cursor:
        sql3_c = """SELECT TOP 3 max(distinct TEMP.hid)as hID, COUNT( DISTINCT TEMP.title) as Total_Orders
                        FROM  (select * from RecordReturns UNION SELECT * FROM RecordOrders) AS TEMP
                        group by TEMP.hid
                        ORDER BY Total_Orders DESC,hID asc"""
        cursor.execute(sql3_c)
        sql_result = dictfetchall(cursor)
    return sql_result


def Rankings(request):
    with connection.cursor() as cursor:
        cursor.execute("select hID from Households")
        list_of_hid = dictfetchall(cursor)
        cursor.execute("select title from Programs")
        list_of_program = dictfetchall(cursor)
        cursor.execute("select genre from Programs p group by genre having count(title)>=5")
        list_of_genre =dictfetchall(cursor)
        if request.method == "POST" and request.POST:
            new_hid = request.POST.get("hID")
            new_title = request.POST.get("title")
            new_rank = request.POST.get("rank")
            new_genre = request.POST.get("genre")
            new_min_rank = request.POST.get("min_rank")
            if new_hid and new_title and new_rank :
                cursor.execute("select hID from ProgramRanks where hID= %s and title=%s", (new_hid,new_title))
                result=dictfetchall(cursor)
                if len(result) != 0:
                    update_rank="""UPDATE ProgramRanks SET hID=%s,title=%s , rank=%s WHERE hID= %s and title=%s"""
                    cursor.execute(update_rank,(new_hid,new_title,new_rank,new_hid,new_title))
                else:
                    insert_rank = """INSERT INTO ProgramRanks(title, hID, rank) values (%s,%s,%s)"""
                    cursor.execute(insert_rank,(new_title,new_hid,new_rank))
            elif new_genre and new_min_rank:
                min_rank="""select top 5 PR.title, cast(avg(cast((pr.rank)as decimal))as decimal(10,2)) as Average_rank
                                from ProgramRanks PR
                                where PR.title in(select P.title from Programs P where genre=%s)
                                group by PR.title
                                HAVING COUNT(*)>= %s
                                order by Average_rank desc;"""
                cursor.execute(min_rank,(new_genre,new_min_rank))
                spoken_program = dictfetchall(cursor)
                if len(spoken_program) >= 5:
                    return render(request, 'Rankings.html', {'list_of_hid': list_of_hid, 'list_of_program': list_of_program,
                                                             'list_of_genre': list_of_genre,'spoken_program':spoken_program})
                else:
                    min_rank_complete = """SELECT distinct TOP (5-%s) P.title ,0 as Average_rank
                                            from Programs P left join (select top 5 PR.title, cast(avg(cast((pr.rank)as decimal))as decimal(10,2)) as Average_rank
                                            from ProgramRanks PR
                                            where PR.title in(select P.title from Programs P where genre=%s)
                                            group by PR.title
                                            HAVING COUNT(*)>= %s
                                            order by Average_rank desc) as SpokenProgram on SpokenProgram.title=P.title
                                            WHERE SpokenProgram.title IS NULL AND P.genre=%s
                                            ORDER BY Average_rank ASC;"""
                    cursor.execute(min_rank_complete,(len(spoken_program),new_genre,new_min_rank,new_genre))
                    complete_spoken_program = dictfetchall(cursor)
                    return render(request, 'Rankings.html', {'list_of_hid': list_of_hid, 'list_of_program': list_of_program,
                                                             'list_of_genre': list_of_genre,'spoken_program': spoken_program ,
                                                             'complete_spoken_program': complete_spoken_program})
    return render(request, 'Rankings.html',{'list_of_hid': list_of_hid,'list_of_program':list_of_program,'list_of_genre': list_of_genre})
