# import datetime
# import  time
#
# class Bid:
#     def __init__(self, item, starting_price, duration_hours):
#         self.item = item
#         self.starting_price = starting_price
#         self.current_bid = starting_price
#         self.bidder = None
#         self.end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
#         self.duration_hours = duration_hours
#
#     def start_auction(self):
#         # Simulate auction duration (replace with actual bidding logic)
#         time.sleep(self.duration_hours * 3600)  # Sleep for duration in seconds
#     def get_remaining_time(self):
#         """Returns the remaining time until the auction ends in a human-readable format."""
#         return self.get_remaining_time(self.end_time)
#
#     # ... other methods for bid management
#
# # Example usage:
# bid = Bid("Painting", 100, 8)  # Auction ending in 8 hours
# print(bid.get_remaining_time())

import datetime

def get_remaining_time(end_time):
    """Calculates the remaining time in a human-readable format (days, hours, minutes, seconds)."""
    now = datetime.datetime.now()
    delta = end_time - now
    days, remaining = divmod(delta.total_seconds(), 86400)
    hours, remaining = divmod(remaining, 3600)
    minutes, seconds = divmod(remaining, 60)
    time_left = []
    if days > 0:
        time_left.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        time_left.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        time_left.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    time_left.append(f"{seconds} second{'s' if seconds > 1 else ''}")
    return ' '.join(time_left) or "Auction Ended"

print(get_remaining_time(datetime.datetime(2024,6,5,23)))