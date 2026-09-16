# Data model

## Property + Reservation

Each `Property` has its own distinct booking.com iCal export link
(1-to-1: one iCal URL per property). `Reservation` rows are imported from
that feed — one row per iCal `VEVENT`, matched on `uid` so re-syncing
updates existing rows instead of duplicating them.

```mermaid
erDiagram
    PROPERTY ||--o{ RESERVATION : has

    PROPERTY {
        int id PK
        string name
        string address "blank"
        string ical_url "unique, required"
        datetime created_at
    }

    RESERVATION {
        int id PK
        int property_id FK
        string uid "unique per property"
        date start_date
        date end_date
        string summary "blank"
        datetime synced_at
    }
```
