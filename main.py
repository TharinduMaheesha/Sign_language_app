import video_to_audio as audio
import audio_to_text as text
import text_emotion as text2
from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy.editor as mp

import os
from pytube import YouTube


def mainFunction(link):
        
    yt = YouTube(link)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download("static")
    val = yt.title

    audio.convert_video_to_audio_ffmpeg(val)
    audio.convert_to_wav(val)
    audio_chunks = audio.break_chunks("static/path.wav")

    final_text , test= text.test(audio_chunks)

    text_emotions = list()

    for i in test:
        emo = text2.detect_emotion(i)
        text_emotions.append(emo)

    facial_emotions = dict()

    final_emotion = list()
    for i in range(1,len(audio_chunks)+1):
        index = i-1

        positive = (text_emotions[index][0])
        negative = (text_emotions[index][1])
        neutral = (text_emotions[index][2])

        final_emotion.append([positive , negative , neutral])


    emotion_index = list()
    for i in final_emotion:
        max_index = i.index(max(i))
        if max_index == 0:
            emotion_index.append("positive")
        elif max_index == 1:
            emotion_index.append("negative")
        else:
            emotion_index.append("neutral")

    import text_to_SSL as SSL
    SSL_text = list()

    for i in test:
        parsed = SSL.parse_text(i)
        lemmatized = SSL.word_lemmatization(parsed)
        tokenized = SSL.word_tokenization(lemmatized)
        SSL_text.append(tokenized)
        print(tokenized)
        
    for i in range(0,len(emotion_index)):
        if "field" not in SSL_text[i] and "empti" not in SSL_text[i]:
            print("Emotion : " + emotion_index[i] + " --- text : " , SSL_text[i])
            print(" ")


    try:
        os.remove("my_concatenation.mp4")
    except:
        pass

    path = "videos"
    arg_array=[]

    for i in range(0,len(emotion_index)):
        for tex in SSL_text[i]:
            arg_array.append(VideoFileClip(path+"/"+emotion_index[i]+"/"+tex+".mp4"))
            print(tex+".mp4")

    print(arg_array[0])
    final_clip = concatenate_videoclips(arg_array , method='compose')
    final_clip.write_videofile("static/my_concatenation.mp4")

    return val