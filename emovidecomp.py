import subprocess

def call_command(command):
    subprocess.Popen(command.split(' '))

# cut the movie
# call_command("ffmpeg -i D://Nick//Downloads//TV-Movies//Movies//Star_Wars//Star.Wars.Episode.IV.A.New.Hope.1977.mkv -ss 00:32:40 -to 00:33:11 -async 1 cut.mp4")

# transform movie into frames
# works
call_command("ffmpeg -i cut.mp4 -vf fps=10 D://Nick//Documents//School//NEU//Personal//Personal_Workspace//Emovi//frames//out%09d.png")





# recompile images into movie
# way faster than original
call_command("ffmpeg -framerate 10 -i D://Nick//Documents//School//NEU//Personal//Personal_Workspace//Emovi//frames//out%09d.png -c:v libx264 -r 30 -pix_fmt yuv420p newEmovi.mp4")
# call_command("ffmpeg -framerate 1 -i D://Nick//Documents//School//NEU//Personal//Personal_Workspace//Emovi//frames//out%09d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p newEmovi.mp4")

# subprocess.Popen(["C://Program Files//VideoLAN//VLC//vlc.exe", "newEmovi.mp4"])
