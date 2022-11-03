'''
Here is my solution to the chest finder coding challenge!
I felt like searching through json objects the normal way is too slow, RegEx all the way baby

Next time I'll try to not use Python lol

~ Ludo
'''

import requests, re,time
newline_character = '\\r\\n'
starting_url = 'https://e0f5e8673c64491d8cce34f5.z35.web.core.windows.net/treasure.json'
boot_sizes = [0]*1024
dubloons = 0
dead_spiders = 0
location = ''
regex_next_chest_string = 'http\S+json'
regex_location_string = r'location":[ ]+"([-0-9. ]+)'
regex_diamond_string = r'"diamond": {[\\\\r\\\\n" a-z:0-9]+}'
regex_ruby_string = r'"ruby": {[\\\\r\\\\n" a-z:0-9]+}'
regex_sapphire_string = r'"sapphire": {[\\\\r\\\\n" a-z:0-9]+}'
regex_spider_string =r'"spider": {[\\\\r\\\\n "a-z:,]+}'
regex_boots_string = r'"boots": {[\\\\r\\\\n "a-z:A-Z.,0-9]+}'
regex_alive_string = r'"alive":[ ]+(\w+)'
regex_size_string = r'"size":[ ]+(\w+)'
regex_value_string = r'"value": ([0-9]+)'
def look_through_chests(url):
    #print('Begin searching in',url)
    string_chests = str(get_string_chest(url))
    def regex_finder(regex,finder_func):
        matches = re.findall(regex,string_chests)
        for match in matches:
            match = "{" + match.replace(newline_character,'') + "}"
            match_json = json.loads(match)
            finder_func(match_json)
    def rare_mineral_finder(mineral_string, mineral_regex, value):
        global dubloons
        matches = re.findall(mineral_regex,string_chests)
        for match in matches:
            num_mineral = int(re.findall('[0-9]+',match)[0])
            dubloons += num_mineral * value
    def look_for_dead_spiders():
        global dead_spiders
        matches = re.findall(regex_spider_string,string_chests)
        for match in matches:
            alive_or_dead = re.findall(regex_alive_string,match,re.M)[0]
            if alive_or_dead == 'false':
                dead_spiders+=1
    def look_for_boots():
        global boot_sizes
        matches = re.findall(regex_boots_string,string_chests)
        for match in matches:
            size = int(re.findall(regex_size_string,match,re.M)[0])
            boot_sizes[size]+=1
    def collect_all_the_monies():
        global dubloons
        matches = re.findall(regex_value_string, string_chests)
        for match in matches:
            dubloons += int(match)
    rare_mineral_finder('diamond',regex_diamond_string,400)
    rare_mineral_finder('ruby', regex_ruby_string,250)
    rare_mineral_finder('sapphire', regex_sapphire_string,200)
    collect_all_the_monies()
    look_for_dead_spiders()
    look_for_boots()
    if 'holy-grail' in string_chests:
        i = re.search('holy-grail', string_chests).end()
        cropped_string = string_chests[i:]
        location_coords = re.search(regex_location_string,cropped_string).groups()[0]
        global location
        location = location_coords

    #look for more chests
    chest_matches = re.findall(regex_next_chest_string, string_chests)
    for match in chest_matches:
        look_through_chests(match)

def get_string_chest(url):
    return requests.get(url).content
t = time.time()
look_through_chests(starting_url)
print('Holy Grail location:' , location)
print('Total chest value:', dubloons, 'doubloons')
print('Dead spiders:' , dead_spiders)
print('Most common boot size:', boot_sizes.index(max(boot_sizes)))
print('Time taken:',round(time.time() - t,2),'s')
