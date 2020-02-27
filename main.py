import os

import srt # pip install srt
import glob
import argparse

import scipy.io.wavfile

parser = argparse.ArgumentParser()
parser.add_argument('--root',default='./',
                    help='Root directory containing .srt files.')
args = parser.parse_args()


class SpeechDetector():

    def __init__(self, args):
        # glob.iglob returns an iterator instead of glob.glob which returns a list.
        self.SRT_ROOT = args.root
        self.iterator = glob.iglob(os.path.join(self.SRT_ROOT,'*.srt'),recursive=True)

    def split_speech(self):

        for file in self.iterator:

            srtFile = open(file) # Open srt file. E.g ".../fileName.srt"
            fileName = (file.split('.')[0]).split('/')[-1] # Just file name. E.g "fileName"
            wavFileName = file.split('.')[0] + '.wav' # Get wav file path # E.g ".../fileName.wav"

            if not os.path.exists(os.path.join('./split_speech',fileName)):
               os.makedirs(os.path.join('./split_speech',fileName)) # Make directory in work directory


            _rate, _stream = scipy.io.wavfile.read(wavFileName) # Open wav file

            subtitleGenerator = srt.parse(srtFile)
            subtitles=list(subtitleGenerator)

            tranScript = open(os.path.join('./split_speech',fileName,fileName+'.trans.txt'),'w')

            for i,_subtitles in enumerate(subtitles):

                _content = _subtitles.content
                _content = _content.replace('-','').replace('\n',' ') # Cleaning

                # IMPORTANT: Microseconds are important!!!
                _start = _subtitles.start.seconds + _subtitles.start.microseconds*1e-6
                _end = _subtitles.end.seconds + _subtitles.end.microseconds*1e-6
                _startFrame = int(_rate * _start) # Start frame index
                _endFrame = int(_rate * _end) # End frame index

                subStream = _stream[_startFrame:_endFrame]
                subFileName = fileName +'-'+ str(i) # E.g "fileName-n"
                _savePath = os.path.join('./split_speech',fileName, subFileName +'.wav')
                scipy.io.wavfile.write(_savePath, _rate, subStream)

                tranScript.write(subFileName + ' ' + _content + '\n')

            srtFile.close()
            tranScript.close()
            exit()

def main():
    sd = SpeechDetector(args);
    sd.split_speech()

if __name__== main():
    main()
