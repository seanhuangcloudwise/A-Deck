# Data Architecture Skill (TOGAF Layer 3)

This skill covers data domains, entity relationships, lineage, lifecycle, and governance responsibilities.

## Scope

Use this skill when users ask for:
- data domain and entity relationship modeling
- data flow and lineage tracing
- data governance and stewardship design
- master data lifecycle management
- data catalog and classification structure
- conceptual or logical data modeling

Do not use this skill for database schema DDL, ETL pipeline code, or SQL query design.

## Mandatory Rules

1. Title/subtitle must use master placeholders first.
2. Rounded rectangle corners stay small.
3. No decorative-only shapes/lines; each connector must represent a relationship.

## Diagram Catalog (Must Support)

1. Conceptual Data Model — high-level entity and relationship overview
2. Logical Data Model — detailed attributes and relationships (3NF-oriented)
3. Data Flow Diagram — data movement across systems and processes
4. Data Domain Map — classification of data into business domains
5. Data Governance Framework — roles, policies, processes for data stewardship
6. Master Data Lifecycle — lifecycle stages of master data entities
7. Data Lineage — source-to-target data transformation tracing
8. Data Catalog Structure — metadata taxonomy and catalog organization

## Diagram Specifications

All diagrams in this skill have dedicated production-level specs with layout variants, color semantics, typography, anti-patterns, and industry references.

See `diagrams/` subdirectory:

- [DA-01: Conceptual Data Model](diagrams/conceptual-data-model.md)
- [DA-02: Logical Data Model](diagrams/logical-data-model.md)
- [DA-03: Data Flow Diagram](diagrams/data-flow-diagram.md)
- [DA-04: Data Domain Map](diagrams/data-domain-map.md)
- [DA-05: Data Governance Framework](diagrams/data-governance-framework.md)
- [DA-06: Master Data Lifecycle](diagrams/master-data-lifecycle.md)
- [DA-07: Data Lineage](diagrams/data-lineage.md)
- [DA-08: Data Catalog Structure](diagrams/data-catalog-structure.md)

See [diagrams/_catalog.md](diagrams/_catalog.md) for selection guide.

## Selection Logic

- If request mentions entity/relationship/ERD: prioritize conceptual-data-model, logical-data-model.
- If request mentions data flow/ETL/pipeline: prioritize data-flow-diagram, data-lineage.
- If request mentions governance/stewardship/quality: prioritize data-governance-framework.
- If request mentions master data/MDM/lifecycle: prioritize master-data-lifecycle.
- If request mentions domain/classification/catalog: prioritize data-domain-map, data-catalog-structure.

## QA Checklist

- Are all connectors semantic (flow/ownership/reference) rather than decorative?
- Are page titles/subtitles in placeholders?
- Are data entities clearly distinguished from processes and systems?
- Are data governance roles (Owner/Steward/Custodian) labeled where applicable?
