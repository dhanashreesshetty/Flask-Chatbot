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
        if raw['mood']==tag1:
            song.append(raw['name']+"      "+raw['artist']+"    "+raw['album'])
        if raw['mood']==tag2:
            song.append(raw['name']+"    "+raw['artist']+"    "+raw['album'])

    if len(song)>0:
        for i in range(8):
            song_display.append(song[i])

    #print(song_display)
    return song_display

