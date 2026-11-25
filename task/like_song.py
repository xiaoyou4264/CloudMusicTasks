import random

from task._yunbei_toggle import apply_task, configured_id


def random_song(music, liked_ids):
    response = music.daily_recommended_songs()
    songs = (response.get('data') or {}).get('dailySongs') or []
    candidates = [row['id'] for row in songs if row.get('id') and row['id'] not in liked_ids]
    if candidates:
        return random.choice(candidates)

    for playlist in music.personalized_playlist(limit=10):
        response = music.playlist_detail(playlist['id'])
        songs = (response.get('playlist') or {}).get('tracks') or []
        candidates = [row['id'] for row in songs if row.get('id') and row['id'] not in liked_ids]
        if candidates:
            return random.choice(candidates)
    return None


def start(user, task):
    music = user.music
    name = task['taskName']
    try:
        song_id = configured_id(task.get('songId'))
    except ValueError as error:
        user.taskInfo(name, str(error))
        return

    def liked_song_ids():
        return music.liked_song_ids(user.uid)

    liked = liked_song_ids()
    if liked is None:
        user.taskInfo(name, '无法确认当前红心列表')
        return
    if song_id is None or song_id in liked:
        song_id = random_song(music, liked)
    if song_id is None:
        user.taskInfo(name, '推荐歌曲中没有可用的未红心歌曲')
        return

    apply_task(user, task, song_id, music.set_song_like, liked_song_ids,
               task.get('unlikeAfterTask', True), '取消红心')
