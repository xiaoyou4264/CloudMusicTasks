import random
import time

from task.publishMlog import recommended_song_ids


def start(user, task={}):
    music = user.music

    if task.get('taskId') == '10795676':
        share_song(user, task)
        return

    resp = music.daily_task(3)
    if resp['code'] == 200:
        user.taskInfo(task['taskName'], '分享成功')
    else:
        user.taskInfo(task['taskName'], user.errMsg(resp))


def share_song(user, task):
    music = user.music
    records = music.play_record(user.uid, time_type=1).get('weekData') or []
    song_ids = [row['song']['id'] for row in records if (row.get('song') or {}).get('id')]
    song_ids = song_ids or recommended_song_ids(music)
    if not song_ids:
        user.taskInfo(task['taskName'], '没有可用于分享的歌曲')
        return

    song_id = random.choice(song_ids)
    resp = music.yunbei_click_task(10795676)
    if resp.get('code') != 200 or resp.get('data') is not True:
        user.taskInfo(task['taskName'], '分享任务未启动：' + user.errMsg(resp))
        return
    time.sleep(3)

    resp = music.song_share_trigger(song_id, 'wxsession')
    if resp.get('code') != 200 or resp.get('data') is not True:
        resp = music.song_share_trigger(song_id, 'copylink')
    if resp.get('code') != 200 or resp.get('data') is not True:
        user.taskInfo(task['taskName'], '分享未触发：' + user.errMsg(resp))
        return
    time.sleep(3)

    resp = music.song_share_progress(song_id)
    if resp.get('code') != 200:
        user.taskInfo(task['taskName'], '分享进度上报失败：' + user.errMsg(resp))
        return
    time.sleep(3)
    status = '已确认完成' if user.yunbei_task_completed(task['taskId']) else '已上报，网易云暂未标记完成'
    user.taskInfo(task['taskName'], status)
