# *************************************************************************
# Course: CSP1114 PROBLEM SOLVING AND PROGRAM DESIGN
# Lecture / Lab Section: TC1L / TL1L
# Trimester: 2530
# Group Name (from eBwise): TL1L-03
# Names: Imanmalik Alim | Wong Winson | Yong Zi Jing
# IDs: 252FC253VV | 252FC2541L | 252FC253BP
# *************************************************************************

from db.classes import *
from sqlalchemy import text
from datetime import timedelta, datetime, timezone
def predictions():
    maxdate = -1
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    pt,dicti,currLetter,labels,letters,mxrev = [],dict(),'A',dict(),dict(),-1
    with engine.connect() as conn:
        result = conn.execute(text('SELECT "orders".created_at AS order_created_at, * FROM `orders` JOIN order_item ON `orders`.id = order_item.order_id LEFT JOIN product ON product.id = order_item.product_id')).fetchall()
        cutoff = conn.execute(text('SELECT MAX(created_at) FROM `orders`')).scalar()
        if isinstance(cutoff, str):
            cutoff = datetime.fromisoformat(cutoff)
        if cutoff.tzinfo is None:
            cutoff = cutoff.replace(tzinfo=timezone.utc)
        recent = cutoff - timedelta(days=20)
        for row in result:
            d = row[0]   # this is order_created_at from the SELECT clause

            if d is None:
                continue  # skip rows with no order_created_at

            if isinstance(d, str):
                d = datetime.fromisoformat(d)
            if d.tzinfo is None:
                d = d.replace(tzinfo=timezone.utc)
            if d >= recent:
                if maxdate == -1:
                    maxdate = d
                if maxdate < d:
                    maxdate = d
                dicti[row.name] = dicti.get(row.name,0) + row.quantity
                if labels.get(row.name,'') == '':
                    labels[row.name] = currLetter
                    letters[currLetter] = row.name
                    currLetter = chr(ord(currLetter) + 1)
                price = row.price if row.price is not None else 0
                if mxrev == -1:
                    mxrev = row.quantity*price
                else:
                    mxrev = max(mxrev,row.quantity*price)
                day_offset = (cutoff.date() - d.date()).days
                if 0 <= day_offset < 20:
                    pt.append((
                        row.quantity * price,
                        20 - day_offset,
                        labels[row.name]
                    ))

    if maxdate == -1:
        print("No orders for this time period")
        exit(0)
    maxdate = [int(a) for a in str(maxdate).split(' ')[0].split('-')]
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    m = maxdate[1]-1
    m -= 1
    if m < 0:
        m = 11
    days = list(range(max(1,maxdate[2]+1-20),maxdate[2]+1))
    needed = max(0,20 - maxdate[2])
    if needed>0:
        days = list(range(days_in_month[m]+1-needed,days_in_month[m]+1)) + days
    cutoff = recent
    cutoff = [int(a) for a in str(cutoff).split(' ')[0].split('-')]
    cli_x,cli_y,range_x = 20,20*3,(0,mxrev)
    len_x,len_y = (range_x[1]-range_x[0]) / cli_x,20 / cli_y
    x_scale = [(str(range_x[1]-round(i*len_x)) + '-' + str(round(range_x[1]-i*len_x-len_x))) for i in range(cli_x)]
    y_scale = [str(i) for i in days]
    pad = len(x_scale[0])
    def convert_to_cli(x,y):
        return cli_x-min(cli_x-1,int((x-range_x[0]) // len_x))-1,round(min(cli_y-1,int(y-1) // len_y))
    matrix = [['.' for i in range(cli_y)] for j in range(cli_x)]
    for i in range(len(pt)):
        p = pt[i]
        x,y = convert_to_cli(p[0],p[1])
        matrix[x][y] = p[2] if matrix[x][y]=='.' else '*'
    print(f'Revenue in RM, {', '.join([a + ' - ' + b for a,b, in list(letters.items())])}' + ', * - Multiple items')
    for i in range(len(matrix)):
        print(x_scale[i].rjust(pad) + ' ' + ''.join(matrix[i]))
    print(' '*(pad+1) + ''.join([s.ljust(3) for s in y_scale]))
    print(' '*(pad+1) + f'{months[cutoff[1]-1]} {cutoff[0]} - {months[maxdate[1]-1]} {maxdate[0]}')
if __name__=="__main__":
    predictions()