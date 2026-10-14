---
url: https://sarvam.ai/trust-center/
title: Trust Center | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:16:31.972679+00:00
---

# Trust Center | Sarvam AI

> Source: https://sarvam.ai/trust-center/

![Sarvam Motif](https://assets.sarvam.ai/assets/motifs/ui/motif.svg)

# Sarvam Trust Center

Complete data residency in India. ISO 27001 and SOC 2 Type II certified. This is our Trust Center, covering how we approach data security and compliance, the certifications we hold, the controls we operate, and direct answers to the questions we hear most from security teams.

See certificationsRequest documents

##  How we think about security 

Four commitments that shape how we build, ship, and operate. They show up in our architecture, our policies, and how our team works day to day. 

01 / Posture

### Secure by default.

Every design decision starts from the conservative position. Least-privilege access, encryption at rest and in transit, tenant isolation, and ephemeral storage are defaults, not toggles you have to opt into.

02 / Track record

### Built for high-stakes environments.

Multiple deployment models for different security needs: managed SaaS, single-tenant on-premises, or fully air-gapped with zero external network dependency. We've run all three in production for banks, government, and critical public infrastructure.

03 / Data stewardship

### Your data stays yours.

Customer Managed Keys for Enterprise ensure that even we cannot see your data at rest. We don't share data across tenants. We don't move it across borders unless you ask us to. Custom models trained on a customer's data remain inside the customer's environment, with weights they own and we never reuse.

04 / Transparency

### Honest about where we are.

We're ISO 27001:2022 certified and hold SOC 2 Type II. ISO 42001 is in progress, and we'll publish it when it's done. We won't claim a control we don't run.

## Compliance

Independent audits are how we hold ourselves accountable. The frameworks below cover information security, AI management, financial regulation, and India's data protection law.

ISO 27001

### ISO 27001:2022

Information Security Management System. Audited annually by an accredited third party.

Certified

SOC 2 Type I

### SOC 2 Type I

Trust Services Criteria covering Security, Availability, and Confidentiality.

Report available

SOC 2 Type II

### SOC 2 Type II

Operating effectiveness of controls across an audit window. Certified.

Certified

ISO 42001

### ISO 42001

AI Management System. Scoped and underway as part of our security roadmap.

In progress

DPDP

### India DPDP Act

Digital Personal Data Protection Act, 2023. Our processes are built around consent, purpose limitation, and data principal rights.

In progress

RBI

### RBI FREE-AI

The Reserve Bank of India's Framework for Responsible and Ethical AI in the BFSI sector.

Aligned

MeitY

### MeitY Guidelines

Ministry of Electronics and IT cloud and AI security guidelines, applied across our UIDAI, NPCI, and IndiaAI deployments.

Aligned

CERT-In

### CERT-In

Indian Computer Emergency Response Team directives for incident logging, retention, and reporting.

In touch

## Resources

The documentation behind our practices. Most reports are released under a mutual NDA. Our security team responds within two business days.

Request all documents

#### ISO 27001:2022 Certificate

Our official certificate of registration, along with the Statement of Applicability.

Request→

#### SOC 2 Reports

Independent attestation reports on the design and operating effectiveness of our controls. Shared under mutual NDA.

Request→

#### Penetration Test Summary

Executive summary of our most recent third-party web application and API penetration test.

Request→

#### Information Security Policy

Our top-level policy and the ISMS control set that governs security, availability, and confidentiality.

Request→

#### Data Processing Addendum

Our standard DPA covering Sarvam's role as a processor under DPDP and equivalent regimes.

Request→

#### Responsible AI Framework

How we approach risk for our foundational models: data curation, inference-time guardrails, evaluations, and red-teaming.

Request→#### [Privacy PolicyHow we collect, process, and retain data across our products and APIs.Visit→](https://sarvam.ai/privacy-policy)

#### BCP and DR Plan

Our Business Continuity and Disaster Recovery Policy, tabletop schedule, and RPO and RTO targets.

Request→

#### Incident Response Plan

How we detect, contain, and notify. Includes our two-hour customer notification commitment and the lessons-learned step that follows every incident.

Request→

## Controls

A summary view of the technical and organisational controls we operate every day, across security, privacy, and AI safety.

Continuously monitored 

### Access Security

  * SSO and MFA enforced for all production access
  * Role-based access control with least-privilege defaults
  * Unique user IDs and password hashing with salt
  * Idle session timeout and a documented joiner, mover, leaver workflow
  * Quarterly user access reviews



### Network Security

  * Azure Firewall Manager (Premium) with IDPS
  * WAF, IP allowlisting, and port restrictions
  * mTLS at integration boundaries; OAuth 2.0 and JWT
  * VNet segmentation between environments



### Data Protection

  * AES-256 at rest, TLS 1.2 or higher in transit
  * CMEK and BYOK with configurable rotation
  * India-only residency for Indian deployments
  * Configurable retention with certified deletion at termination
  * PII masking, pseudonymisation, and redaction



### Incident Response

  * Documented Incident Management Policy within the ISMS
  * Detection via Azure Monitor and Grafana dashboards
  * Customer notification within two hours of discovery
  * L1, L2, L3 triage with a mandatory lessons-learned retro



### Change Management

  * Documented change policy with required PR review
  * Segregated development, staging, and production environments
  * Zero-downtime deploys; phased rollouts behind feature flags
  * Production data is never used in non-production environments



### Vulnerability Management

  * Continuous code scanning in private repositories
  * Annual third-party penetration testing
  * Secure SDLC with security gates prior to production
  * High and critical findings closed before promotion



### Availability and Recovery

  * 99.9% uptime SLA on enterprise contracts
  * Daily encrypted backups with real-time replication for critical data
  * Multi-AZ and multi-DC redundancy and failover
  * BCP and DR plan tested against agreed RPO and RTO targets



### People and Organisation

  * Background verification through SpringVerify for every hire
  * NDAs and confidentiality agreements at onboarding
  * Security and privacy training at hire, with annual refreshers
  * Dedicated InfoSec function with executive sponsorship



### AI and Model Security

  * Inference-time guardrails against prompt injection
  * Input and output sanitisation with sensitive-content filtering
  * Versioned models, prompts, and evaluations with audit trail
  * Customer data is never used to train models for other customers



### Talk to our security team

[[email protected]](https://sarvam.ai/cdn-cgi/l/email-protection#93e0f6f0e6e1fae7ead3e0f2e1e5f2febdf2fa)[Contact our DPO](https://sarvam.ai/cdn-cgi/l/email-protection#e6829689a695879490878bc8878f)

## Frequently asked questions

### Where does Sarvam store customer data?

In India, for Indian customers. Our managed production environment runs on Microsoft Azure's Central India region, and our LLM inference runs on sovereign GPU infrastructure operated by Yotta and NxtGen. If your security posture demands more, we can deploy the entire stack inside your own VPC, an on-premises data centre, or an air-gapped environment with no external network dependency. We've run this pattern in production for UIDAI on bare-metal infrastructure.

### How is data encrypted at rest and in transit?

AES-256 at rest, TLS 1.2 or higher in transit. Every byte. That includes internal service-to-service traffic, and we enforce mTLS at integration boundaries. If you'd rather hold the keys yourself, we support customer-managed keys (CMEK and BYOK), with rotation cadences and per-tenant isolation that you control.

### What deployment models do you support?

All of them. Managed SaaS on Azure Central India if you'd like us to operate the infrastructure. A single-tenant deployment in your own VPC on AWS, Azure, or GCP if you want isolation without owning the data centre. Fully on-premises if you do. Air-gapped if you need zero outbound network calls. The platform is fully containerised on Kubernetes, provisioned with Terraform and Helm. The same artefacts deploy across all four targets, which means our security posture stays consistent wherever you run us.

### How is multi-tenant data isolated?

In our shared SaaS environment, tenants are logically separated using tenant-scoped JWT tokens, Azure VNet segmentation, and per-tenant database structures. Internal access is gated by RBAC with least-privilege defaults. For customers who need physical separation, including banks, regulated enterprises, and government, we deploy single-tenant. And to be explicit: we do not use one customer's data to train or fine-tune models for any other customer. Ever.

### What's your data retention policy?

Whatever you need it to be. Retention is configurable per customer and per data category, covering audio, transcripts, and structured metadata. We support an ephemeral mode where data passes through our systems only for processing and is purged immediately afterwards. At contract end, your data comes out of our primary systems and backups under our Data Record Retention and Deletion Policy. We'll send you a certificate of deletion when it's done.

### How does Sarvam handle PII?

We collect as little as we can. Customers can opt out of audio storage entirely. For data we do retain, sensitive fields are masked, hashed, or pseudonymised by default, and access is gated by RBAC with full audit logging. We do not use your data, PII or otherwise, to improve models for anyone else. Custom model weights trained on your data stay in your environment, on your hardware.

### What is your incident response and breach notification commitment?

Two hours. If we discover a security or privacy incident that could affect your data, you hear from us within two hours of discovery, per our Breach Notification Plan. Detection runs on Azure Monitor with Grafana dashboards. Response follows a documented Incident Management Policy that's part of our ISMS, with severity-based SLAs and a mandatory lessons-learned step after every incident.

### Do you conduct penetration tests and vulnerability assessments?

Yes. We run continuous code scanning across our private repositories, security testing in QA and staging before promotion, and we engage third parties for web application and API penetration tests. High and critical findings are tracked to closure before code reaches production. Executive summaries are available under mutual NDA.

### How is internal access to customer data restricted?

By default, no one has it. Production access is least-privilege and gated through SSO with MFA. Developers don't get standing access. Role assignments are reviewed on the cadence set out in our Access Control Policy, and every access event is logged for audit. Every Sarvam employee passes background verification through SpringVerify before access is provisioned, signs a confidentiality agreement, and completes security and privacy training at onboarding with an annual refresh.

### How are Sarvam's AI models secured against misuse?

We train our foundational models from scratch on data we curate ourselves for quality and screen for sensitive content. At inference, we apply guardrails that enforce instruction adherence and screen for prompt injection, off-script behaviour, and hallucination. Inputs and outputs are sanitised, sensitive-content filtering runs in both directions, and synthesised voices are restricted to those with explicit permission so they cannot be used to impersonate real people. Every model and prompt version is tracked with a full audit trail.

### What about business continuity and disaster recovery?

Encrypted backups run daily. Critical data replicates in real time. Production deployments span multiple availability zones and data centres with redundancy and failover, against RPO and RTO targets we agree with you upfront. Our BCP and DR plan is governed by our ISMS and exercised through tabletop scenarios.

AI agents that understand, learn, and always deliver. 

AI agents that understand,

learn, and always deliver.

[Contact Us](https://sarvam.ai/contact-us)
