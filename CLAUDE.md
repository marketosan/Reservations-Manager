# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

The Django project has been scaffolded: `manage.py`, the `reservations_manager/` project package (settings/urls/wsgi/asgi), and two apps live at the repo root — `properties` (the reservations/property domain) and `accounts` (Django-auth user management: login/logout + staff-only user CRUD). Both are registered in `INSTALLED_APPS`.

- Models: `Property` (name, address, mandatory unique `ical_url`, created_at) and `Reservation` (FK to Property, `uid` matched against booking.com's iCal `VEVENT` UID to avoid duplicate imports, start/end date, summary, synced_at) — both in `properties/models.py`, registered in Django admin. See `docs/schema.md` for the field list and ERD.
- Auth/URLs: login-gated access is in place, fully owned by the `accounts` app. `/login/` and `/logout/` use Django's built-in `LoginView`/`LogoutView` (`accounts/urls.py`) with templates in `accounts/templates/registration/`; staff-only user CRUD lives at `/users/...` (`accounts/views.py`, `accounts/forms.py`, `accounts/templates/accounts/`). `/` is a `home` view (`properties/views.py`) behind `@login_required`. `LOGIN_URL`/`LOGIN_REDIRECT_URL`/`LOGOUT_REDIRECT_URL` are set in settings. No plain "user" role/permissions have been built yet — only a seeded `admin` superuser exists so far; the admin/user permission split is still TBD (see Project goals).
- The shared navbar (`properties/templates/properties/layout/admin_base.html` / `guest_base.html`) has a daisyUI `navbar`: app title on the left; on the right, a Settings dropdown visible only to `user.is_staff` (links to the `accounts` user list) and a user-icon dropdown with the log-out form. `login.html` is still plain unstyled HTML — not yet updated to Tailwind/daisyUI.
- Styling: Tailwind CSS v4 + daisyUI, built via the Tailwind standalone CLI (no Node/npm). Source lives in `tailwind/` — `input.css` (`@import "tailwindcss"`, scans both `properties/templates` and `accounts/templates` via `@source`, loads `daisyui.mjs` and `daisyui-theme.mjs` as `@plugin`s, both vendored directly since there's no npm install). The `tailwind/tailwindcss` binary itself is gitignored (~100MB+, platform-specific; re-download link is in the `.gitignore` comment). Compiles to `properties/static/properties/css/my_tailwind.css`, linked from templates via `{% load static %}` / `{% static %}`. Per user preference, CSS always stays in this static file — never inline `<style>` tags in templates.
- A `PostToolUse` hook in `.claude/settings.json` reminds Claude to keep `docs/schema.md` in sync whenever `properties/models.py` changes.

This file will be filled in incrementally as the project develops.

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
- Settings module lives at `reservations_manager/settings.py`; project package and each app (`properties`, `accounts`) sit as siblings at the repo root alongside `manage.py`, per Django convention

## UI approach

- Server-rendered Django templates + HTMX (and Alpine.js for small client-side interactivity), not a separate SPA/API frontend. Keeps everything in one Django codebase and works naturally with Django's built-in admin/auth for the admin/user roles.
- Styling is Tailwind CSS v4 + daisyUI (see Project status for the build setup), not hand-written CSS.
- Calendar/availability grid uses **FullCalendar** (JS library) embedded in a template for the interactive view.
  - Date-range selection uses FullCalendar's default drag/click-start-then-end range selection (contiguous days only — no ctrl-click multi-select needed).
  - On selection, the start/end range is submitted (via HTMX or fetch) to a Django view that bulk-creates/updates the reservation and any per-day info (price, comments, etc.) across that range in one transaction.
- Rationale: this is a small internal admin tool; a full SPA (React/Vue + DRF API) would add build-pipeline and auth-token overhead that isn't justified here. Revisit only if the UI needs grow significantly richer/more app-like.

## Notes

- No commands, architecture, or conventions are documented yet since there is no source tree to describe. Update this file as the project takes shape.
