import time


def start(user, task={}):
    music = user.music

    if task.get('taskId') == '6758460':
        resp = music.yunbei_click_task(6758460, task.get('subAction', ''), 'feizhu')
        if resp.get('code') != 200 or resp.get('data') is not True:
            user.taskInfo(task['taskName'], '浏览任务未启动：' + user.errMsg(resp))
            return
        time.sleep(16)
        status = '已确认完成' if user.yunbei_task_completed(task['taskId']) else '已触发，网易云暂未标记完成'
        user.taskInfo(task['taskName'], status)
        return

    resp = music.vipcenter_task_external(1)
    if resp['code'] == 200:
        user.taskInfo(task['taskName'], '浏览成功')
    else:
        user.taskInfo(task['taskName'], user.errMsg(resp))
