import SER_prediction as SER
import video_to_audio as audio
import audio_to_text as text
import video_emotion as video
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
    audio.break_video(val+".mp4")
    audio_chunks = audio.break_chunks("static/path.wav")

    for i in range (1,len(audio_chunks)+1):
        frame = 0
        video.FrameCapture("video/"+str(i)+".mp4" , i)

    dictionary = dict()

    for i in range (1,len(audio_chunks)+1):
        happy = 0
        sad = 0
        neutral = 0
        count = 0
        for filename in os.listdir("images/"+str(i)):
            count += 1
            result = video.detect_emotion("images/"+str(i)+"/"+filename)
            happy+= result['emotion']['happy']
            sad += result['emotion']['sad']
            neutral += result['emotion']['neutral']

        if count == 0:
            happy = 0
            sad = 0
            neutral = 0
        else:

            positive = happy / count
            negative = sad / count
            neutral = neutral / count
        
        dictionary[str(i)] = [positive , negative , neutral]

        print("Positive : " + str(positive) + " Negative : " + str(negative) + " Neutral : " + str(neutral))

    audio_emotions = SER.predict_emotion(audio_chunks)
    final_text , test= text.test(audio_chunks)

    text_emotions = list()

    for i in test:
        emo = text2.detect_emotion(i)
        text_emotions.append(emo)

    facial_emotions = dict()

    final_emotion = list()
    for i in range(1,len(audio_chunks)+1):
        index = i-1
        pos_aud = 0
        neg_aud = 0
        neu_aud = 0
        if audio_emotions[index] == "positive":
            pos_aud = 0.1
        elif audio_emotions[index] == "negative":
            neg_aud = 0.1
        else:
            neu_aud = 0.1

        positive = (dictionary[str(i)][0] * 0.4) + pos_aud + (text_emotions[index][0] * 40)
        negative = (dictionary[str(i)][1] * 0.4) + neg_aud + (text_emotions[index][1] * 40)
        neutral = (dictionary[str(i)][2] * 0.4) + neu_aud + (text_emotions[index][2] * 40)

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