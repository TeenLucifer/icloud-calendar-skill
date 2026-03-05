# iCloud Calendar

Add events to iCloud Calendar via CalDAV. Syncs to iPhone automatically.

## Setup

### 1. Get iCloud App Specific Password

1. Go to [appleid.apple.com](https://appleid.apple.com)
2. Sign in → "Sign-In and Security"
3. Click "App-Specific Passwords" → "+"
4. Create a new password and save it

### 2. Configure Credentials

Copy the example env file and fill in your credentials:

```bash
cp secrets/.env.example secrets/.env
# Edit secrets/.env with your credentials
```

Or set environment variables directly:

```bash
export ICLOUD_EMAIL="your-email@icloud.com"
export ICLOUD_PASSWORD="your-app-specific-password"
```

## Add Event

使用自然语言创建日程，格式如：
- "明天上午10点有个会议"
- "下周五3点安排客户电话"
- "每天早上8点跑步"

## Technical

- Credentials stored in `secrets/.env` (not committed to Git)
- Uses CalDAV PUT request to add .ics format events
- Supports alarm reminders (default 15 min + 5 min before)