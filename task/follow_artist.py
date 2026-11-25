import random

from task._yunbei_toggle import apply_task, configured_id


def random_artist(music, followed_ids):
    for offset in (0, 50, 100):
        response = music.top_artists(offset)
        if response.get('code') != 200:
            break
        artists = response.get('artists') or []
        candidates = [row['id'] for row in artists if row.get('id') and row['id'] not in followed_ids and not row.get('followed')]
        if candidates:
            return random.choice(candidates)
        if not response.get('more') or not artists:
            break
    return None


def start(user, task):
    music = user.music
    name = task['taskName']
    try:
        artist_id = configured_id(task.get('artistId'))
    except ValueError as error:
        user.taskInfo(name, str(error))
        return

    followed = music.followed_artist_ids()
    if followed is None:
        user.taskInfo(name, '无法确认当前关注列表')
        return
    if artist_id is None or artist_id in followed:
        artist_id = random_artist(music, followed)
    if artist_id is None:
        user.taskInfo(name, '热门歌手中没有可用的未关注歌手')
        return

    apply_task(user, task, artist_id, music.set_artist_follow, music.followed_artist_ids,
               task.get('unfollowAfterTask', True), '取关')
