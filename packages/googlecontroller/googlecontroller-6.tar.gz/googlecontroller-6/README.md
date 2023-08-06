# googlecontroller
GITHUB EXCLUSIVE KNOWLEDGE FOR SERVE_MEDIA HERE
Library for Python 3.9+ to push text message or audio file with the Google Home.Originally made by - Thomas Deblock (@tdeblock) I have expanded most of the code quite a bit little of the original remains, but the idea came from Mr.Deblock.This is a sorta v2 for the googlehomepush module they made.

## Installation

finally a pypi!!!!!!!
```
pip install googlecontroller
```
## Depending On

PyChromeCast
Pyngrok


## How to use

``` python
from googlecontroller import GoogleAssistant
from googlecontroller.http_server import serve_file # for local files
host = "ip"
home = GoogleAssistant(host=host)
home.say("test")
home.play("http://www.hubharp.com/web_sound/BachGavotteShort.mp3, opentunnel = 0") # we are doing opentunnel as this is the first time doing it
home.play("http://www.hubharp.com/web_sound/BachGavotteShort.mp3) # you do this after the first opening

#When serving media NEVER USE A \ ONLY USE /
#when doing your first home.serve_media you have to include a 3rd variable, opentunnle!For that 1 first time you have to set it manually to a 0!
#opentunnel = 0
#YOU MUST USE A DELAY IF DOING MULTIPLE IN A ROW FINE TUNE AS YOU SEE FIT
#like this home.serve_media("YourMedia.mp3", "C:/Users/YOU!/Music/", opentunnel)
#**then never use that variable again**
home.serve_media("YourMedia.mp3", "C:/Users/YOU!/Music/") # 1st is the name of the media, second is the full path to media location!
home.volume(100)
home.volume(0)

```
### .say(text, speed,ignore, lang)

Push a message on Google home

- `text` is the test message to say
- `speed` is the rate of speed of the message ranges from 0.000+ as slowest to 1 as normal speed.
- `ignore` ignore if audio is playing and play it regardless if ignore=True and only play if not playing if ignore=False or is not specified. 
- `lang` the text language, default value is 'en' to change it have lang = 'language' as described in google translate en-Us, es (spanish), ect

### .play(url, ignore, contentType = 'audio/mp3'):

Push a sound to Google home
- `url` an audio file URL
- `ignore` ignore if audio is playing and play it regardless if ignore=True and only play if not playing.If ignore is not specified it will be set to False. 
- `contentType` the audio file content type

### .volume(volumelevel):
- `volumelevel` the volume level from 0-100 (must be a integer) Example: home.volume(5) or home.volume(volumelevel=5). If you want to take it as user input you can do home.volume(volumelevel=input()).



## Maintainers
- Dray-Cyber
