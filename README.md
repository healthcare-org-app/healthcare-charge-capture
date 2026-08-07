# charge-capture-service

charge-capture-service — domain: billing

- **Port:** 8701
- **Language:** Python 3.11 + Flask
- **Database:** `billing` (Postgres, table `charge_capture`)
- **Event bus:** Kafka

## API

| Method    | Path                       |
|-----------|----------------------------|
| GET       | `/api/charge_capture/`          |
| POST      | `/api/charge_capture/`          |
| GET       | `/api/charge_capture/<id>`      |
| PUT/PATCH | `/api/charge_capture/<id>`      |
| DELETE    | `/api/charge_capture/<id>`      |
| GET       | `/health`                  |
| GET       | `/ready`                   |

## Events

**Publishes:** charge.captured
**Subscribes:** encounter.ended

## HTTP peer dependencies

- `ehr-service`
- `coding-service`
- `audit-log-service`

## Local dev

```bash
pip install -e ../../libs/py-healthcare-common
pip install -r requirements.txt
cp .env.example .env
(cd ../../infra && docker compose up -d postgres kafka kafka-init)
python -m app.main
```

## Tests

```bash
pytest
```
