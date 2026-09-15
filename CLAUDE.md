# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

The Django project has been scaffolded: `manage.py`, the `reservations_manager/` project package (settings/urls/wsgi/asgi), and an initial `reservations` app live at the repo root. `reservations` is registered in `INSTALLED_APPS`. No models, views, or URLs have been written yet. This file will be filled in incrementally as the project develops.

## Project goals

A Django app to track and organize reservations from booking.com.

- Supports multiple properties.
- Two roles: admin and user (exact permission split TBD).
- Reservation data is initially ingested via booking.com's iCal export links (one per property/room).
- Admin UI shows availability per property based on the imported iCal data.
- Later: on top of the imported iCal data, admin will be able to edit availability and add prices, comments, and other info per calendar entry/day within the app.
- Calendar UI supports selecting a **contiguous range of days** (like a booking-site date-range picker, not multi-select via ctrl-click) to add info to / reserve all of them at once, mirroring how a real booking spans consecutive nights.

Requirements are still being gathered and will be refined here as decisions are made.

## Intended stack

- Python 3.14, Django 6.1.1 (installed in `venv/`)
- Local dependencies: `asgiref`, `sqlparse`, `Black` (formatter)
- Settings module lives at `reservations_manager/settings.py`; project package and each app (starting with `reservations`) sit as siblings at the repo root alongside `manage.py`, per Django convention

## UI approach

- Server-rendered Django templates + HTMX (and Alpine.js for small client-side interactivity), not a separate SPA/API frontend. Keeps everything in one Django codebase and works naturally with Django's built-in admin/auth for the admin/user roles.
- Calendar/availability grid uses **FullCalendar** (JS library) embedded in a template for the interactive view.
  - Date-range selection uses FullCalendar's default drag/click-start-then-end range selection (contiguous days only — no ctrl-click multi-select needed).
  - On selection, the start/end range is submitted (via HTMX or fetch) to a Django view that bulk-creates/updates the reservation and any per-day info (price, comments, etc.) across that range in one transaction.
- Rationale: this is a small internal admin tool; a full SPA (React/Vue + DRF API) would add build-pipeline and auth-token overhead that isn't justified here. Revisit only if the UI needs grow significantly richer/more app-like.

## Notes

- No commands, architecture, or conventions are documented yet since there is no source tree to describe. Update this file as the project takes shape.
