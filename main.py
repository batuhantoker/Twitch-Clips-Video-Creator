import os
import random
import moviepy.editor as mp
import json, random, shutil

# Set global constants
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
MUSIC_DIR = os.path.join(os.getcwd(), 'music')
BG_DIR = os.path.join(os.getcwd(), 'background')
CODEC_STYLE = 'libx264'

def clear_old_files():
    """Remove old .mov and .mp4 files in the current directory."""
    current_dir = os.getcwd()
    for item in os.listdir(current_dir):
        if item.endswith((".mov", ".mp4")):
            os.remove(os.path.join(current_dir, item))

def video_download(username, max_clip):
    """
    Download Twitch clips for a given username and return file names and titles.

    Args:
        username (str): Twitch username.
        max_clip (int): Maximum number of clips to download.

    Returns:
        file_names (list): List of downloaded video file names.
        titles (list): List of clip titles.
    """
    os.system(f'cd {os.getcwd()}')
    print(f'File download username: {username}')
    
    command = f'python3 twitch-dl.2.1.3.pyz clips {username} --download --limit {max_clip} --period all_time'
    os.system(command)

    command2 = f'python3 twitch-dl.2.1.3.pyz clips {username} --json --limit {max_clip} --period all_time'
    stream = os.popen(command2)
    clip_list_json = stream.read()

    # Parse JSON data
    clip_list = json.loads(clip_list_json)

    # Extract clip titles and create file names
    titles = []
    file_names = []
    for clip in clip_list:
        title = ''.join(filter(lambda char: char.isalnum() or char.isspace(), clip['title']))
        titles.append(title)
        file_names.append(f'{title}.mp4')
        print(f'{len(titles) - 1}: {file_names[-1]}')

    # Rename downloaded files based on titles
    files = os.listdir('.')
    mp4_files = [f for f in files if f.endswith('.mp4')]
    mp4_files.sort(key=lambda x: os.stat(x).st_ctime)
    
    for i, old_name in enumerate(mp4_files):
        new_name = file_names[i]
        print(f'Renaming: {new_name} <- {old_name}')
        os.rename(old_name, new_name)

    return file_names, titles

def select_random_mp3():
    """Select a random MP3 file from the 'music' directory."""
    mp3_files = [f for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3')]
    return random.choice(mp3_files)

def select_random_png():
    """Select a random PNG file from the 'background' directory."""
    png_files = [f for f in os.listdir(BG_DIR) if f.endswith('.png')]
    return random.choice(png_files)

def generate_text(intro_text):
    """
    Generate an intro video with text and random background music.

    Args:
        intro_text (str): Text to display in the intro video.
    """
    text_clip = mp.TextClip(intro_text, font="Lane", fontsize=120, color=random.choice(mp.TextClip.list('color')))
    text_clip = text_clip.set_duration(10)
    text_clip = text_clip.on_color(size=(1920, 1080), color=(0, 0, 0))

    audio_clip = mp.AudioFileClip(os.path.join(MUSIC_DIR, select_random_mp3())).subclip(0, 10)

    video_clip = mp.CompositeVideoClip([text_clip])
    video_clip.audio = mp.CompositeAudioClip([audio_clip])

    video_clip.write_videofile("intro.mp4", fps=24, codec=CODEC_STYLE)

def transition(title, i):
    """
    Create a transition video with text and random background music.

    Args:
        title (str): Transition title.
        i (int): Video index.
    """
    image_clip = mp.ImageClip(os.path.join(BG_DIR, select_random_png()))
    text_clip = mp.TextClip(txt=title.upper(),
                            size=(.8 * image_clip.size[0], 0),
                            font="Lane",
                            color="black")
    audio_clip = mp.AudioFileClip(os.path.join(MUSIC_DIR, select_random_mp3())).subclip(0, 3)
    text_clip = text_clip.set_position('center')
    im_width, im_height = text_clip.size
    color_clip = mp.ColorClip(size=(int(im_width * 1.1), int(im_height * 1.4)),
                              color=(0, 255, 255))
    color_clip = color_clip.set_opacity(.6)
    clip_to_overlay = mp.CompositeVideoClip([text_clip, color_clip])
    clip_to_overlay = clip_to_overlay.set_position('center')
    final_clip = mp.CompositeVideoClip([image_clip, text_clip])
    final_clip.audio = audio_clip
    final_clip.set_duration(3).write_videofile(f"{i}.mp4", fps=24, codec=CODEC_STYLE)

def add_text(filename, title, i):
    """
    Add text overlay to a video file.

    Args:
        filename (str): Input video filename.
        title (str): Title text to overlay.
        i (int): Video index.
    """
    clip = mp.VideoFileClip(filename)
    final = mp.CompositeVideoClip([clip])
    final.subclip(0, int(clip.duration)).write_videofile(f"{i}.mp4", fps=24, codec=CODEC_STYLE)

def add_background(filename, i):
    """
    Add background music to a video file.

    Args:
        filename (str): Input video filename.
        i (int): Video index.
    """
    video = mp.VideoFileClip(filename)
    additional_audio = mp.AudioFileClip(os.path.join(MUSIC_DIR, select_random_mp3()))
    additional_audio = additional_audio.set_duration(video.duration)
    new_audio = moviepy.audio.fx.all.volumex(additional_audio, 0.15)
    audio = mp.CompositeAudioClip([video.audio, new_audio])
    video = video.set_audio(audio)
    video.write_videofile(f"{i}.mp4", fps=24, codec=CODEC_STYLE)

def main():
    # Define a list of streamer usernames
    streamers = [
        'pokimane', 'juansguarnizo', 'sodapoppin', 'myth', 'tommyinnit', 'slakun10',
        'timthetatman', 'nickmercs', 'riot games', 'sypherpk', 'elmariana', 'dream',
        'summit1g', 'elspreen', 'amouranth', 'alanzoka', 'esl_csgo', 'clix', 'arigameplays',
        'mongraal', 'fortnite', 'elded', 'quackity', 'loltyler1', 'bugha', 'tubbo',
        'georgenotfound', 'montanablack88', 'moistcr1tikal', 'robleis', 'dakotaz',
        'wilbursoot', 'drlupo', 'fresh', 'ranboolive', 'nickeh30', 'daequanwoco',
        'philza', 'squeezie', 'sykkuno', 'benjyfishy', 'slakun10'
    ]

    # Clear old files in the current directory
    clear_old_files()

    max_clip = 20
    for username in streamers:
        file_names, titles = video_download(username, max_clip)
        generate_text(username + '\n best moments')
        
        for i, j in enumerate(file_names):
            title = titles[i]
            print(j, title)
            transition(title, 2 * i)
            add_text(j, title, 2 * i + 1)

        # Concatenate videos and create a video list
        files = [f"{i}.mp4" for i in range(2 * len(file_names))]
        files.insert(0, "intro.mp4")
        with open('videolist.txt', 'w') as f:
            for item in files:
                f.write(f'file \'{item}\'\n')

        # Run FFmpeg to concatenate videos
        os.system(f'ffmpeg -f concat -i videolist.txt -c copy output.mp4')

        # Rename and move the output file
        shutil.move('output.mp4', os.path.join(OUTPUT_DIR, f'{username}.mp4'))

        # Clear old files again
        clear_old_files()

if __name__ == '__main__':
    main()
