import time
from datetime import datetime

def get_exact_world_clock():
    utc_time = time.time()  
    
    utc_datetime = datetime.utcfromtimestamp(utc_time)
    
    formatted_time = utc_datetime.strftime('%Y-%m-%d %H:%M:%S.') + str(int((utc_time % 1) * 1000)).zfill(3)
    
    return formatted_time

world_clock = get_exact_world_clock()
print(f"Exact World Clock: {world_clock}")
