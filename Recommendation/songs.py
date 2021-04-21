import csv
song=[]
song_display=[]
#tag1=""
#tag2=""
def songs(emotion):
    reader = csv.DictReader(open('data_moods.csv', encoding="utf8"))
    if emotion=='sadness':
        tag1='Happy'
        tag2='Sad'
    if emotion=='fear':
        tag1='Calm'
        tag2='Happy'
    if emotion=='anger':
        tag1='Calm'
        tag2='Calm'
    if emotion=='joy':
        tag1='Happy'
        tag2='Energetic'
    for raw in reader:
        dic1={}
        if raw['mood']==tag1:
            dic1={"name":raw['name'],"artist":raw['artist'],"album":raw['album']}
            song.append(dic1)
        if raw['mood']==tag2:
            dic1={"name":raw['name'],"artist":raw['artist'],"album":raw['album']}
            song.append(dic1)

    if len(song)>0:
        for i in range(8):
            song_display.append(song[i])

    #print(song_display)
    return song_display
