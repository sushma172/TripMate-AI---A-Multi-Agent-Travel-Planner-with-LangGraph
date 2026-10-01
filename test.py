from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights

# result = tavily_search("best resorts in chikmangalur")
# print(result)

res=search_flights("Plan a 5 days Japan trip")
print(res)