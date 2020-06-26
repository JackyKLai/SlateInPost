import ffmpeg
import os


def convert_one_file(file, savePath):
    _, name = os.path.split(file)
    name = name[:name.find(".")]
    outName = savePath + "/" + name + ".wav"
    stream = ffmpeg.input(file)
    stream = ffmpeg.output(stream, outName)
    ffmpeg.run(stream)
    return outName


def change_path(files, newPath):
    result = []
    for file in files:
        _, name = os.path.split(file)
        name = name[:name.find(".")]
        result.append(newPath + "/" + name + ".wav")
    return result


