from datetime import datetime, timedelta

yesterday = datetime.today()
delta = timedelta(days=365)
min_day_value = (yesterday - delta).strftime("%Y-%m-%d")
max_day_value = (yesterday + delta).strftime("%Y-%m-%d")
tommorow = (yesterday + timedelta(days=1)).strftime("%Y-%m-%d")
