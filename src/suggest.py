from sources.eventbrite import suggest_from_eventbrite
from sources.groupon import suggest_from_groupon
total = 0
total += suggest_from_eventbrite()
total += suggest_from_groupon()
print(f"Suggestions added: {total}. See data/out/suggestions.csv")
