# SlateInPost
Audio syncing assistance for film/video editors with Python's SpeechRecognition

## How It Works
SlateInPost transcribes all your media files and compares them, giving you a rough idea of which audio/video clips contain similar contents.
It uses a Python package called [SpeechRecognition](https://pypi.org/project/SpeechRecognition/), which requires all media files to be in the .wav format. It is recommended that you convert your files to the supported format in advance, but SlateInPost does provide a conversion option that depends on the installation of [FFmpeg](https://ffmpeg.org/).

## Getting Started
**The app is still a work in progress, releases are for testing only.**
Releases are available [here](https://github.com/JackyKLai/SlateInPost/releases). You can also build it yourself with [PyInstaller](https://pypi.org/project/PyInstaller/).
To build the app, you will need [SpeechRecognition](https://pypi.org/project/SpeechRecognition/), [ffmpeg-python](https://pypi.org/project/ffmpeg-python/) and [PyQt5](https://pypi.org/project/PyQt5/).

## Usage
1. To start, click on the **Import Media Files** button and select your files.
2. SlateInPost outputs a .txt file with the information it collected. Click on the **Save output to...** button to tell it where the text file should be saved.
3. Let SlateInPost know how similar the files need to be in order for them to be associated. The minimum is set at 30%.
4. You can also choose which speech recognition engine to use. Options include Google Speech Recognition (free), [Wit.ai](http://wit.ai/), [Bing](https://www.microsoft.com/cognitive-services/en-us/speech-api), [Houndify](https://houndify.com/) and [IBM](http://www.ibm.com/watson/speech-to-text).
5. As mentioned above, you can also ask SlateInPost to convert your files to .wav for you, but make sure you have FFmpeg installed properly. If you choose to go with this conversion option, you can also decide whether these new .wav files should be deleted.
6. **Action!** ;) Audio transcriptions take quite a while to complete. Maybe take that time to go through your footage clip by clip like a good editor should!
