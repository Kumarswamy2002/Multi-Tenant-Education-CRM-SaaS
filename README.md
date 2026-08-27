# Multi-Tenant Education CRM SaaS (CampusSphere CRM)

CampusSphere CRM is an enterprise-grade Customer Relationship Management SaaS platform engineered specifically for educational institutions. It provides a unified 360-degree view of relationships across the entire learner lifecycle:

```text
Prospect → Lead → Counseling → Application → Admission → Student → Engagement → Student Success → Career → Alumni
```

---

## Key Features

- **Multi-Tenant Data Isolation**: Logical data separation with tenant authorization context across database, search, and AI queries.
- **Unified Person & Organization Architecture**: Zero data duplication with a single `Person` model (Student, Parent, Counselor, Faculty, Alumni) and `Organization` model (Institutions, Employers, Partners).
- **Relationship Graph Engine**: Centralized tracking of complex education relationships (`HAS_PARENT`, `ADVISED_BY`, `TAUGHT_BY`, `ENROLLED_IN`, `APPLIED_TO`, `MENTORED_BY`).
- **Unified Timeline**: Outbox pattern domain events aggregated into a chronological relationship history.
- **Workflow Automation**: Visual workflow engine supporting custom triggers, nested conditions, branching, and automated actions.
- **Integration Hub & Webhooks**: Canonical Education Data Model, webhook signature validation, idempotency checks, and dead-letter queues.
- **Student Success & AI Intelligence**: Risk signal aggregation, lead scoring ML algorithms, career skill recommendations, and tenant-scoped AI assistants.
- **Support & Case Management**: Centralized ticket routing, SLA enforcement, and multi-department triage.

---

## Monorepo Architecture

```text
campussphere/
├── apps/
│   ├── web/                 # Next.js Institutional Admin Portal
│   ├── student-portal/      # Next.js Student Self-Service Portal
│   ├── parent-portal/       # Next.js Parent/Guardian Portal
│   ├── counselor-portal/    # Next.js Admissions & Counseling Workspace
│   └── employer-portal/     # Next.js Employer & Recruitment Portal
├── backend/                  # FastAPI Modular Backend Services
│   ├── identity/            # Multi-Tenant Auth, JWT & RBAC
│   ├── tenants/             # Tenant & Subscription Management
│   ├── organizations/       # Institutions, Employers & Departments
│   ├── people/              # Unified Person Model & Profiles
│   ├── crm/                 # Leads, Activities, Case System
│   ├── admissions/          # Counseling, Applications & Eligibility Pipeline
│   ├── students/            # Student 360 & Timeline Engine
│   ├── success/             # Student Success Engine & Interventions
│   ├── career/              # Skills, Resumes, Jobs, Employers & Placement
│   ├── alumni/              # Alumni Profiles, Mentorship & Networking
│   ├── workflows/           # Workflow Engine Execution & Triggers
│   ├── integrations/        # Canonical Model Adapters & Webhooks
│   ├── analytics/           # Cross-domain BI Aggregators
│   └── ai/                  # Lead Scoring ML & RAG Engine
├── packages/                # Shared Types, Schemas & Utilities
├── infrastructure/          # Docker Compose, K8s, Prometheus, Grafana
└── tests/                   # 20,000+ LOC Unit, Integration & Security Tests
```

---

## Tech Stack

- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, TanStack Query, Zustand, Recharts.
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy 2.0 (Async), Pydantic v2, Alembic.
- **Database**: PostgreSQL 16+ (Multi-Tenant Data Isolation).
- **Cache & Async**: Redis 7+, Celery async task queue.
- **Event Streaming**: Apache Kafka / Outbox pattern dispatches.
- **Search**: OpenSearch / PostgreSQL Full-Text Search.
- **AI/ML**: Scikit-Learn (Lead Scoring) + RAG Vector Engine.

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm / pnpm
- Docker & Docker Compose

### Environment Setup
```bash
cp example.env .env
```

### Running with Docker Compose
```bash
docker-compose up -d --build
```

### Running Backend Locally
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## License

Copyright © 2026 CampusSphere. All rights reserved.
