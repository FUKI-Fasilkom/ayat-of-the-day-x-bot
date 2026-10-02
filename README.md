# twitter-bot-aod

Dedicated X posting service for **Ayat of The Day**. It exposes one protected endpoint and publishes through the posting account's authenticated X web session.

```text
AOD Cloudflare Worker -> HTTPS -> twitter-bot-aod -> X web API
```

This service uses undocumented X browser endpoints through `twitter-openapi-python`, not the official X API. It avoids per-request X API charges, but X may change those endpoints and invalidate the integration without notice. Session cookies also expire. Use a dedicated account, monitor failures, and comply with X's rules.

## Configure

Copy `.env.example` to `.env` and set:

- `SERVICE_BEARER_TOKEN`: a long random value shared only with the AOD Worker.
- `TWITTER_AUTH_TOKEN`: the X session's `auth_token` cookie.
- `TWITTER_CT0`: the X session's `ct0` cookie.

The two X cookies provide account access. Never send them to the Worker, commit them, or place them in logs.

## Run locally

```bash
cp .env.example .env
docker compose up --build
```

The Compose service binds to `127.0.0.1:8010` by default.

## API

Health check:

```http
GET /health
```

Create a post:

```http
POST /api/v1/tweets
Authorization: Bearer <SERVICE_BEARER_TOKEN>
Content-Type: application/json

{"tweet_text":"Ayat of The Day..."}
```

A successful response is:

```json
{"tweet_id":"123456789","tweet_text":"Ayat of The Day..."}
```

## Connect AOD

Deploy this repository to an HTTPS-capable container host, then configure the AOD Worker:

```bash
npx wrangler secret put TWITTER_BOT_URL
npx wrangler secret put TWITTER_BOT_TOKEN
```

`TWITTER_BOT_URL` is this service's HTTPS origin. `TWITTER_BOT_TOKEN` must equal this service's `SERVICE_BEARER_TOKEN`.

## Validate

```bash
python -m compileall app tests
python -m pytest
```
