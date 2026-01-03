import datetime as dt

def minutes_between(t1, t2):
    # returns minutes from t1 to t2 (t2 - t1) where both are time
    d = dt.date(2000,1,1)
    dt1 = dt.datetime.combine(d, t1)
    dt2 = dt.datetime.combine(d, t2)
    return int((dt2 - dt1).total_seconds() // 60)

def clamp_nonneg(x):
    return x if x > 0 else 0
