# importing libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from moviepy.editor import VideoFileClip


# creating object for speech recognition
r = sr.Recognizer()

# Function which splits given audio in to chunks by sentences
def break_chunks(path):
  
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  

    # split audio sound where silence is 500 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-14,
        keep_silence=500,
    )

    # create a directory to store the audio chunks
    folder_name = "audio-chunks"

    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    # process each chunk 
    # export audio chunk and save it in
    # the `folder_name` directory.
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

    return chunks

# Function to convert the audio file to wav file
def convert_to_wav(val):
    sound = AudioSegment.from_wav("static/"+val+".wav")
    sound = sound.set_channels(1)
    sound.export("static/path.wav", format="wav")

# # Downloading given youtube video for processing
# def download_video(link):

#     link_split = link.split('/')
#     end = link_split[3]

#     ydl_opts = {'quiet': True}
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([link])
#         info_dict = ydl.extract_info(link, download=False)
#         video_title = info_dict.get('title', None)
#         filename = ydl.prepare_filename(info_dict)

#     return video_title , end , filename

# def convert_to_mp4(val):
#     clip = VideoFileClip(val+".mkv")
#     clip.write_videofile(val+".mp4" , verbose = False ,logger= None)


def convert_video_to_audio_ffmpeg(video_file):
    # Insert Local Video File Path
    clip = VideoFileClip("static/"+video_file+".mp4")

    # Insert Local Audio File Path
    clip.audio.write_audiofile("static/"+video_file+".wav")



#adjust target amplitude
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

