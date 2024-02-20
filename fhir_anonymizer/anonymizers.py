

import datetime
import hashlib
import random
from time import strptime


def hash_string():
    return lambda x,y,z: hashlib.sha256(x.encode()).hexdigest()

def mask(value = "REDACTED"):
    return value



def shift_time(variance=90):
    def _shift_time(date_str):
        date_obj = strptime(date_str, "%Y-%m-%d")
        random_days = random.randint(-variance, variance)
        new_date_obj = date_obj + datetime.timedelta(days=random_days)
        return new_date_obj.strftime("%Y-%m-%d")


    return lambda x,y,z: _shift_time(x)
