from flask import Flask, render_template, request
from pytube import YouTube  
import os
from pathlib import Path
from history import getHistory, loadHistory

app = Flask(__name__)
global yt

@app.route("/")
def home():
    return render_template("index.html")


def vid_options():
    yt_link = request.form['yt-link']
    try:  
        yt = YouTube(yt_link)  
    except:  
        print("Connection Error") #to handle exception  
    # filters out all the files with "mp4" extension  
    mp4files = yt.streams.filter(progressive=True)
    #hr = yt.streams.filter(res="1080p").first()
    #res_high = list((hr.resolution, hr.itag))
    #res = [(stream.resolution, stream.itag) for stream in mp4files if stream.resolution != None]
    #res.append(res_high)
    #res_tag = dict(res)
    abr_itag_dict = {stream.resolution: stream.itag for stream in mp4files if stream.resolution != None}

    ftype = [stream.mime_type for stream in mp4files]
    #ftype.append(hr.mime_type)
    
    #print(yt.streams.file_type)
    return render_template("index.html", video = yt_link, mime_type = ftype, 
                        reslist = abr_itag_dict, title=yt.title, 
                        thumb = yt.thumbnail_url, media_type='video')

    
def mp3_options():
    youtube_link = request.form['yt-link']
    try:  
        youtube = YouTube(youtube_link)  
    except KeyError:  
        print("Invalid YouTube Link Provided") #to handle exception if the link is not valid

    # filters out all the files with "mp4" extension  
    audio_streams = youtube.streams.filter(only_audio = True)

    # filter out streams with mime_type not equal to "audio/webm" and create a dictionary with abr and itag
    abr_itag_dict = {stream.abr: stream.itag for stream in audio_streams if stream.mime_type != "audio/webm"}

    # get list of mime_types from audio streams
    mime_types = [stream.mime_type for stream in audio_streams]

    return render_template("index.html", video=youtube_link, mime_type=mime_types, 
                        reslist=abr_itag_dict, title=youtube.title, 
                        thumb=youtube.thumbnail_url, media_type='audio')


@app.route("/download", methods=['POST', 'GET'])
def download():
    vid_url = request.form.get("vid_url")
    itag = request.form.get("itag")
    media_type = request.form.get("media_type")
    media_title = request.form.get("media_title")
    yt = YouTube(vid_url)
    stream = yt.streams.get_by_itag(itag)
    path_to_download = str(os.path.join(Path.home(), 'Downloads'))
    f = stream.download(path_to_download)
    if(media_type == 'audio'):
        base, ext = os.path.splitext(f) 
        new_file = f"{base}.mp3"
        os.rename(f, new_file) 
    getHistory(media_title, media_type)
    return render_template('index.html', msg=f'File downloaded Successfully. Check your "{path_to_download}" folder')


@app.route("/history")
def history():
    return loadHistory()

#@app.route("/mp3_options", methods=['POST', 'GET'])
@app.route("/check", methods=['POST', 'GET'])
def check():
    if request.form['btn-opt'] == 'video':
        return vid_options()
    else:
        return mp3_options()
     

if __name__ == "__main__":
    app.run(debug = False, host='0.0.0.0')
