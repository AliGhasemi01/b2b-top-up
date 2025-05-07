## 📄 Project Overview

This Django REST API simulates a basic B2B mobile top-up system.

- Sellers can register, log in, view their profile, and request credit increases.
- Admins review and approve or reject credit requests via the Django admin panel.
- Approved credit is added to the seller’s balance using safe transaction logic.
- Sellers can perform mobile top-ups if they have sufficient credit.
- Logs are recorded for each top-up request.
- The system enforces data integrity using `transaction.atomic()` and `select_for_update()`.
- Admin permissions prevent reprocessing of finalized credit requests.

All credentials and secrets are managed via `.env` and excluded from version control.
