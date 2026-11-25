import time


MAX_SONGS = 10
LISTEN_SECONDS = 31


def progress(music, task_id):
    response = music.yunbei_task()
    if response.get('code') != 200:
        return None
    for row in response.get('data') or []:
        if str(row['taskId']) == task_id and row.get('taskPointDetail'):
            stage = row['taskPointDetail'][0]
            current, target, reward = (stage.get(key) for key in ('progressRate', 'sumTarget', 'worth'))
            if all(isinstance(value, int) and value >= 0 for value in (current, target, reward)) and target and reward:
                return current, min(target, MAX_SONGS), reward
            return None
    return None


def start(user, task):
    music = user.music
    name = task['taskName']
    task_id = task['taskId']
    state = progress(music, task_id)
    if state is None:
        user.taskInfo(name, '无法读取任务进度')
        return
    current, target, reward = state
    if current >= target:
        user.taskInfo(name, f'今日进度 {current}/{target}，已达上限')
        return

    recommendations = music.yunbei_indie_songs(MAX_SONGS)
    if recommendations.get('code') != 200:
        user.taskInfo(name, '获取推荐失败：' + user.errMsg(recommendations))
        return
    song_ids = list(dict.fromkeys(row['songId'] for row in recommendations.get('data') or [] if row.get('songId')))
    if not song_ids:
        user.taskInfo(name, '没有可用的推荐歌曲')
        return

    details = music.songs_detail(song_ids)
    albums = {row['id']: row['al']['id'] for row in details.get('songs') or [] if (row.get('al') or {}).get('id')}
    if details.get('code') != 200 or not albums:
        user.taskInfo(name, '无法读取推荐歌曲的专辑信息')
        return

    initial = current
    for song_id in song_ids[:MAX_SONGS]:
        if song_id not in albums:
            continue
        time.sleep(LISTEN_SECONDS)
        distribution = music.yunbei_indie_distribution(reward)
        if distribution.get('code') != 200 or distribution.get('data') is not True:
            user.taskInfo(name, '云贝分配接口未确认：' + user.errMsg(distribution))
            break
        time.sleep(2)
        result = music.yunbei_indie_listen(song_id, albums[song_id])
        if result.get('code') != 200 or result.get('data') is not True:
            user.taskInfo(name, '听歌进度上报未确认：' + user.errMsg(result))
            break
        time.sleep(2)
        state = progress(music, task_id)
        if state is None:
            user.taskInfo(name, '上报后无法回查进度')
            break
        current, target, reward = state
        print(f'{name}：网易云进度 {current}/{target}', flush=True)
        if current >= target:
            break

    user.taskInfo(name, f'网易云确认进度 {current}/{target}，本次增加 {current - initial} 首')
