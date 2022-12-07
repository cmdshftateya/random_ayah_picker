#! /usr/bin/env python3
import random
import webbrowser
import requests
import datetime

def random_ayah_picker():
    

    # create a data structure to put info that we will randomize from
    official_surahs_and_ayahs = []

    with open("SurahInfoSheet1.csv", "r") as surahinfo:
        # print(surahinfo.readlines())
        # loop through surah info csv document to strip information about surahs
        # index to second line in order to skip the header
        for x in surahinfo.readlines()[1:]:
            # print(x)
            # turn each line into a list so we can use index to parse through
            individual_info = x.split(",")
            # use index to get the surah order in quran
            surah_index = individual_info[0]
            # use index to get the number of ayahs in said surah
            surah_ayah_count = individual_info[2]
            # put those things into a structure for a tuple
            b = surah_index, surah_ayah_count
            # append them to the list as a tuple
            official_surahs_and_ayahs.append(tuple(b))

    # for x in official_surahs_and_ayahs:
    #     # print(x)
    ayahs_requested = int(input("How many ayahs do you want? "))
    
    i = 0
    while i < ayahs_requested:
        # pick a random tuple from the list
        surah = random.choice(official_surahs_and_ayahs)
        # print(surah)
        surah_number = surah[0]
        print(surah_number)
        # pick a random ayah from the surah
        ayah_number = random.randint(1, int(surah[1]))
        print(ayah_number)

        # open it in the default browser
        # print(f'http://quran.com/{surah_number}/{ayah_number}/')
        # webbrowser.open(f'http://quran.com/{surah_number}/{ayah_number}/', new=2)
        
        # build copy paste item
        copypaste = ""

        # get the date
        now = datetime.datetime.now()
        day = now.strftime("%d")
        daymonth = now.strftime(f"%m/{day.lstrip('0')}")

        # add it all to a string
        first_line = "Ayah of the Day, " + daymonth + "\n\n"
        arabic = get_arabic(surah_number, ayah_number) + "\n\n"
        english = get_english(surah_number, ayah_number)
        surah_name = surah_name_transliteration(surah_number)
        name_line = "Surah " + surah_name + ", Ayah " + str(ayah_number) + "\n\n"
        copypaste = first_line + name_line + arabic + english 
        print(copypaste)

        i += 1

def get_arabic(surah_number, ayah_number):
    # make api calls to get stuff
    url = f'https://api.quran.com/api/v4/quran/verses/uthmani?verse_key={surah_number}%3A{ayah_number}'

    response = requests.get(url)
    x = response.json()
    return x['verses'][0]['text_uthmani']

def get_english(surah_number, ayah_number):
    url = f'https://api.quran.com/api/v4/quran/translations/85?verse_key={surah_number}%3A{ayah_number}'

    response = requests.get(url)
    x = response.json()
    return x['translations'][0]['text']

def surah_name_transliteration(surah_number):
    url = f'https://api.quran.com/api/v4/chapters/{surah_number}?language=en'

    response = requests.get(url)
    x = response.json()
    return x['chapter']['name_simple']
random_ayah_picker()