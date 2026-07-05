# Frontend Backend Integration Guide

## Current State

The mini program is configured to call the local FastAPI backend:

```js
apiBaseUrl: 'http://127.0.0.1:8000/api/v1'
useMock: false
autoGuestLogin: true
```

`autoGuestLogin` is enabled for local development. When the mini program starts without a local token, it calls `/auth/wx-login` with a development guest code and stores a valid backend token.

The request layer also retries once after a `401` response when `autoGuestLogin` is enabled. This handles the common local-development race where a page requests a protected endpoint before the startup guest-login request has finished.

## Start Backend

```powershell
cd F:\code\python\xingyu\backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Health check:

```text
http://127.0.0.1:8000/api/v1/health
```

OpenAPI:

```text
http://127.0.0.1:8000/docs
```

If port 8000 is occupied:

```powershell
netstat -ano | findstr :8000
Stop-Process -Id <PID> -Force
```

## Local Verification

Backend:

```powershell
cd F:\code\python\xingyu\backend
pytest
```

Mini program JavaScript syntax:

```powershell
cd F:\code\python\xingyu
Get-ChildItem -Path miniprogram -Recurse -Filter *.js | ForEach-Object {
  node --check $_.FullName
  if ($LASTEXITCODE -ne 0) { throw "JS syntax check failed: $($_.FullName)" }
}
```

## Manual Page Checklist

Run these pages in WeChat Developer Tools after the backend is up:

1. Login page: guest entry and WeChat login button.
2. Home page: today poem, recommended poems, hot keywords.
3. Category page: category list and category poem list.
4. Poem detail page: detail loading, favorite toggle, history recording.
5. Square page: feed, like, favorite, share, create topic.
6. Square detail page: detail loading, comment create, comment like/favorite.
7. Feihualing page: room list, enter room, answer check, record save.
8. Profile page: overview, profile edit, favorites, likes, follows, feihualing rooms.
9. Feedback page: feedback submission.

## Notes

- `127.0.0.1` works in the desktop developer tool when the backend runs on the same machine.
- For real-device preview, replace `apiBaseUrl` with a LAN IP or HTTPS test domain that the device can reach.
- The backend creates SQLite tables and seed data on startup in development mode.
