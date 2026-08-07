"""Kafka consumers for charge-capture-service.

One handler per subscribed topic. Handlers are best-effort logging plus
audit — services override this file to implement real cross-domain behavior.
"""
from __future__ import annotations

import logging

from healthcare_common.audit import emit_audit

log = logging.getLogger("charge-capture-service.consumers")


def register(svc) -> None:
    bus = svc.bus

    @bus.on("encounter.ended")
    def _on_encounter_ended(envelope: dict) -> None:
        log.info("charge-capture-service: received encounter.ended id=%s", envelope.get("id"))
        emit_audit(bus, action="consume.encounter.ended", actor="system:charge-capture-service",
                   target=None, details={"envelope_id": envelope.get("id")})

