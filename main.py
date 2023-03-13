import json
import requests
from secrets import spotify_user_id, hipHopPlaylist_id
from datetime import date
from refresh import refresh

class saveSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.tracks = ""
        self.new_playlist_id = ""
        self.trackList = ""

    def create_playlist(self):
        todaysDate = date.today().strftime("%d/%m/%Y")
        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)

        request_body = json.dumps({
            "name": todaysDate + "- automated via python",
            "description": "side project by ashley zhang. This playlist was built using nothing but python!",
            "public": True
        })

        response = requests.post(query, data=request_body, headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()
        return response_json["id"]

    def add_to_playlist(self):
        self.new_playlist_id = self.create_playlist()
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.trackList)

        response = requests.post(query, headers= {"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})

    def callRefresh(self):
        refreshCaller = refresh()
        self.spotify_token = refreshCaller.refresh()
        self.getTracks()

    def findArtistID(self, artist):
        query = "https://api.spotify.com/v1/search?q=artist%3A{}&type=artist&limit=1".format(artist)
        response = requests.get(query, headers= {"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
        return response.json()["artists"]["items"][0]["id"]

    def getArtists(self):
        artists = []
        artist_ids = []
        print('Input an artist name or "done" when finished')
        while True:
            userInput = input("Enter an artist name: ")
            if userInput == "done":
                print("The artists you have chosen are: ")
                for artist in artists:
                    print(artist)
                break
            userInput = userInput.replace(" ", "%20")
            artists.append(userInput)

        for artist in artists:
            artist_ids.append(self.findArtistID(artist))

        return artist_ids


    def getTopTrack(self, artistID):
        query = "https://api.spotify.com/v1/artists/{}/top-tracks?market=ES".format(artistID)
        response = requests.get(query, headers={"Content-Type": "application/json",
                                                "Authorization": "Bearer {}".format(self.spotify_token)})
        return response.json()["tracks"][0]["uri"]

    def getTracks(self):
        ids = self.getArtists()
        for artistID in ids:
            self.trackList += (self.getTopTrack(artistID) + ",")

        self.trackList = self.trackList[:-1]
        self.add_to_playlist()


#START
a = saveSongs()
a.callRefresh()




