#### main.py

from ytspace.funcs import *

print("""
    Hi and Welcome to YT SPACE!
    """)

options = ("""
    Select the action you want to perform:
    
    1. Download Video           5. Download Music
    2. Show Downloaded Videos   6. Show Downloaded Music
    3. Update Video Info        7. Update Music Info
    4. Delete Video             8. Delete Music

    0. Quit                     
    """)

media_type, media_type_str, table_name, audio = "","","",""

def init_database_schema():
    query("CREATE DATABASE IF NOT EXISTS yt_space")
    query("USE yt_space")

    path_music = get_download_path(0)
    path_videos = get_download_path(1)
    query(table_type)
    query(type_init.format(path_music, path_videos))

    query(table_media)
    query(table_music)
    query(table_videos)

def menu():
    global media_type, media_type_str, table_name, audio

    print("    Enter (0-8): ", end = "")

    action = input()

    if action.isdigit(): pass
    else:
        print("    Invalid input! Please try again.")
        menu(); return

    action = int(action)

    if action in range(9): print("")
    else:
        print("    Please enter a number between 0 and 8.")
        menu(); return

    media_type, media_type_str, table_name, audio = (0, "Music", "music", True) \
                    if action in (5,6,7,8) else (1, "Videos", "videos", False)
    
    
    if action in (1,5): download(media_type)
    elif action in (2,6): display(media_type)
    elif action in (3,7): update(media_type)
    elif action in (4,8): delete(media_type)

    elif action == 0: print("=-"*50+"="); exit()

def back_to_menu():
    print("\n", "══"*45, sep="")
    choice = input("Press enter to go back to menu or enter 'exit'/'e' to exit: ")
    print("══"*45)
    
    if choice in ("e", "exit"): exit()
    else: print(options); menu()

def download(media_type):    
    yt_link = input("    Enter the YT Video Link: ")
    if yt_link in ("e","exit"): back_to_menu(); return

    try:
        media_id, title = yt_add(yt_link, audio)
    except pytube_err.VideoUnavailable:
        print("    This YT video does not exist. Enter a valid link.")
        download(media_type); return
    except pytube_err.RegexMatchError:
        print("    Invalid YT link. Please check and try again.")
        download(media_type); return

    print(f"> YT {media_type_str} Downloaded! | Title: {title} \n> Media ID: {media_id}")

    back_to_menu()

def display(media_type):
    print(f"""
    Enter the Media ID of the {media_type_str} you want to be displayed
    or enter '*' to display all of the {table_name}: """, end = "")

    media_id = input()
    if media_id in ("e","exit"): back_to_menu(); return

    if media_id == "*":
        query(display_all_video_music.format(table_name))
    else:
        try:
            if int(media_id):
                query(display_video_music.format(table_name, media_id))
        except ValueError:
            print("    Invalid input! Please check and try again.")
            display(media_type); return
            
    path_len = len(get_download_path(media_type))
    results = [i for i in cursor]
	
    try: max_title_len = max([len(i[1]) for i in results])
    except: max_title_len = 30

    print(f"\n    {table_name.capitalize()} found:")

    print(f"""    ╒════╤════╤═{'═'*max_title_len}═╤═{'═'*21}═╤═{'═'*path_len}═╕
    │SNo.│ ID │ Title{' '*(max_title_len-5)} │ Date & Time{' '*10} │ Path{' '*(path_len-4)} │
    ├────┼────┼─{'─'*max_title_len}─┼─{'─'*21}─┼─{'─'*path_len}─┤""")
    
    for i, rec in enumerate(results):
        print("""    │ {:^2} │ {:^2} │ {:<}{} │ {:^21} │ {:<} │""".format(
            i+1,
            rec[0],
            rec[1], " "*(max_title_len - len(rec[1])),
            str(rec[3]) + " | " + str(rec[4]),
            rec[2]
        ))
    
    print(f"    ╘════╧════╧═{'═'*max_title_len}═╧═{'═'*21}═╧═{'═'*path_len}═╛")
    
    back_to_menu()

def update(media_type):
    media_id = input(f"    Enter the Media ID of the {media_type_str.lower()} you want to update: ")
    if media_id in ("e","exit"): back_to_menu(); return
    new_title = input(f"    Enter the new title for the selected {media_type_str.lower()}: ")
    if new_title in ("e","exit"): back_to_menu(); return

    try:
        query(update_title.format(table_name, new_title, media_id))
    except mysql.errors.ProgrammingError:
        print("    Invalid input! Please check and try again.")
        update(media_type); return

    print(f"    Title of the {media_type_str.lower()} with Media ID {media_id} updated.")
    
    back_to_menu()

def delete(media_type):
    media_id = input("    Enter the Media ID: ")
    if media_id in ("e","exit"): back_to_menu(); return

    yt_delete(media_id)

    print(f"    Deleted Media with ID {media_id}")
    
    back_to_menu()

init_database_schema()
print(options); menu()
'''
f"""    +----+----+-{'-'*max_title_len}-+-{'-'*21}-+-{'-'*path_len}-+
    |SNo.| ID | Title{' '*(max_title_len-5)} | Date & Time{' '*10} | Path{' '*(path_len-4)} |
    +----+----+-{'-'*max_title_len}-+-{'-'*21}-+-{'-'*path_len}-+""")

    for i, rec in enumerate(results):
        print("""    | {:^2} | {:^2} | {:<}{} | {:^21} | {:<} |""".format(
            i+1,
            rec[0],
            rec[1], " "*(max_title_len - len(rec[1])),
            str(rec[3]) + " | " + str(rec[4]),
            rec[2]
        ))

    print(f"    +----+----+-{'-'*max_title_len}-+-{'-'*21}-+-{'-'*path_len}-+"

f"""    ┏━━━━┳━━━━┳━{'━'*max_title_len}━┳━{'━'*21}━┳━{'━'*path_len}━┓
    ┃SNo.┃ ID ┃ Title{' '*(max_title_len-5)} ┃ Date & Time{' '*10} ┃ Path{' '*(path_len-4)} ┃
    ┣━━━━╋━━━━╋━{'━'*max_title_len}━╋━{'━'*21}━╋━{'━'*path_len}━┫""")
    
    for i, rec in enumerate(results):
        print("""    ┃ {:^2} ┃ {:^2} ┃ {:<}{} ┃ {:^21} ┃ {:<} ┃""".format(
            i+1,
            rec[0],
            rec[1], " "*(max_title_len - len(rec[1])),
            str(rec[3]) + " | " + str(rec[4]),
            rec[2]
        ))
    
    print(f"    ┗━━━━┻━━━━┻━{'━'*max_title_len}━┻━{'━'*21}━┻━{'━'*path_len}━┛"

f"""    ╒════╤════╤═{'═'*max_title_len}═╤═{'═'*21}═╤═{'═'*path_len}═╕
    │SNo.│ ID │ Title{' '*(max_title_len-5)} │ Date & Time{' '*10} │ Path{' '*(path_len-4)} │
    ├────┼────┼─{'─'*max_title_len}─┼─{'─'*21}─┼─{'─'*path_len}─┤""")
    
    for i, rec in enumerate(results):
        print("""    │ {:^2} │ {:^2} │ {:<}{} │ {:^21} │ {:<} │""".format(
            i+1,
            rec[0],
            rec[1], " "*(max_title_len - len(rec[1])),
            str(rec[3]) + " | " + str(rec[4]),
            rec[2]
        ))
    
    print(f"    ╘════╧════╧═{'═'*max_title_len}═╧═{'═'*21}═╧═{'═'*path_len}═╛"

 '''
