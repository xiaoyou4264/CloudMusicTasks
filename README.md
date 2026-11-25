# CloudMusicTasks · 网易云音乐自动任务

本仓库维护网易云音乐签到、云贝任务和推送功能，包含新版云贝接口适配。可从源码通过 [Docker Compose](#从本仓库构建并运行-docker-compose) 部署，或直接用 Python [本地运行](#三本地运行)。

## 功能

1. 签到领云贝
2. 自动完成云贝任务，并领取云贝
3. 打卡升级
4. 刷指定歌曲的播放量
5. 音乐人自动签到领取云豆
6. 音乐人自动完成任务，并领取云豆
7. 自动领取 vip 成长值
8. 多种[推送方式](#推送)
9. 支持多账号
10. 支持[腾讯云函数](#一部署到腾讯云函数) & [青龙面板](#二部署到青龙面板) & [本地运行](#三本地运行) & [docker 部署](#四使用docker部署)

### Docker 配置示例

| 状态 | 功能 |
| --- | --- |
| 已开启 | 每日签到、自动领取云贝、分享歌曲、浏览会员中心、探索小众歌曲、关注歌手、红心歌曲、访问商城、发布动态、发布 Mlog |
| 已关闭 | 打卡升级、指定歌单刷播放量、云贝推歌、音乐人任务及云豆领取、VIP 成长值及共享歌单、关注作者 |
| 账号与推送 | 单账号，使用 Server 酱推送到微信 |
| 执行时间 | 每天北京时间 08:30，容器启动和重启时只加载计划 |

表中的账号、推送和任务开关是一套部署示例。新部署从 [`config.example.json`](./config.example.json) 复制配置，再按需选择功能。

云贝子任务以网易云对该账号返回的任务列表为准。已经开启的访问商城、发布动态或发布 Mlog，只有在接口返回对应任务且任务可执行时才会运行。网易云返回的发布图文笔记、设置双人关系、完善个人资料目前尚未接入。

## 注意事项

- 示例配置中的 `follow` 默认开启，可在本机[关闭关注作者](#关注作者)。
- 反馈问题前，请先搜索[本仓库的 Issues](https://github.com/xiaoyou4264/CloudMusicTasks/issues)。
- 在本机 `config.json` 中填写账号 Cookie、密码和推送密钥。提交代码时使用 `config.example.json` 展示配置结构，凭据留在本机。
- 转载请注明出处，并保留原作者信息。
- 禁止将代码用于商业用途，包括打包售卖，收费代挂等。
- 为了账号安全考虑，请勿将账号密码交给他人代挂。

## 一、部署到腾讯云函数

### 开通服务

首次使用云函数，依次登录 [SCF 云函数控制台](https://console.cloud.tencent.com/scf) 和 [SLS 控制台](https://console.cloud.tencent.com/sls) 开通相关服务，确保账户下已开通服务并创建相应[服务角色](https://console.cloud.tencent.com/cam/role) **SCF_QcsRole、SLS_QcsRole**

> 注意！为了确保权限足够，获取这两个参数时不要使用子账户！此外，腾讯云账户需要[实名认证](https://console.cloud.tencent.com/developer/auth)。

### 获取密钥

在腾讯云[API 密钥管理](https://console.cloud.tencent.com/cam/capi)新建密钥，获取 SecretId 和 SecretKey

![Fork](./public/img/getsecret.png)

### 准备 GitHub 仓库

在自己有管理权限的仓库设置 Secrets。也可以从 [xiaoyou4264/CloudMusicTasks](https://github.com/xiaoyou4264/CloudMusicTasks) 创建自己的 fork 后继续。

![Fork](./public/img/fork.png)

### 创建 Secrets

打开部署所用仓库的 `Settings`。

![Settings](./public/img/settings.png)

在页面点击 `Secrets`，点击 `Actions`，然后点击 `New repository secret` 创建新的 secret。

![NewSecrets](./public/img/newsecrets.png)

| Name          | Value                     | 是否必填 |
| :------------ | :------------------------ | :------- |
| SECRET_ID     | 填写之前获取的 SecretId   | 必填     |
| SECRET_KEY    | 填写之前获取的 SecretKey  | 必填     |
| CRON          | 定时触发器的时间          | 选填     |
| FUNCTION_NAME | 自定义函数名              | 选填     |
| REGION        | 地域，默认为 ap-guangzhou | 选填     |

先填写先前获取的 SECRET_ID

![SECRET_ID](./public/img/secretid.png)

同理，填写先前获取的 SECRET_KEY

![SECRET_KEY](./public/img/secretkey.png)

CRON 默认为 `0 35 8 * * * *` 表示每天 8 点 35 分触发。如需更改，则如下图所示创建此 secret，。比如：`0 20 12 * * * *` 表示每天 12 点 20 分触发，`0 0 12,16 * * * *` 表示每天 12 点和 16 点各触发一次。

![Cron](./public/img/cron.png)

FUNCTION_NAME 为函数名，不填写默认为 `NeteaseCloudMusicTasks`。如需更改，则创建此 secret，并填写自定义的函数名，命名规则：只能包含字母、数字、下划线、连字符，以字母开头，以数字或字母结尾，2~60 个字符。

REGION 默认为 `ap-guangzhou` ，可选的地域详见[地域列表](https://cloud.tencent.com/document/product/583/17238#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8)。

添加完毕可以看到

![Cron](./public/img/secretlist.png)

### 部署

打开部署所用仓库的 `Actions`。

![Actions](./public/img/actions.png)

点击 `All workflows` 下方的 `deploy`（移动端要先点击 `Select workflow`），再点击右侧 `Run workflow`，在弹出的页面再次点击 `Run workflow`，将会运行新的 workflow

![RunWorkflow](./public/img/runworkflow.png)

运行后如果不显示，刷新一下页面即可看到正在运行的 workflow。

![Workflow](./public/img/workflow.png)

等到标志变成 ✅，表示已经部署成功。

![Success](./public/img/success.png)

如果发现标志变成 ❌，则表示部署失败。

![Failure](./public/img/failure.png)

可以点进这个 workflow 查看失败原因。

![Failue](./public/img/failure2.png)

### 添加依赖

下载[依赖文件](https://chen10.lanzouo.com/igHXzxf8wjc) ，也可以自己用 pip 下载依赖，然后打包。然后在[高级能力](https://console.cloud.tencent.com/scf/layer)新建`层`

![Layer](./public/img/layer.png)

`层名称`可以自己任意填写，然后上传刚刚下载的压缩包，点击`添加运行环境`，选择 `Python3.6`。

![Dependence](./public/img/dependence.png)

在[函数服务](https://console.cloud.tencent.com/scf/list)点进刚刚创建的函数

![Function](./public/img/function.png)

点击上方的`层管理`，点击`绑定`

![Bind](./public/img/bind1.png)

选择刚刚创建的层。

![Bind](./public/img/bind2.png)

### 修改配置

在[函数服务](https://console.cloud.tencent.com/scf/list)点进刚刚创建的函数

![Function](./public/img/function.png)

如果在函数服务里找不到刚刚部署的函数，先到 GitHub Actions 中确认是否部署成功。如果部署成功，则确认页面左上角的地域选择是否正确，默认地域应为广州。如果在 Secrets 中设置了 REGION，则根据自己设置的 REGION 选择相应的地域。

在编辑器里点击 `config.json` 这个文件进行配置

![Config](./public/img/config.png)

可以看到文件中有红色波浪线的错误提示，可以忽略不管，也可以下拉到编辑器的右下角，点击 `JSON` 来更改语言模式，选择 `JSON with Comments`，这样就可以消除错误提示。

![Style](./public/img/style.png)

在 `config.json` 里进行如下的账号配置。运行之后如果发现有些任务没有完成，可能是因为没有开启，将任务对应的 `enable` 字段设置为 `true` 即可开启。

#### 账号密码

```json5
"users": [
    {
        "username": "188xxxx8888",
        "countrycode": "",
        "password": "mypassword",
        "cookie": "MUSIC_U=xxxxxxxxx;",
        "X-Real-IP": "",
        "enable": true
    }
],
// ...
```

`username` 里填写手机号或邮箱，`password` 里填写账号密码或 32 位 md5 加密后的密码，`countrycode` 为手机号前缀，使用非中国大陆的手机号登录需填写。`X-Real-IP` 里填写国内 IP，否则可能会有无法登录等情况出现，可填写本机 IP，[点击](https://www.ip138.com/)可查看本机 IP，填写显示的 ip 即可。`enable` 为该账号的开关，设置为 `false` 表示不运行该账号的任务。

如果同时填写了账号密码和 `cookie`， 会优先使用 cookie 登录，如果 cookie 填写有误或失效，会尝试使用账号密码登录。

cookie 获取方式：首先在网页登录[网易云音乐](https://music.163.com/)，然后按 <kbd>F12</kbd> 打开开发人员工具，再按 <kbd>F5</kbd> 刷新页面，最后按照以下步骤来获取 cookie，可以只复制 `MUSIC_U` 的那部分

![Cookie](./public/img/cookie.png)

#### 签到

```json5
"setting": {
    // ...
    "sign": true,
    // ...
}
```

签到默认开启，连续签到可以获得更多云贝。本地和 Docker 运行使用桌面签到接口，并通过网易云接口回查当天到账的云贝。

#### 刷听歌量

```json5
"setting": {
    // ...
    "daka": {
        "enable": true,
        "full_stop": true,
        "auto": true,
        "tolerance": 10,
        "song_number": 300,
        // ...
    },
    // ...
}
```

每个账号每天最多只计算 300 首的听歌量，而且必须是没有听过的歌曲。`enable` 表示开启刷听歌量的任务，`full_stop` 表示满级后自动停止任务，无需手动将 `enable` 设为 `false`。`song_number` 表示每次要刷的歌曲数量，账号等级较低的时候可以设置得小一点，不然等级高的时候就难刷了，可能较难刷满 300 首。

`auto` 设置为 `true` 的话表示开启自动模式，程序将自动调整每次打卡的歌曲数，`song_number` 参数将失效。此时，每天 0 点时定时触发器会自动运行代码，获取当前的听歌数，并写入环境变量中，这样的话就可以比较精确地计算每次打卡的歌曲数。`tolerance` 表示对打卡误差的容忍度，在自动打卡模式下有效，如果设置为 0 表示必须要达到 300 首才停止打卡，10 表示达到 290 首就可以停止打卡。

#### 云贝任务

```json5
"setting": {
    // ...
    "yunbei_claim_rewards": true,
    "yunbei_task": {
        "6718451": {
            "taskName": "探索小众歌曲",
            "module": "listen_indie",
            "enable": false
        },
        "3809301": {
            "taskName": "关注歌手",
            "module": "follow_artist",
            "enable": false,
            "artistId": null,
            "unfollowAfterTask": true
        },
        "3804300": {
            "taskName": "红心歌曲",
            "module": "like_song",
            "enable": false,
            "songId": null,
            "unlikeAfterTask": true
        },
        "162005": {
            "taskName": "发布动态",
            "module": "publishEvent",
            "enable": false,
            // 需要分享的歌单id
            "id": [],
            "msg": ["每日分享","今日分享","分享歌单"],
            "delete": true
        },
        "216002": {
            "taskName": "访问云音乐商城",
            "module": "visitMall",
            "enable": true
        },
        "200002": {
            "taskName": "云贝推歌",
            "module": "rcmdSong",
            "enable": false,
            // 填写歌曲ID
            "songId": [],
            "yunbeiNum": 10,
            "reason": []
        },
        "162006": {
            "taskName": "发布Mlog",
            "module": "publishMlog",
            "enable": false,
            // 留空且 randomRecommendedSong 为 true 时，从推荐歌单随机选歌
            "songId": [],
            "randomRecommendedSong": false,
            /* 动态内容，随机选取一个，其中$artist会被替换为歌手名，$song会被替换为歌曲名 */
            "text": [
                "分享$artist的歌曲: $song",
                "分享歌曲: $song"
            ],
            /* 图片大小，越大则消耗的外网出流量越多 */
            "size": 500,
            /* 发布成功后是否自动删除该动态 */
            "delete": true
        },
        "166000": {
            "taskName": "分享歌曲/歌单",
            "module": "share",
            "enable": false
        },
        "656007": {
            "taskName": "浏览会员中心",
            "module": "visitVipCenter",
            "enable": false
        }
    },
    // ...
}
```

每个子任务通过 `enable` 独立开关。`yunbei_claim_rewards` 控制自动领取已完成任务的奖励。任务是否可执行和奖励数量以网易云返回为准。

| 功能 | 配置与行为 |
| --- | --- |
| 探索小众歌曲 | 从网易云的任务推荐列表选歌，逐首等待 31 秒后上报并回查。按当天剩余进度续跑，最多 10 首。 |
| 关注歌手 | `artistId` 可填歌手 ID。为 `null` 或指定歌手已经关注时，从热门歌手中随机选择一位未关注的歌手。`unfollowAfterTask` 默认为 `true`，任务处理后取关本次新增的关注。 |
| 红心歌曲 | `songId` 可填歌曲 ID。为 `null` 或指定歌曲已经红心时，从每日推荐或推荐歌单里随机选择一首未红心歌曲。`unlikeAfterTask` 默认为 `true`，任务处理后取消本次新增的红心。 |
| 分享歌曲或歌单 | 使用 `166000` 的配置，兼容网易云返回的新版任务 ID `10795676`。新版上报站外分享任务进度，没有接收人设置。 |
| 浏览会员中心 | 使用 `656007` 的配置，兼容新版任务 ID `6758460`。新版触发后等待浏览时长，再回查完成状态。 |
| 访问云音乐商城 | 开启后执行网易云返回的商城访问任务。 |
| 发布动态 | `id` 可指定歌单 ID，留空时从推荐歌单中随机选择。`msg` 设置文案，`delete` 控制发布后是否尝试删除。 |
| 发布 Mlog | 优先使用 `songId` 中的歌曲。留空时，可打开 `randomRecommendedSong` 从推荐歌单随机选歌。使用歌曲专辑封面，`text` 设置文案，`delete` 控制发布后是否尝试删除。 |
| 云贝推歌 | 设置 `songId`、消耗的 `yunbeiNum` 和推荐理由 `reason`。 |

开启自动领奖时，关注歌手和红心歌曲会在撤销本次操作前尝试领取对应奖励。将 `unfollowAfterTask` 或 `unlikeAfterTask` 设为 `false` 可保留本次新增的关注或红心。

#### 音乐人任务

```json5
"setting": {
    // ...
    "musician_task": {
        "749006": {
            "taskName": "音乐人中心签到",
            "module": "musicianSignin",
            "enable": true
        },
        "740004": {
            "taskName": "发布动态",
            "module": "publishEvent",
            "enable": false,
            // 自定义要分享的歌单id，用逗号隔开，分享时随机选取一个，若为空，则从每日推荐歌单中随机选取
            "id": [],
            "msg": ["每日分享","今日分享","分享歌单"],
            "delete": true
        },
        "755000": {
            "taskName": "发布主创说",
            "module": "publishComment",
            "enable": false,
            // 填写你自己歌曲的id，如有多首用,隔开，随机挑选一首
            "id": [],
            "msg": ["感谢大家收听"],
            "delete": true
        },
        "732004": {
            "taskName": "回复粉丝评论",
            "module": "replyComment",
            "enable": false,
            // 填写你自己歌曲的id，如有多首用,隔开，随机挑选一首
            "id": [],
            "msg": ["感谢收听"],
            "delete": true
        },
        "755001": {
            "taskName": "回复粉丝私信",
            "module": "sendPrivateMsg",
            "enable": false,
            // 填写粉丝的用户id，如有多个用,隔开，随机挑选一个进行回复,可以用自己的小号
            "id": [],
            "msg": ["你好"]
        },
        "739008": {
            "taskName": "观看课程",
            "module": "watchCollegeLesson",
            "enable": false
        },
        "740005": {
            "taskName": "访问自己的云圈",
            "module": "visitMyCircle",
            "enable": false,
            /* 自己的云圈ID，可不填写，如果提示 resourceID 获取失败，则需要手动填写 */
            /* 获取方式: 云圈右上角分享，链接中 circleId= 后得参数即为云圈 id */
            "circleId": ""
        },
        "744005": {
            "taskName": "发布mlog",
            "module": "publishMlog",
            "enable": false,
            // 填写歌曲ID
            "songId": [],
            /* 动态内容，随机选取一个，其中$artist会被替换为歌手名，$song会被替换为歌曲名 */
            "text": [
                "分享$artist的歌曲: $song",
                "分享歌曲: $song"
            ],
            /* 图片大小，越大则消耗的外网出流量越多 */
            "size": 500,
            /* 发布成功后是否自动删除该动态 */
            "delete": true
        },
    },
    // ...
}
```

需要是音乐人才能执行，想要开启相应的任务，需要将 `enable` 由 `false` 改为 `true`，`登录音乐人中心`自动开启，其他任务根据实际情况开启。`音乐人中心签到`即签到获取云豆；`发布动态`即转发歌单；`发布主创说`即在自己的歌曲评论区留言；`回复粉丝评论`即在自己歌曲的评论区回复粉丝留言，该任务是通过回复自己的留言实现的；`回复粉丝私信`需要填写粉丝 id，可用小号。

#### VIP 成长值任务

```json5
"setting": {
    // ...
    "vip_task": {
        "816": {
            "taskName": "创建共享歌单",
            "module": "createSharedPlaylist",
            "enable": false,
            /* 自定义歌单名，用逗号隔开，随机选取一个 */
            "name": [
                "歌单",
                "我的歌单"
            ],
            /* 创建成功后是否自动删除该动态 */
            "delete": true
        }
    },
    // ...
}
```

`创建共享歌单` 任务默认关闭，需要开启的话将 `enable` 设为 `true`，`name` 里填写自定义的歌单名，创建时随机选取一个，`delete`表示歌单创建成功后时候自动删除。

#### 推送

支持多种推送方式，建议使用企业微信进行推送

1. [企业微信](https://work.weixin.qq.com/)
2. [server 酱](https://sct.ftqq.com/)
3. [酷推](https://cp.xuthus.cc/)
4. [pushPlus](https://www.pushplus.plus)
5. [Telegram](https://telegram.org/)
6. [Bark](https://github.com/Finb/Bark)
7. [pushdeer](https://github.com/easychen/pushdeer)

要使用推送的话将相应的 `enable` 设为 `true`，并填写配置

##### 企业微信

```json5
"WeCom": {
    "module": "WeCom",
    "enable": false,
    "corpid": "",
    "agentid": "",
    "secret": "",
    "userid": "@all",
    "msgtype": "text",
    /* 是否将多个账号的信息合并推送 */
    "merge": false
}
```

`corpid` 为企业 ID，登录企业微信后在管理后台`我的企业`－`企业信息`下查看；`agentid` 为应用 ID，在`应用管理`里，点进相应的应用可查看；`secret` 为应用密钥，在`应用管理`里，点进相应的应用可查看；`userid` 默认为`@all`，会向该企业应用的全部成员发送；`msgtype` 为消息类型，可填写文本消息 `text`、文本卡片消息 `textcard` 或 markdown 消息 `markdown`，markdown 消息不能在微信里查看，只能在企业微信里查看。

##### server 酱

```json5
"serverChan": {
    "module": "serverChan",
    "enable": false,
    "KEY": "",
    /* 是否将多个账号的信息合并推送 */
    "merge": true
}
```

要使用 server 酱的话需要在 `KEY` 里填写旧版的 SCKEY 或新版的 SendKey。

##### 酷推

```json5
"CoolPush": {
    "module": "CoolPush",
    "enable": false,
    /* 推送方式: send QQ号私人推送 | group QQ群推送 | wx 微信推送 | email 邮件推送 */
    "method": "send",
    "Skey": "",
    /* 是否将多个账号的信息合并推送 */
    "merge": true
}
```

要使用酷推的话需要填写 `Skey`。

##### pushPlus 微信推送

```json5
"pushPlus": {
    "module": "pushPlus",
    "enable": false,
    "pushToken": "",
    /* 消息模板:  markdown | html | txt | json */
    "template": "markdown",
    /* 群组编码，为空时发给自己 */
    "topic": "",
    /* 是否将多个账号的信息合并推送 */
    "merge": true
}
```

要使用酷推的话需要填写 `pushToken`。

##### Telegram 推送

```json5
"Telegram": {
    "module": "Telegram",
    "enable": false,
    /* 自定义域名，放空则默认为 https://api.telegram.org */
    "server": "",    
    /* Telegram账号ID */
    "userId": "",
    /* TG机器人token */
    "botToken": "",
    /* 是否将多个账号的信息合并推送 */
    "merge": true
}
```

要使用 Telegram 的话需要填写 `userId` 和 `botToken`。

##### Bark 推送

```json5
"Bark": {
    "module": "Bark",
    /* 是否启用Bark推送 */
    "enable": false,
    /* Bark的地址 */
    "Bark_url": "",
    /* Bark的API key */
    "Bark_key": "",
    /* 是否将多个账号的信息合并推送, 建议为false，iOS推送消息过长可能会失败 */
    "merge": false
}
```

要使用 Bark 的话需要填写 `Bark_url` 和 `Bark_key`。可以使用 Bark 官方 API 或者自行搭建。

##### pushdeer

```json5
"pushdeer": {
    "module": "pushdeer",
    /* 是否启用推送 */
    "enable": false,
    /* 服务器地址，放空则使用官方服务器: https://api2.pushdeer.com */
    "server": "",
    /* pushkey */
    "pushkey": "",
    /* 是否将多个账号的信息合并推送 */
    "merge": false
}
```

要使用 pushdeer 的话需要填写 `pushkey`。如果使用自己搭建的服务器，请填写 `server`。

#### 刷单曲播放量

```json5
"setting": {
    // ...
    "other": {
        /* 刷歌单中歌曲的播放次数，用来改变听歌风格，仅在需要时使用 */
        "play_playlists": {
            "enable": false,
            /* 歌单id,用逗号隔开,如 [5279371062,5279377564] */
            "playlist_ids": [],
            /* 播放次数 */
            "times": 1
        }
    },
    // ...
}
```

将要刷的歌曲加到歌单中，把歌单 id 填写到 `playlist_ids` 中，可以添加多个歌单 id，用英文逗号隔开，如 `"playlist_ids":[5279371062,5279377564]`。该功能可以用来改变听歌风格。

#### 多账号

```json5
"users": [
    {
        "username": "188xxxx8888",
        "countrycode": "",
        "password": "mypassword",
        "cookie": "",
        "enable": true
    },
    {
        "username": "166xxxx6666",
        "countrycode": "",
        "password": "anotherpassword",
        "cookie": "MUSIC_U=xxxxxxxxx;",
        "X-Real-IP": "",
        "enable": true,
    }
],
// ...
```

在 `users` 内填写多个账号，不同账号之间要用逗号 `,` 隔开。

假如多个账号配置不同可以参照下面

```json5
"users": [
    {
        "username": "188xxxx8888",
        "countrycode": "",
        "password": "mypassword",
        "cookie": "",
        "X-Real-IP": "",
        "enable": true
    },
    {
        "username": "166xxxx6666",
        "countrycode": "",
        "password": "anotherpassword",
        "cookie": "MUSIC_U=xxxxxxxxx;",
        "X-Real-IP": "",
        "enable": true,
        "setting": {
            "push": {
                "serverChan": {
                    "KEY": "xxxxxxxxxx"
                }
            },
            "yunbei_task": {
                "200002": {
                    "songId": [25707139],
                }
            },
        }
    }
],
// ...
```

如上所示，在第二个账号中加入了 `setting` 字段，并填写与公共配置不同的地方。这样一来，两个账号就使用了不同的 server 酱推送，并使用不同的歌曲进行云贝推歌。

#### 关注作者

```json5
"setting": {
    // ...
    "follow": true
    // ...
}
```

默认会在网易云音乐中关注作者，不想关注可将 `true` 改为 `false`。已经关注了的可到网易云音乐 APP 里取消关注。

### 测试

修改完代码后，按 ctrl+s 保存代码，然后点击编辑器右上角的`部署`（每次修改完都要重新部署），左下角的`部署`也行。部署完成后点击部署旁边的测试按钮，观察结果，如果失败则检查修改代码。

![Test](./public/img/test.png)

### 更新代码

将此仓库的更新合入部署仓库后，在 `Actions` 查看部署进度。部署工作流监听 `main` 上的 Python、JSON、Shell 和部署工作流文件变更，其他情况可手动运行 `deploy`。工作流会尝试合并现有云函数配置。需要修改任务时，可参考 `config.example.json` 的注释编辑云函数里的 `config.json`。

如果修改了 Secrets，需要手动部署才会生效，详见[部署](#部署)。

## 二、部署到青龙面板

### 进入容器

```shell
docker exec -it qinglong bash
```

如果容器名称不是 `qinglong` 则需要修改。

### 拉取代码

在青龙容器内把项目克隆到持久化目录。下面使用常见的 `/ql/data` 挂载目录，可按你的容器调整实际路径。

```shell
git clone https://github.com/xiaoyou4264/CloudMusicTasks.git /ql/data/CloudMusicTasks
cd /ql/data/CloudMusicTasks
```

### 生成配置文件

```shell
cp -n config.example.json config.json
```

### 安装依赖

```shell
apk add python3-dev gcc libc-dev
pip3 install requests json5 pycryptodomex
```

### 修改配置文件

按[账号和任务配置](#账号密码)编辑 `config.json`，然后在青龙新增定时任务，命令填写 `cd /ql/data/CloudMusicTasks && python3 index.py`。克隆到其他目录时，定时任务中的路径也要一起调整。

### 更新代码

在容器内运行以下命令，更新代码并合并配置模板。

```shell
cd /ql/data/CloudMusicTasks
git pull --ff-only
python3 updateconfig.py config.example.json config.json config.json
```

每次更新完代码后一定要更新配置文件，否则可能会出错

## 三、本地运行

### 下载

拉取代码

```shell
git clone https://github.com/xiaoyou4264/CloudMusicTasks.git
```

### 安装依赖

切换到项目目录

```shell
cd CloudMusicTasks
```

然后安装依赖

```shell
pip install -r requirements.txt
```

### 修改配置文件

首先将 `config.example.json` 文件复制为 `config.json` 文件

```shell
cp config.example.json config.json
```

然后对配置文件 `config.json` 进行修改，修改方式可以参考[修改配置](#账号密码)

### 运行

```shell
python3 index.py
```

### 更新代码

首先更新代码

```shell
git pull
```

然后更新配置文件

```shell
python3 updateconfig.py config.example.json config.json config.json
```

每次更新完代码后一定要更新配置文件，否则可能会出错

## 四、使用`docker`部署

### 从本仓库构建并运行 Docker Compose

在终端运行以下命令，从本仓库克隆代码并生成本机配置。

```bash
git clone https://github.com/xiaoyou4264/CloudMusicTasks.git
cd CloudMusicTasks
cp -n config.example.json config.json
```

编辑 `config.json`，填写网易云登录信息和需要的推送凭据，再按需开启任务。已有部署可直接编辑本机配置。Compose 以只读方式挂载 `config.json`，该文件已排除在 Git 和镜像构建上下文之外。

```bash
docker compose up -d --build
docker compose ps
docker compose logs --tail=100
```

在 `compose.yaml` 里修改 `SCHEDULER_HOUR` 和 `SCHEDULER_MINUTE` 可以调整北京时间下的执行时间。`SCHEDULER_RUN_ON_START` 默认为 `false`，改为 `true` 后容器每次启动时会额外执行一轮。

| 操作 | 命令 |
| --- | --- |
| 手动执行一轮已开启任务，并发送配置中的推送 | `docker compose exec -T cloudmusictasks python index.py` |
| 修改配置后重新创建容器 | `docker compose up -d --force-recreate` |
| 修改代码后重建镜像并部署 | `docker compose up -d --build` |

### 上游预构建镜像

以下命令使用上游预构建镜像。要使用本仓库的新增任务和接口适配，请按上面的 Compose 方式从源码构建。

> 1. 支持 ARM64/AMD64 docker 镜像
> 2. 支持指定时间定时执行
> 3. 未指定定时执行时间，每次重启随机设定执行时间

### 下载并配置 `config.json`

```shell
curl -fsSL -o config.json https://raw.githubusercontent.com/chen310/NeteaseCloudMusicTasks/main/config.example.json
```

### 随机时间执行

```shell
docker run -itd --restart=on-failure \
    -v $(pwd)/config.json:/root/config.json \
    --name netease-cloud-music-tasks \
    enwaiax/netease-cloud-music-tasks:latest
```

### 指定时间执行

```shell
docker run -itd --restart=on-failure \
    -v $(pwd)/config.json:/root/config.json \
    -e "SCHEDULER_HOUR=8" -e "SCHEDULER_MINUTE=30" \
    --name netease-cloud-music-tasks \
    enwaiax/netease-cloud-music-tasks:latest
```

## 其他

### 对日推的影响

打卡功能可能会影响日推，介意慎用。

### 云函数免费额度及计费方式

在云函数[概览](https://console.cloud.tencent.com/scf/index)界面，可以查看本月剩余免费额度

详见[计费概述](https://cloud.tencent.com/document/product/583/17299)

### 声明

- 本仓库中的脚本仅用于测试和学习目的，请勿用于商业或非法目的，否则后果自负
- 转载请注明出处，并保留原作者信息。
- 如果您认为该项目的脚本可能涉嫌侵犯您的权利，请及时通知，我们将在确认后及时删除

本仓库基于 [Vonalien/CloudMusicTasks](https://github.com/Vonalien/CloudMusicTasks)，原始项目为 [chen310/NeteaseCloudMusicTasks](https://github.com/chen310/NeteaseCloudMusicTasks)。

### 灵感来源

1. [网易云音乐 API](https://github.com/Binaryify/NeteaseCloudMusicApi)
2. [NetEase-MusicBox](https://github.com/darknessomi/musicbox)
