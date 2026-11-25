import time


def configured_id(value):
    if value is None:
        return None
    raw = str(value)
    if not raw.isascii() or not raw.isdecimal() or int(raw) <= 0:
        raise ValueError('ID 必须为正整数或 null')
    return int(raw)


def apply_task(user, task, item_id, set_state, current_ids, undo, undo_name):
    name = task['taskName']
    response = set_state(item_id, True)
    if response.get('code') != 200:
        user.taskInfo(name, '操作失败：' + user.errMsg(response))
        return

    completed = False
    try:
        for _ in range(5):
            time.sleep(2)
            if user.yunbei_task_completed(task['taskId']):
                completed = True
                break
        if completed and undo and user.user_setting.get('yunbei_claim_rewards', True):
            user.get_yunbei(task_name=name)
    finally:
        if undo:
            for _ in range(2):
                set_state(item_id, False)
                ids = current_ids()
                if ids is not None and item_id not in ids:
                    user.taskInfo(name, f'ID {item_id} 已{undo_name}')
                    break
            else:
                user.taskInfo(name, f'ID {item_id} 未能确认已{undo_name}')

    status = '已确认完成' if completed else '已提交，网易云暂未确认完成'
    user.taskInfo(name, f'{status}（ID {item_id}）')
