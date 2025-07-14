from datetime import datetime, timedelta

current_time = datetime.utcnow()
start_of_week_previous = (current_time - timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
start_of_week_ahead = (current_time + timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
