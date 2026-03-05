# iCloud Calendar

Add events to iCloud Calendar via CalDAV. Syncs to iPhone automatically.

## Setup (已配置)

**已配置账号：**
- Email: wangjintao1999@icloud.com
- CalDAV URL: https://caldav.icloud.com

**Note:** 需要 App Specific Password（已在 credentials 中配置）

## Add Event

使用自然语言创建日程，格式如：
- "明天上午10点有个会议"
- "下周五3点安排客户电话"
- "每天早上8点跑步"

## Technical

使用 CalDAV PUT 请求添加 .ics 格式的日程到默认日历。