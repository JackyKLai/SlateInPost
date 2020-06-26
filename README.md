# SlateInPost
Audio syncing assistance for film/video editors with Python's SpeechRecognition

## How It Works
SlateInPost transcribes all your media files and compares them, giving you a rough idea of which audio/video clips contain similar contents.
It uses a Python package called [SpeechRecognition](https://pypi.org/project/SpeechRecognition/), which requires all media files to be in the .wav format. It is recommended that you convert your files to the supported format in advance, but SlateInPost does provide a conversion option that depends on the installation of [FFmpeg](https://ffmpeg.org/).

## Usage
![UI](https://github.com/JackyKLai/SlateInPost/blob/master/UI.jpg | width=100)
1. To start, click on the **Import Media Files** button and select your files.
2. SlateInPost outputs a .txt file with the information it collected. Click on the **Save output to...** button to let it know where to save this file.
3. Let SlateInPost know how similar the files need to be in order for them to be associated. You can choose which speech recognition engine to use. Options include Sphinx, Google Speech Recognition, [Wit.ai](http://wit.ai/), [Bing](https://www.microsoft.com/cognitive-services/en-us/speech-api), [Houndify](https://houndify.com/) and [IBM](http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/speech-to-text.html). The first two are completely free and require no API keys/Account info. As mentioned above, you can also ask SlateInPost to convert your files to .wav for you, but make sure you have FFmpeg installed properly. If you choose to use this conversion option, you can also decide whether these new .wav files should be deleted or not.
4. Action! ;) Audio transcription takes quite a while to complete. Maybe take that time to go through your footage clip by clip like a good editor should!
