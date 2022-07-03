from datetime import datetime
import time
#date = datetime.utcfromtimestamp(1583222427000)
#datetime.utcfromtimestamp(1583222427000).strftime('%Y-%m-%dT%H:%M:%SZ')
#date = time.ctime(int("1583222427000"))

epoch_time = 1583222427000

# truncate last 3 digits because they're milliseconds
epoch_time = str(epoch_time)[0: 10]

# print timestamp without milliseconds
date = datetime.fromtimestamp(float(epoch_time)).strftime('%m/%d/%Y -- %H:%M:%S')

print(date)
