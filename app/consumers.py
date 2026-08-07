"""Kafka consumers for charge-capture-service.

One handler per subscribed topic. Real handlers write to this service's own
database and/or publish follow-up events; stub handlers just log + audit.
"""
from __future__ import annotations

import logging

from psycopg.types.json import Json

from healthcare_common.audit import emit_audit

log = logging.getLogger("charge-capture-service.consumers")

TABLE = "charge_capture"


def register(svc) -> None:
    bus = svc.bus
    db = svc.db
    clients = svc.clients

    @bus.on("encounter.ended")
    def _on_encounter_ended(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    # Turn the encounter into billable charges (naive: single line item).
                    row = db.query_one(f"INSERT INTO {TABLE} (data) VALUES (%s) RETURNING *",
                                       (Json({"encounter_id": data.get("id"),
                                              "patient_id":  data.get("patient_id"),
                                              "amount":      data.get("estimated_charge") or 100.0,
                                              "state": "captured"}),))
                    bus.publish("charge.captured", key=str(row["id"]),
                                value={"charge_id": row["id"], **row["data"]})
        except Exception as e:
            log.exception("charge-capture-service/encounter.ended handler failed: %s", e)
        emit_audit(bus, action="consume.encounter.ended", actor="system:charge-capture-service",
                   target=None, details={"envelope_id": envelope.get("id")})

