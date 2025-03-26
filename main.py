import requests
import heapq
from config import api_key
headers = {
    'accept': 'application/json',
    'X-API-Key': api_key,
}
username = str(input("Enter username or UID: "))
print("Updating player data...")
requests.get(f'https://marvelrivalsapi.com/api/v1/player/{username}/update', headers=headers)
print("Player data updated. Requesting data...")
response = requests.get(f'https://marvelrivalsapi.com/api/v1/player/{username}', headers=headers)
match response.status_code:
    case 200:
        print("Success")
    case 403:
        print("Error: Private profile")
    case 404:
        print("Error. Typo?")
    case 500:
        print("Server error")
    case _:
        print("Unknown error")
data = response.json()
total_comp_matches = data['overall_stats']['ranked']['total_matches']
total_comp_wins = data['overall_stats']['ranked']['total_wins']
mvp_and_svp = data['overall_stats']['ranked']['total_mvp'] + data['overall_stats']['ranked']['total_svp']
player_rank = data['player']['rank']['rank']
winrate = total_comp_wins / total_comp_matches
top_3_played = heapq.nlargest(3, data['heroes_ranked'], key=lambda x: x['play_time'])
most_played = top_3_played[0]['hero_name']
second_most_played = top_3_played[1]['hero_name']
third_most_played = top_3_played[2]['hero_name']
most_playtime = int(top_3_played[0]['play_time']) / 3600
second_most_playtime = int(top_3_played[1]['play_time']) / 3600
third_most_playtime = int(top_3_played[2]['play_time']) / 3600
print(f"Total comp matches: {total_comp_matches}")
print(f'Total MVPs: {mvp_and_svp}')
print(f'Player rank: {player_rank}')
print(f'Comp winrate: {winrate:.2%}')
print(f'Most played: {most_played}, {most_playtime:.2f} hours')
print(f'Second most played: {second_most_played}, {second_most_playtime:.2f} hours')
print(f'Third most played: {third_most_played}, {third_most_playtime:.2f} hours')