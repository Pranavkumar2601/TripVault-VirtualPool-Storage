# 🚀 TripVault - Complete Software Requirements Specification

<div align="center">

**Distributed Cloud Storage for Group Travel**

![Version](https://img.shields.io/badge/version-1.0-blue)
![Status](https://img.shields.io/badge/status-design_phase-orange)
![License](https://img.shields.io/badge/license-MIT-green)

_Share trip memories without storage limits_

</div>

---

## 📋 Document Information

| Field                 | Details                        |
| --------------------- | ------------------------------ |
| **Document Version**  | 1.0                            |
| **Last Updated**      | January 23, 2026               |
| **Author**            | [Your Name]                    |
| **Project Status**    | Pre-Development (Design Phase) |
| **Target Completion** | Q2 2026 (8-10 weeks)           |

---

## 📖 Table of Contents

- [1. 🎯 Introduction](#1--introduction)
  - [1.1 Purpose](#11-purpose)
  - [1.2 Scope](#12-scope)
  - [1.3 Intended Audience](#13-intended-audience)
- [2. 🌍 Overall Description](#2--overall-description)
  - [2.1 Problem Statement](#21-problem-statement)
  - [2.2 Solution Overview](#22-solution-overview)
  - [2.3 Product Functions](#23-product-functions)
  - [2.4 User Personas](#24-user-personas)
- [3. ⚙️ System Features & Requirements](#3-️-system-features--requirements)
  - [3.1 Functional Requirements](#31-functional-requirements)
  - [3.2 Non-Functional Requirements](#32-non-functional-requirements)
- [4. 🏗️ Technical Architecture](#4-️-technical-architecture)
  - [4.1 System Architecture](#41-system-architecture)
  - [4.2 Technology Stack](#42-technology-stack)
  - [4.3 Database Design](#43-database-design)
  - [4.4 API Design](#44-api-design)
- [5. 🧠 Core Algorithms](#5--core-algorithms)
  - [5.1 Adaptive Placement Algorithm](#51-adaptive-placement-algorithm)
  - [5.2 Deduplication Strategy](#52-deduplication-strategy)
  - [5.3 Quota Management](#53-quota-management)
  - [5.4 Retry & Failover Logic](#54-retry--failover-logic)
- [6. 🔒 Security & Privacy](#6--security--privacy)
  - [6.1 Authentication](#61-authentication)
  - [6.2 Data Protection](#62-data-protection)
  - [6.3 Storage Isolation](#63-storage-isolation)
- [7. 🎨 User Interface](#7--user-interface)
  - [7.1 User Workflows](#71-user-workflows)
  - [7.2 Wireframes](#72-wireframes)
  - [7.3 Error Handling](#73-error-handling)
- [8. 📅 Development Plan](#8--development-plan)
  - [8.1 MVP Roadmap](#81-mvp-roadmap)
  - [8.2 Sprint Breakdown](#82-sprint-breakdown)
  - [8.3 Testing Strategy](#83-testing-strategy)
- [9. 📚 Appendices](#9--appendices)

---

# 1. 🎯 Introduction

## 1.1 Purpose

This Software Requirements Specification (SRS) provides a **comprehensive blueprint** for **TripVault** - a distributed cloud storage pooling platform designed for group travel scenarios.

### 🎯 What This Document Provides:

- ✅ Complete functional and non-functional requirements
- ✅ Detailed system architecture and design decisions
- ✅ Algorithm specifications with examples
- ✅ Database schema and API contracts
- ✅ Security and privacy considerations
- ✅ Development roadmap and timelines

### 👥 Target Audience:

- **Software Engineers** - Implementation guide
- **System Architects** - Design validation
- **QA Engineers** - Test case development
- **Recruiters/Interviewers** - Technical assessment
- **Product Managers** - Feature prioritization

---

## 1.2 Scope

### ✅ In Scope (MVP - Phase 1)

| Feature Category   | Details                                                |
| ------------------ | ------------------------------------------------------ |
| **Platform**       | Web application (responsive design)                    |
| **Authentication** | Google OAuth 2.0                                       |
| **Storage**        | Google Drive integration                               |
| **Core Features**  | Trip management, file upload/download, storage pooling |
| **Algorithm**      | Adaptive placement (single-owner)                      |
| **Analytics**      | Basic storage tracking                                 |
| **Security**       | OAuth token encryption, HTTPS                          |

### ❌ Out of Scope (Phase 2+)

| Feature              | Reason Deferred                |
| -------------------- | ------------------------------ |
| Native Mobile Apps   | Focus on web MVP first         |
| Multi-cloud Support  | Google Drive validation first  |
| Multi-owner Chunking | Complex, handles <5% use cases |
| Payment Processing   | Free tier only for MVP         |
| Video Compression    | Third-party tools available    |
| P2P File Transfer    | Requires WebRTC, complex       |

---

## 1.3 Intended Audience

### 📊 Document Usage Guide

| Reader Type          | Primary Sections                   | What to Focus On                    |
| -------------------- | ---------------------------------- | ----------------------------------- |
| **Developers**       | Architecture, Algorithms, API      | Implementation details, code specs  |
| **Architects**       | System Design, Database Schema     | Scalability, design patterns        |
| **Interviewers**     | Problem Statement, Core Innovation | Unique approach, technical depth    |
| **QA Engineers**     | Requirements, Error Handling       | Test scenarios, acceptance criteria |
| **Product Managers** | Features, User Workflows           | User value, priorities              |

---

# 2. 🌍 Overall Description

## 2.1 Problem Statement

### 🚨 The Current Pain Points

When groups travel together, they face significant challenges in sharing and storing trip media:

<table>
<tr>
<th width="30%">Problem</th>
<th width="70%">Description</th>
</tr>
<tr>
<td>🗃️ <b>Individual Storage Limits</b></td>
<td>One person's cloud storage fills up quickly, blocking uploads for the entire group</td>
</tr>
<tr>
<td>😵 <b>Chaotic Sharing</b></td>
<td>Files scattered across WhatsApp (compressed), email (size limits), multiple platforms</td>
</tr>
<tr>
<td>📂 <b>Fragmented Collections</b></td>
<td>Photos/videos scattered across different devices with no central, organized repository</td>
</tr>
<tr>
<td>🔄 <b>Duplicate Files</b></td>
<td>Same photo/video stored multiple times across different accounts, wasting space</td>
</tr>
<tr>
<td>🚫 <b>Access Barriers</b></td>
<td>Members without sufficient storage cannot receive all files</td>
</tr>
<tr>
<td>👤 <b>Single Point of Failure</b></td>
<td>Heavy reliance on one person to collect and distribute all media</td>
</tr>
</table>

### 📊 Real-World Impact

```
Typical 3-Day Trip (5 People):
├── 500 Photos × 5 MB each = 2.5 GB
├── 50 Videos × 200 MB each = 10 GB
└── 5 Long Videos × 2 GB = 10 GB
    ────────────────────────────
    Total: ~22.5 GB

Problem:
❌ Usually 1-2 people run out of storage
❌ Files shared via WhatsApp get compressed (quality loss)
❌ Takes 2-3 weeks to finally collect everything
❌ Some files never shared due to size limits
```

---

## 2.2 Solution Overview

### 💡 The TripVault Innovation

TripVault solves this by **decoupling who uploads from where files are stored**.

#### 🔄 Traditional vs TripVault Model

```
┌─────────────────────────────────────────────────────────┐
│                  TRADITIONAL MODEL                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Alice uploads photo.jpg                                │
│         ↓                                               │
│  Stored in Alice's Google Drive                         │
│         ↓                                               │
│  Alice's quota consumed                                 │
│                                                         │
│  Problem: Alice's storage fills up!                     │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   TRIPVAULT MODEL                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Alice uploads photo.jpg                                │
│         ↓                                               │
│  TripVault Placement Algorithm                          │
│         ↓                                               │
│  Analyzes: Who has space? Who used least?               │
│         ↓                                               │
│  Decision: Store in Bob's Drive                         │
│         ↓                                               │
│  Bob's quota consumed (not Alice's!)                    │
│                                                         │
│  Result: Fair distribution, no single bottleneck        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 🎯 Core Innovation

> **"Pool storage from multiple users into a single virtual shared drive"**

| Concept         | Traditional Cloud       | TripVault                 |
| --------------- | ----------------------- | ------------------------- |
| **Ownership**   | Single owner            | Distributed across group  |
| **Quota Limit** | Individual quota        | Sum of all allocations    |
| **Burden**      | Falls on one person     | Shared fairly             |
| **Scalability** | Limited by one account  | Grows with group size     |
| **Failure**     | Single point of failure | Resilient (auto-failover) |

---

## 2.3 Product Functions

### 🎯 Primary Features

<details open>
<summary><b>1. 🗺️ Trip Management</b></summary>

- Create trips with name, dates, description
- Invite members via email (automatic notifications)
- Join multiple trips simultaneously
- Archive old trips (preserve access to files)
- Delete trips (with orphaned file warnings)

**User Value:** Organize memories by event, not device

</details>

<details open>
<summary><b>2. 💾 Storage Pooling</b></summary>

- Members pledge portion of their Google Drive (e.g., "I'll contribute 3 GB")
- Real-time pool capacity calculation
- Visual dashboard showing pool utilization
- Dynamic max file size based on largest member's space

**User Value:** Turn "I don't have space" into "We have space"

</details>

<details open>
<summary><b>3. ⬆️ Intelligent File Upload</b></summary>

- Drag-and-drop or file picker interface
- Batch upload (10, 50, 100 files at once)
- Client-side hash calculation (deduplication)
- Automatic placement via smart algorithm
- Progress tracking with retry/failover
- Pre-upload validation (size, duplicates)

**User Value:** Upload once, accessible to all forever

</details>

<details open>
<summary><b>4. ⬇️ Unified File Access</b></summary>

- Gallery view of ALL trip files (regardless of who uploaded)
- Filter by date, uploader, file type
- Single-file or bulk download (ZIP)
- Streaming download (no server bottleneck)
- Thumbnail previews

**User Value:** One place for all trip memories

</details>

<details open>
<summary><b>5. 🧠 Adaptive Placement</b></summary>

- Small files (<100 MB): Balanced round-robin
- Medium files (100 MB - 1 GB): Balanced best-fit
- Large files (>1 GB): Least-used-first
- Automatic failover on upload failures

**User Value:** Fair distribution, zero manual management

</details>

<details open>
<summary><b>6. 📊 Storage Analytics</b> (Future)</summary>

- Who contributed most storage?
- Who uploaded most content?
- Storage usage trends
- Fair contribution visualization

**User Value:** Transparency and appreciation

</details>

---

## 2.4 User Personas

### 👤 Primary Persona: Trip Participant

```
Name: Priya, 28
Occupation: Marketing Manager
Tech Savvy: ⭐⭐⭐⚪⚪ (Moderate)

Background:
├── Goes on 3-4 trips per year with friends
├── Uses Google Drive for work, WhatsApp for sharing
└── Phone storage always near full (128 GB device)

Pain Points:
❌ "I can't receive all the videos - no space!"
❌ "WhatsApp compresses photos, quality is ruined"
❌ "I'm still waiting for trip photos from 2 months ago"

Goals:
✅ Easy access to ALL trip photos/videos
✅ Good quality (no compression)
✅ No manual file management
✅ Works on mobile browser

How TripVault Helps:
→ Contribute 2 GB from her Drive (she has 8 GB free)
→ Access 10 GB pool from entire group
→ Upload/download from mobile browser
→ No storage worry, no quality loss
```

### 👤 Secondary Persona: Trip Organizer

```
Name: Rahul, 32
Occupation: Software Engineer
Tech Savvy: ⭐⭐⭐⭐⭐ (High)

Background:
├── Always the "trip planner" in friend groups
├── Creates Google Drive folders, manages sharing
└── Comfortable with cloud services, APIs

Pain Points:
❌ "My Drive is always full from being the 'collector'"
❌ "I have to manually organize and share files"
❌ "Hard to track who has space, who uploaded what"

Goals:
✅ Centralized control over trip content
✅ Fair distribution of storage burden
✅ Automated file organization
✅ Analytics (who contributed what)

How TripVault Helps:
→ Creates trip, invites members automatically
→ Storage burden distributed (not just his Drive)
→ Dashboard shows who stored what
→ Analytics for transparency
```

### 👤 Tertiary Persona: Casual Member

```
Name: Ananya, 24
Occupation: Teacher
Tech Savvy: ⭐⭐⚪⚪⚪ (Low-Moderate)

Background:
├── Joins trips but rarely uploads photos
├── Prefers downloading over uploading
└── Not tech-savvy (uses apps, doesn't configure)

Pain Points:
❌ "Too complicated to set up cloud sharing"
❌ "I just want to download the photos"
❌ "Don't know how much space to 'allocate'"

Goals:
✅ Simple one-click download
✅ No configuration needed
✅ Works like "normal" apps

How TripVault Helps:
→ Joins via email invitation link (one click)
→ Allocates 1 GB (system suggests amount)
→ Downloads all photos in one ZIP
→ Minimal effort, maximum benefit
```

---

# 3. ⚙️ System Features & Requirements

## 3.1 Functional Requirements

### 🔐 FR-1: User Authentication

<table>
<tr>
<th width="30%">Requirement ID</th>
<th width="70%">Description</th>
</tr>
<tr>
<td><b>FR-1.1</b></td>
<td>System SHALL support Google OAuth 2.0 authentication</td>
</tr>
<tr>
<td><b>FR-1.2</b></td>
<td>System SHALL request minimal OAuth scopes (<code>drive.appdata</code>, <code>drive.file</code>)</td>
</tr>
<tr>
<td><b>FR-1.3</b></td>
<td>OAuth tokens SHALL be encrypted (AES-256) before database storage</td>
</tr>
<tr>
<td><b>FR-1.4</b></td>
<td>System SHALL automatically refresh expired tokens without user intervention</td>
</tr>
<tr>
<td><b>FR-1.5</b></td>
<td>Users SHALL be able to revoke app access (triggers cleanup)</td>
</tr>
</table>

**Priority:** 🔴 CRITICAL

**Acceptance Criteria:**

- ✅ User logs in with Google in ≤3 clicks
- ✅ OAuth consent shows ONLY app folder access (not full Drive)
- ✅ Token refresh happens automatically (no user action)
- ✅ Revoked access cleans up within 24 hours

---

### 🗺️ FR-2: Trip Management

<table>
<tr>
<th width="30%">Requirement ID</th>
<th width="70%">Description</th>
</tr>
<tr>
<td><b>FR-2.1</b></td>
<td>Users SHALL create trips with name, dates, description</td>
</tr>
<tr>
<td><b>FR-2.2</b></td>
<td>Trip owners SHALL invite members via email</td>
</tr>
<tr>
<td><b>FR-2.3</b></td>
<td>Invited members SHALL receive email with join link</td>
</tr>
<tr>
<td><b>FR-2.4</b></td>
<td>Users SHALL join multiple trips simultaneously</td>
</tr>
<tr>
<td><b>FR-2.5</b></td>
<td>Trip owners SHALL archive or delete trips</td>
</tr>
<tr>
<td><b>FR-2.6</b></td>
<td>Deleting trip SHALL NOT delete files from members' Drives (orphan files)</td>
</tr>
</table>

**Priority:** 🟠 HIGH

**Acceptance Criteria:**

- ✅ Trip creation completes in ≤5 seconds
- ✅ Email invitations sent within 1 minute
- ✅ Users see list of all trips (active + archived)
- ✅ Deleted trips show warning about orphaned files

---

### 💾 FR-3: Storage Allocation

<table>
<tr>
<th width="30%">Requirement ID</th>
<th width="70%">Description</th>
</tr>
<tr>
<td><b>FR-3.1</b></td>
<td>Members SHALL specify storage allocation in GB</td>
</tr>
<tr>
<td><b>FR-3.2</b></td>
<td>System SHALL validate allocation against real Drive free space</td>
</tr>
<tr>
<td><b>FR-3.3</b></td>
<td>System SHALL calculate total pool capacity (sum of allocations)</td>
</tr>
<tr>
<td><b>FR-3.4</b></td>
<td>Pool usage SHALL display in real-time</td>
</tr>
<tr>
<td><b>FR-3.5</b></td>
<td>Members SHALL modify allocation anytime</td>
</tr>
<tr>
<td><b>FR-3.6</b></td>
<td>Reducing allocation below current usage SHALL be prevented</td>
</tr>
</table>

**Priority:** 🔴 CRITICAL

**Acceptance Criteria:**

- ✅ UI shows current Drive free space during allocation
- ✅ Pool capacity updates within 5 seconds
- ✅ Visual progress bar shows utilization %
- ✅ Error if allocation exceeds available space

---

### ⬆️ FR-4: File Upload

<table>
<tr>
<th width="30%">Requirement ID</th>
<th width="70%">Description</th>
</tr>
<tr>
<td><b>FR-4.1</b></td>
<td>Users SHALL upload via drag-and-drop or file picker</td>
</tr>
<tr>
<td><b>FR-4.2</b></td>
<td>System SHALL support batch upload (multiple files)</td>
</tr>
<tr>
<td><b>FR-4.3</b></td>
<td>System SHALL calculate SHA-256 hash for deduplication</td>
</tr>
<tr>
<td><b>FR-4.4</b></td>
<td>Duplicate files SHALL NOT be uploaded (link to existing)</td>
</tr>
<tr>
<td><b>FR-4.5</b></td>
<td>System SHALL display dynamic max file size before upload</td>
</tr>
<tr>
<td><b>FR-4.6</b></td>
<td>Files exceeding max size SHALL be rejected with clear message</td>
</tr>
<tr>
<td><b>FR-4.7</b></td>
<td>System SHALL show upload progress percentage</td>
</tr>
<tr>
<td><b>FR-4.8</b></td>
<td>Failed uploads SHALL retry once, then auto-failover</td>
</tr>
</table>

**Priority:** 🔴 CRITICAL

**Acceptance Criteria:**

- ✅ Deduplication check completes in ≤2 seconds
- ✅ Progress bar updates every second
- ✅ Retry/failover happens automatically
- ✅ User sees specific error messages

---

### 🧠 FR-5: Adaptive Placement Algorithm

<table>
<tr>
<th width="30%">Requirement ID</th>
<th width="70%">Description</th>
</tr>
<tr>
<td><b>FR-5.1</b></td>
<td>System SHALL implement adaptive placement based on file size</td>
</tr>
<tr>
<td><b>FR-5.2</b></td>
<td>Small files (<100 MB) SHALL use balanced round-robin</td>
</tr>
<tr>
<td><b>FR-5.3</b></td>
<td>Medium files (100 MB - 1 GB) SHALL use balanced best-fit</td>
</tr>
<tr>
<td><b>FR-5.4</b></td>
<td>Large files (>1 GB) SHALL use least-used-first</td>
</tr>
<tr>
<td><b>FR-5.5</b></td>
<td>Placement SHALL consider usage ratio for fairness</td>
</tr>
<tr>
<td><b>FR-5.6</b></td>
<td>Tie-breaking SHALL use least-recently-used (LRU)</td>
</tr>
<tr>
<td><b>FR-5.7</b></td>
<td>System SHALL use optimistic locking (prevent race conditions)</td>
</tr>
</table>

**Priority:** 🔴 CRITICAL

**Acceptance Criteria:**

- ✅ Placement decision completes in ≤500ms
- ✅ Storage usage balanced within ±10% across members
- ✅ Concurrent uploads never exceed quotas
- ✅ Algorithm is explainable to users

---

### ⬇️ FR-6: File Download

<table>
<tr>
<th width="30%">Requirement ID</th>
<th width="70%">Description</th>
</tr>
<tr>
<td><b>FR-6.1</b></td>
<td>Users SHALL see unified gallery of all trip files</td>
</tr>
<tr>
<td><b>FR-6.2</b></td>
<td>Files SHALL be downloadable individually or in bulk (ZIP)</td>
</tr>
<tr>
<td><b>FR-6.3</b></td>
<td>System SHALL stream files (no server-side caching)</td>
</tr>
<tr>
<td><b>FR-6.4</b></td>
<td>Downloads SHALL support resumable transfers</td>
</tr>
<tr>
<td><b>FR-6.5</b></td>
<td>Gallery SHALL support filtering (date, uploader, type)</td>
</tr>
<tr>
<td><b>FR-6.6</b></td>
<td>Gallery SHALL display thumbnails for images/videos</td>
</tr>
</table>

**Priority:** 🟠 HIGH

**Acceptance Criteria:**

- ✅ Gallery loads in ≤3 seconds (500 files)
- ✅ Bulk download creates ZIP efficiently
- ✅ Download speed matches Drive native (±10%)
- ✅ Filters apply in ≤1 second

---

### 📊 FR-7: Quota Management

<table>
<tr>
<th width="30%">Requirement ID</th>
<th width="70%">Description</th>
</tr>
<tr>
<td><b>FR-7.1</b></td>
<td>System SHALL sync real Drive quotas every 6 hours</td>
</tr>
<tr>
<td><b>FR-7.2</b></td>
<td>System SHALL reserve space during upload (prevent over-allocation)</td>
</tr>
<tr>
<td><b>FR-7.3</b></td>
<td>Reserved space SHALL be released on completion/failure</td>
</tr>
<tr>
<td><b>FR-7.4</b></td>
<td>System SHALL warn if real free space < allocated</td>
</tr>
<tr>
<td><b>FR-7.5</b></td>
<td>Placement SHALL skip members with insufficient real space</td>
</tr>
</table>

**Priority:** 🟠 HIGH

**Acceptance Criteria:**

- ✅ Quota sync completes in ≤30 seconds per member
- ✅ Reserved space never causes overflow
- ✅ Warnings shown within 1 hour of detection

---

## 3.2 Non-Functional Requirements

### ⚡ NFR-1: Performance

| Metric           | Target                      | Measurement                      |
| ---------------- | --------------------------- | -------------------------------- |
| **Page Load**    | ≤2s initial, ≤1s subsequent | Lighthouse Performance Score >90 |
| **API Response** | p50: ≤200ms, p95: ≤500ms    | APM monitoring                   |
| **Upload Speed** | Match Google Drive (±10%)   | Comparative testing              |
| **Gallery Load** | ≤3s for 500 files           | End-to-end testing               |
| **Throughput**   | 100 concurrent uploads      | Load testing                     |
| **Daily Users**  | 1,000 (MVP target)          | Analytics                        |

---

### 🛡️ NFR-2: Reliability

| Aspect                   | Target                        | Implementation                         |
| ------------------------ | ----------------------------- | -------------------------------------- |
| **Availability**         | 99% uptime                    | Multi-region deployment                |
| **Data Integrity**       | Zero data loss                | Files in user Drives (not our servers) |
| **Backups**              | Daily (30-day retention)      | Automated PostgreSQL backups           |
| **Error Recovery**       | Automatic retry               | Retry logic + failover                 |
| **Graceful Degradation** | Read-only mode during outages | Feature flags                          |

---

### 🔒 NFR-3: Security

| Requirement        | Implementation            | Standard              |
| ------------------ | ------------------------- | --------------------- |
| **Authentication** | OAuth 2.0 only            | RFC 6749              |
| **Session**        | JWT, 7-day expiry         | HS256 algorithm       |
| **Token Storage**  | AES-256 encryption        | FIPS 140-2            |
| **Transport**      | HTTPS/TLS 1.2+            | Mozilla Modern Config |
| **Authorization**  | Role-based (owner/member) | RBAC                  |
| **Privacy**        | Minimal data collection   | GDPR compliant        |

---

### 👥 NFR-4: Usability

| Criteria             | Target                     | How Measured        |
| -------------------- | -------------------------- | ------------------- |
| **Learnability**     | First upload in ≤5 minutes | User testing        |
| **Efficiency**       | Common tasks in ≤3 clicks  | Click-path analysis |
| **Error Prevention** | Client-side validation     | Form validation     |
| **Help**             | Contextual tooltips        | In-app guidance     |
| **Accessibility**    | WCAG 2.1 Level AA          | Automated testing   |

---

# 4. 🏗️ Technical Architecture

## 4.1 System Architecture

### 🎨 High-Level Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                        USER LAYER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │  Desktop    │  │   Tablet    │  │   Mobile    │           │
│  │  Browser    │  │   Browser   │  │   Browser   │           │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘           │
└─────────┼─────────────────┼─────────────────┼──────────────────┘
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
                    HTTPS (TLS 1.2+)
                            │
                            ▼
┌────────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │            Next.js Frontend (Vercel)                     │ │
│  │  ┌────────────────────────────────────────────────────┐ │ │
│  │  │  • React Components (TypeScript)                   │ │ │
│  │  │  • Server-Side Rendering (SSR)                     │ │ │
│  │  │  • Static Generation (SSG)                         │ │ │
│  │  │  • Client-Side SHA-256 Hashing                     │ │ │
│  │  │  • Tailwind CSS Styling                            │ │ │
│  │  └────────────────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────┬───────────────────────────────────────┘
                         │
                  REST API (JSON)
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                            │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │         FastAPI Backend (AWS EC2 / Railway)              │ │
│  │  ┌────────────────────────────────────────────────────┐ │ │
│  │  │  API Endpoints:                                     │ │ │
│  │  │  • /auth/*      → OAuth & Session Management       │ │ │
│  │  │  • /trips/*     → Trip CRUD Operations             │ │ │
│  │  │  • /files/*     → Upload/Download/Delete           │ │ │
│  │  │  • /analytics/* → Storage Insights                 │ │ │
│  │  └────────────────────────────────────────────────────┘ │ │
│  │  ┌────────────────────────────────────────────────────┐ │ │
│  │  │  Business Logic:                                    │ │ │
│



# 🚀 TripVault SRS - Part 2: Algorithms & Implementation

## Table of Contents
- [Core Algorithms](#-5-core-algorithms)
- [Security & Privacy](#-6-security--privacy)
- [User Interface](#-7-user-interface)
- [Development Plan](#-8-development-plan)
- [Appendices](#-9-appendices)

---

# 🧠 5. Core Algorithms

## 5.1 Adaptive Placement Algorithm

### 📖 Algorithm Overview

The **Adaptive Placement Algorithm** is the heart of TripVault. It determines which group member's Google Drive should store each uploaded file.

#### 🎯 Design Goals

| Goal | Description | Impact |
|------|-------------|--------|
| **⚖️ Fairness** | Distribute storage burden evenly | No single member overloaded |
| **⚡ Efficiency** | Minimize fragmentation | Support large files later |
| **🎲 Adaptability** | Different strategies for different file sizes | Optimal for all use cases |
| **🛡️ Resilience** | Handle edge cases gracefully | Concurrent uploads, failures |

---

### 📊 Three Strategies by File Size

```

┌─────────────────────────────────────────────────────────────┐
│ ADAPTIVE STRATEGY SELECTION │
├─────────────────────────────────────────────────────────────┤
│ │
│ File Size Strategy Goal │
│ ───────────────────────────────────────────────────────── │
│ │
│ 📸 Small Balanced Fair │
│ (<100 MB) Round-Robin Distribution│
│ Photos, docs │
│ │
│ 🎥 Medium Balanced Balance │
│ (100 MB - 1 GB) Best-Fit Fairness + │
│ Short videos Efficiency │
│ │
│ 🎬 Large Least-Used Maximum │
│ (>1 GB) First Success │
│ Long videos, raw Rate │
│ │
└─────────────────────────────────────────────────────────────┘

````

---

### 🔢 Algorithm Specification

```python
ALGORITHM: Adaptive Balanced Placement

# ============================================================
# INPUT
# ============================================================
file_size: int          # File size in bytes
trip_members: List[Member]  # All trip members with quotas

# ============================================================
# OUTPUT
# ============================================================
selected_member: Member  # Member to store the file
OR
PlacementError: Exception  # If no space available

# ============================================================
# STEP 1: Filter Candidates
# ============================================================
candidates = []

FOR EACH member IN trip_members:

    # Skip inactive members
    IF member.status != 'active':
        CONTINUE

    # Calculate available space
    available = member.allocated_limit_bytes
                - member.used_bytes
                - member.reserved_bytes

    # Consider real Drive space (prevent over-allocation)
    IF member.real_free_bytes IS NOT NULL:
        available = MIN(available, member.real_free_bytes)

    # Only consider if member can fit the file
    IF available >= file_size:
        candidates.APPEND({
            member: member,
            available: available,
            usage_ratio: member.used_bytes / member.allocated_limit_bytes
        })

# No candidates found
IF candidates.LENGTH == 0:
    RAISE PlacementError("No space available in pool")

# ============================================================
# STEP 2: Categorize File & Select Strategy
# ============================================================
IF file_size < 104_857_600:  # 100 MB
    strategy = "BALANCED_ROUND_ROBIN"

ELIF file_size < 1_073_741_824:  # 1 GB
    strategy = "BALANCED_BEST_FIT"

ELSE:  # >= 1 GB
    strategy = "LEAST_USED_FIRST"

# ============================================================
# STEP 3: Apply Strategy
# ============================================================

# ─────────────────────────────────────────────────────────
# Strategy 1: BALANCED_ROUND_ROBIN (Small Files)
# ─────────────────────────────────────────────────────────
IF strategy == "BALANCED_ROUND_ROBIN":

    # Find member with LOWEST usage ratio
    min_ratio = MIN(c.usage_ratio FOR c IN candidates)

    # Get all members with minimum ratio (may be ties)
    tied_candidates = [c FOR c IN candidates
                       WHERE c.usage_ratio == min_ratio]

    IF tied_candidates.LENGTH == 1:
        selected = tied_candidates[0]
    ELSE:
        # Tie-breaker: Least Recently Used (LRU)
        selected = member WITH oldest last_used_at FROM tied_candidates

# ─────────────────────────────────────────────────────────
# Strategy 2: BALANCED_BEST_FIT (Medium Files)
# ─────────────────────────────────────────────────────────
ELIF strategy == "BALANCED_BEST_FIT":

    max_available = MAX(c.available FOR c IN candidates)

    FOR EACH candidate IN candidates:
        # Balance score: Higher if less used
        balance_score = 1 - candidate.usage_ratio

        # Efficiency score: Higher if more space available
        efficiency_score = candidate.available / max_available

        # Weighted combination: 60% balance, 40% efficiency
        candidate.final_score = (0.6 * balance_score) +
                                (0.4 * efficiency_score)

    # Select member with highest score
    selected = candidate WITH MAX(final_score)

# ─────────────────────────────────────────────────────────
# Strategy 3: LEAST_USED_FIRST (Large Files)
# ─────────────────────────────────────────────────────────
ELSE:  # LEAST_USED_FIRST

    FOR EACH candidate IN candidates:
        # Balance score: Higher if less used
        balance_score = 1 - candidate.usage_ratio

        # Capacity score: How much room left after storing file
        capacity_score = candidate.available / file_size

        # Weighted combination: 70% balance, 30% capacity
        candidate.final_score = (0.7 * balance_score) +
                                (0.3 * capacity_score)

    # Select member with highest score
    selected = candidate WITH MAX(final_score)

# ============================================================
# STEP 4: Reserve Space (Optimistic Locking)
# ============================================================
BEGIN DATABASE TRANSACTION:

    # Re-check availability (prevent race conditions)
    current_available = selected.member.allocated_limit_bytes
                        - selected.member.used_bytes
                        - selected.member.reserved_bytes

    # Another upload consumed space while we were deciding
    IF current_available < file_size:
        ROLLBACK TRANSACTION
        # Retry from beginning with updated state
        GOTO STEP 1

    # Reserve space to prevent other uploads from using it
    UPDATE trip_members
    SET reserved_bytes = reserved_bytes + file_size,
        last_used_at = CURRENT_TIMESTAMP
    WHERE id = selected.member.id

COMMIT TRANSACTION

# ============================================================
# STEP 5: Return Selected Member
# ============================================================
RETURN selected.member
````

---

### 📈 Example Walkthrough

#### Scenario Setup

```yaml
Trip: "Goa Beach Trip 2025"

Members:
  - Alice:
      allocated: 5 GB
      used: 1 GB
      reserved: 0 GB
      usage_ratio: 20%

  - Bob:
      allocated: 5 GB
      used: 2 GB
      reserved: 0 GB
      usage_ratio: 40%

  - Carol:
      allocated: 5 GB
      used: 3 GB
      reserved: 0 GB
      usage_ratio: 60%

Upload Request: sunset_video.mp4 (500 MB)
Category: Medium File (100 MB - 1 GB)
```

#### Step-by-Step Execution

**STEP 1: Filter Candidates**

```
Alice: available = 5 GB - 1 GB - 0 GB = 4 GB ✅ (>= 500 MB)
Bob:   available = 5 GB - 2 GB - 0 GB = 3 GB ✅ (>= 500 MB)
Carol: available = 5 GB - 3 GB - 0 GB = 2 GB ✅ (>= 500 MB)

All three members can store the file!
```

**STEP 2: Select Strategy**

```
File size = 500 MB
Category: Medium File (100 MB < 500 MB < 1 GB)
Strategy: BALANCED_BEST_FIT
```

**STEP 3: Calculate Scores**

```
max_available = 4 GB (Alice has most space)

┌────────┬────────────────┬──────────────────┬─────────────┐
│ Member │ Balance Score  │ Efficiency Score │ Final Score │
├────────┼────────────────┼──────────────────┼─────────────┤
│ Alice  │ 1 - 0.20 = 0.80│ 4/4 = 1.00       │ 0.88 ⭐     │
│        │                │                  │ (Highest)   │
├────────┼────────────────┼──────────────────┼─────────────┤
│ Bob    │ 1 - 0.40 = 0.60│ 3/4 = 0.75       │ 0.66        │
├────────┼────────────────┼──────────────────┼─────────────┤
│ Carol  │ 1 - 0.60 = 0.40│ 2/4 = 0.50       │ 0.44        │
└────────┴────────────────┴──────────────────┴─────────────┘

Alice Score = (0.6 × 0.80) + (0.4 × 1.00) = 0.88
Bob Score   = (0.6 × 0.60) + (0.4 × 0.75) = 0.66
Carol Score = (0.6 × 0.40) + (0.4 × 0.50) = 0.44

Winner: Alice (highest score)
```

**STEP 4: Reserve Space**

```sql
BEGIN TRANSACTION;

-- Re-check Alice's availability (race condition protection)
SELECT allocated_limit_bytes - used_bytes - reserved_bytes
FROM trip_members
WHERE user_id = 'alice_id';
-- Result: 4 GB ✅ (still enough)

-- Reserve space
UPDATE trip_members
SET reserved_bytes = reserved_bytes + 524288000,  -- 500 MB
    last_used_at = NOW()
WHERE user_id = 'alice_id';

COMMIT;
```

**STEP 5: Result**

```
✅ File will be uploaded to Alice's Google Drive
✅ Alice's reserved space increased by 500 MB
✅ Other members remain untouched

After Upload Completes:
┌────────┬───────────┬──────────┬───────────┬─────────────┐
│ Member │ Allocated │ Used     │ Reserved  │ Usage Ratio │
├────────┼───────────┼──────────┼───────────┼─────────────┤
│ Alice  │ 5 GB      │ 1.5 GB   │ 0 GB      │ 30%         │
│ Bob    │ 5 GB      │ 2 GB     │ 0 GB      │ 40%         │
│ Carol  │ 5 GB      │ 3 GB     │ 0 GB      │ 60%         │
└────────┴───────────┴──────────┴───────────┴─────────────┘
```

---

### 🎨 Algorithm Flowchart

```
                    ┌─────────┐
                    │  START  │
                    └────┬────┘
                         │
                         ▼
            ┌────────────────────────┐
            │ Get All Trip Members   │
            └────────────┬───────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │ Filter Active Members  │
            │ WITH Enough Space      │
            └────────────┬───────────┘
                         │
                    ┌────┴────┐
                    │         │
                    ▼         ▼
            ┌──────────┐ ┌──────────┐
            │ Found?   │ │ Not Found│
            │   YES    │ │    NO    │
            └────┬─────┘ └────┬─────┘
                 │            │
                 │            ▼
                 │   ┌────────────────┐
                 │   │ ERROR:         │
                 │   │ No space       │
                 │   │ available      │
                 │   └────────────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │ Categorize File Size   │
    └────────────┬───────────┘
                 │
       ┌─────────┼─────────┐
       │         │         │
       ▼         ▼         ▼
  ┌────────┐┌────────┐┌────────┐
  │< 100MB ││100MB-1G││ > 1GB  │
  │        ││        ││        │
  │ Round  ││ Best   ││ Least  │
  │ Robin  ││  Fit   ││  Used  │
  └───┬────┘└───┬────┘└───┬────┘
      │         │         │
      └─────────┼─────────┘
                │
                ▼
    ┌────────────────────────┐
    │ Calculate Scores       │
    │ For All Candidates     │
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │ Select Highest Score   │
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │ BEGIN TRANSACTION      │
    └────────────┬───────────┘
                 │
                 ▼
    ┌────────────────────────┐
    │ Re-check Availability  │
    │ (Race Protection)      │
    └────────────┬───────────┘
                 │
          ┌──────┴──────┐
          │             │
          ▼             ▼
    ┌─────────┐   ┌─────────┐
    │ Still   │   │ Space   │
    │Available│   │  Gone   │
    └────┬────┘   └────┬────┘
         │             │
         │             ▼
         │      ┌───────────┐
         │      │ ROLLBACK  │
         │      │ & RETRY   │─┐
         │      └───────────┘ │
         │                    │
         ▼                    │
    ┌─────────┐              │
    │ Reserve │              │
    │  Space  │              │
    └────┬────┘              │
         │                    │
         ▼                    │
    ┌─────────┐              │
    │ COMMIT  │              │
    └────┬────┘              │
         │                    │
         ▼                    │
    ┌─────────┐              │
    │ RETURN  │◄─────────────┘
    │ Member  │
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │   END   │
    └─────────┘
```

---

## 5.2 Deduplication Strategy

### 🎯 Purpose

Prevent storing identical files multiple times within a trip, saving both storage space and upload bandwidth.

### 🔐 Hash-Based Deduplication

#### Why SHA-256?

| Property                | Benefit                              |
| ----------------------- | ------------------------------------ |
| **Deterministic**       | Same file always produces same hash  |
| **Collision-Resistant** | Probability of collision: 1 in 2^256 |
| **Fast**                | Modern browsers compute it quickly   |
| **Standard**            | Widely used, well-tested             |

#### Hash Calculation (Client-Side)

```javascript
// Client-side JavaScript (runs in browser)
async function calculateFileHash(file) {
  // Read file as ArrayBuffer
  const arrayBuffer = await file.arrayBuffer();

  // Compute SHA-256 hash
  const hashBuffer = await crypto.subtle.digest("SHA-256", arrayBuffer);

  // Convert to hex string
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");

  return hashHex;
}

// Example output:
// "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
```

**Why Client-Side?**

- ✅ Faster (no need to upload file first to check)
- ✅ Saves bandwidth (duplicate detected before upload)
- ✅ Better UX (instant feedback)

---

### 🔄 Deduplication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  UPLOAD WITH DEDUPLICATION                  │
└─────────────────────────────────────────────────────────────┘

User Selects File: beach_sunset.jpg
        │
        ▼
┌───────────────────────┐
│ 1. Calculate Hash     │  Client computes SHA-256
│    (Client-Side)      │  Result: "abc123def456..."
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ 2. Send to Backend    │  POST /files/upload
│    {                  │  Body: { hash: "abc123...",
│      hash,            │         filename, size }
│      filename,        │
│      size             │
│    }                  │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ 3. Check Database     │  SELECT * FROM virtual_files
│                       │  WHERE trip_id = X AND hash = Y
└──────────┬────────────┘
           │
      ┌────┴────┐
      │         │
      ▼ Found   ▼ Not Found
┌──────────┐  ┌────────────┐
│ DUPLICATE│  │ NEW FILE   │
└─────┬────┘  └─────┬──────┘
      │             │
      ▼             ▼
┌──────────────────────────────┐  ┌───────────────────────┐
│ 4a. Link to Existing         │  │ 4b. Proceed Upload    │
│                              │  │                       │
│ • Create virtual_file entry  │  │ • Run placement algo  │
│   (new uploader_id)          │  │ • Upload to Drive     │
│                              │  │ • Save metadata       │
│ • Reference same file_chunks │  │                       │
│   (no actual upload!)        │  │                       │
│                              │  │                       │
│ • No storage consumed        │  │                       │
└──────────────────────────────┘  └───────────────────────┘
      │                                    │
      ▼                                    │
┌──────────────────────────────────────────┘
│
▼
┌───────────────────────────────────────────┐
│ 5. Show Result to User                    │
│                                           │
│ Duplicate: "This file was already         │
│            uploaded by Alice on Feb 2"    │
│                                           │
│ New File: "Upload successful!"            │
└───────────────────────────────────────────┘
```

---

### 💾 Database Implementation

#### Unique Constraint (Prevents Duplicates)

```sql
-- Ensure only ONE file with this hash per trip
CREATE UNIQUE INDEX idx_virtualfiles_trip_hash
ON virtual_files(trip_id, hash);

-- Query to check for duplicates
SELECT
    id,
    filename,
    uploader_user_id,
    uploaded_at
FROM virtual_files
WHERE trip_id = $1 AND hash = $2
LIMIT 1;
```

#### When Duplicate Found

```sql
-- Option 1: Simple Linking (MVP)
-- Just create a virtual file entry, reference existing chunks

INSERT INTO virtual_files (
    trip_id,
    filename,
    original_name,
    total_size,
    mime_type,
    hash,
    uploader_user_id,
    status
) VALUES (
    'goa_trip_123',
    'beach_sunset_copy.jpg',  -- Different filename for new uploader
    'IMG_5678.jpg',           -- User's original filename
    5242880,                  -- Same size as existing
    'image/jpeg',
    'abc123def456...',        -- SAME HASH
    'bob_user_id',            -- Different uploader
    'complete'
);

-- No new file_chunks created!
-- Downloads will fetch chunks from existing file
```

---

### 📊 Storage Savings Example

**Scenario: 5 Users Upload Same Beach Photo**

```
Without Deduplication:
├── Alice uploads beach.jpg (10 MB) → Stored in Bob's Drive
├── Carol uploads beach.jpg (10 MB) → Stored in Dave's Drive
├── Dave uploads beach.jpg (10 MB)  → Stored in Eve's Drive
├── Eve uploads beach.jpg (10 MB)   → Stored in Alice's Drive
└── Bob uploads beach.jpg (10 MB)   → Stored in Carol's Drive
    ────────────────────────────────
    Total: 50 MB consumed

With Deduplication:
├── Alice uploads beach.jpg (10 MB) → Stored in Bob's Drive ✅
├── Carol uploads beach.jpg (10 MB) → DUPLICATE, linked to existing ✅
├── Dave uploads beach.jpg (10 MB)  → DUPLICATE, linked to existing ✅
├── Eve uploads beach.jpg (10 MB)   → DUPLICATE, linked to existing ✅
└── Bob uploads beach.jpg (10 MB)   → DUPLICATE, linked to existing ✅
    ────────────────────────────────
    Total: 10 MB consumed (80% savings!)
```

**Real-World Impact:**

- Common in group trips (everyone photos the same sunset, monument, etc.)
- Saves 50-80% storage in typical scenarios
- Instant uploads for duplicates (no actual upload needed)

---

## 5.3 Quota Management System

### 📊 Three Types of Quota

```
┌─────────────────────────────────────────────────────────────┐
│                     QUOTA TRACKING                          │
└─────────────────────────────────────────────────────────────┘

1️⃣ ALLOCATED QUOTA (User's Pledge)
   ─────────────────────────────────
   What user promised to contribute

   Example: Alice pledges 5 GB to the trip

   Storage: trip_members.allocated_limit_bytes

2️⃣ USED QUOTA (Actually Consumed)
   ─────────────────────────────────
   How much space is actually storing files

   Example: 23 files stored in Alice's Drive = 2.3 GB

   Calculation: SUM(file_chunks.chunk_size)
                WHERE owner_user_id = alice_id

3️⃣ RESERVED QUOTA (Temporarily Locked)
   ─────────────────────────────────
   Space locked during active uploads

   Example: 500 MB video uploading to Alice's Drive

   Purpose: Prevent other uploads from using same space

┌─────────────────────────────────────────────────────────────┐
│              AVAILABLE SPACE FORMULA                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Available = Allocated - Used - Reserved                    │
│                                                             │
│  Example:                                                   │
│  Available = 5 GB - 2.3 GB - 0.5 GB = 2.2 GB               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 🔄 Real Drive Quota Sync

**Why Sync?**
User might delete personal files outside TripVault → Real free space changes!

#### Background Job (Runs Every 6 Hours)

```python
# Pseudocode for quota sync job

async def sync_user_quota(user_id: str):
    """
    Fetch real Drive quota from Google API
    Update database with current free space
    """

    # 1. Get user's OAuth token
    credentials = await get_user_credentials(user_id)

    # 2. Call Google Drive API
    service = build('drive', 'v3', credentials=credentials)
    about = service.about().get(fields='storageQuota').execute()

    # 3. Parse response
    quota = about['storageQuota']
    #    {
    #      "limit": "16106127360",        # 15 GB total
    #      "usage": "5368709120",         # 5 GB used
    #      "usageInDrive": "4294967296",  # 4 GB in Drive
    #      "usageInDriveTrash": "1073741824" # 1 GB in trash
    #    }

    # 4. Calculate real free space
    limit = int(quota['limit'])
    usage = int(quota['usage'])
    real_free = limit - usage  # 15 GB - 5 GB = 10 GB

    # 5. Update database
    await db.execute("""
        UPDATE trip_members
        SET real_free_bytes = $1,
            last_quota_sync = NOW()
        WHERE user_id = $2
    """, real_free, user_id)

    # 6. Check for over-allocation
    member = await db.fetch_one("""
        SELECT allocated_limit_bytes, real_free_bytes
        FROM trip_members
        WHERE user_id = $1
    """, user_id)

    if member['allocated_limit_bytes'] > member['real_free_bytes']:
        # Send warning notification
        await notify_user(
            user_id,
            "Your Drive space decreased. "
            "Please adjust your allocation."
        )
```

#### Enhanced Placement Logic

```python
# When placing files, consider BOTH allocated and real space

def calculate_available_space(member):
    """
    Calculate truly available space
    (minimum of pledged space and real Drive space)
    """

    pledged_available = (member.allocated_limit_bytes
                        - member.used_bytes
                        - member.reserved_bytes)

    real_available = member.real_free_bytes

    # Use whichever is smaller (more conservative)
    return min(pledged_available, real_available)
```

---

### 🔒 Space Reservation Flow

```
┌─────────────────────────────────────────────────────────────┐
│            SPACE RESERVATION DURING UPLOAD                  │
└─────────────────────────────────────────────────────────────┘

State BEFORE Upload:
┌────────┬───────────┬──────────┬───────────┬───────────┐
│ Member │ Allocated │ Used     │ Reserved  │ Available │
├────────┼───────────┼──────────┼───────────┼───────────┤
│ Alice  │ 5 GB      │ 2 GB     │ 0 GB      │ 3 GB      │
└────────┴───────────┴──────────┴───────────┴───────────┘

User uploads 500 MB file → Placement selects Alice

Step 1: RESERVE SPACE
┌────────┬───────────┬──────────┬───────────┬───────────┐
│ Member │ Allocated │ Used     │ Reserved  │ Available │
├────────┼───────────┼──────────┼───────────┼───────────┤
│ Alice  │ 5 GB      │ 2 GB     │ 0.5 GB    │ 2.5 GB    │
└────────┴───────────┴──────────┴───────────┴───────────┘
                                   ↑ Locked!

Step 2: UPLOAD TO DRIVE
(500 MB uploading... other uploads see only 2.5 GB available)

Step 3a: Upload SUCCESS → Transfer Reserved to Used
┌────────┬───────────┬──────────┬───────────┬───────────┐
│ Member │ Allocated │ Used     │ Reserved  │ Available │
├────────┼───────────┼──────────┼───────────┼───────────┤
│ Alice  │ 5 GB      │ 2.5 GB   │ 0 GB      │ 2.5 GB    │
└────────┴───────────┴──────────┴───────────┴───────────┘
                        ↑ Updated    ↑ Released

Step 3b: Upload FAILS → Release Reserved
┌────────┬───────────┬──────────┬───────────┬───────────┐
│ Member │ Allocated │ Used     │ Reserved  │ Available │
├────────┼───────────┼──────────┼───────────┼───────────┤
│ Alice  │ 5 GB      │ 2 GB     │ 0 GB      │ 3 GB      │
└────────┴───────────┴──────────┴───────────┴───────────┘
                                   ↑ Released (back to original)
```

---

## 5.4 Retry & Failover Logic

### 🎯 Three-Tier Failure Handling

```
┌─────────────────────────────────────────────────────────────┐
│                 UPLOAD RETRY STRATEGY                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Tier 1: Immediate Retry (Same Member)                     │
│  ────────────────────────────────────────                  │
│  Attempts: 1 retry                                          │
│  Delay: 2 seconds                                           │
│  Use Case: Transient network glitches                       │
│                                                             │
│  Tier 2: Auto-Failover (Different Members)                 │
│  ────────────────────────────────────────                  │
│  Attempts: Up to 3 backup members                           │
│  Delay: 2 seconds between attempts                          │
│  Use Case: Primary member unavailable/quota exceeded        │
│                                                             │
│  Tier 3: Give Up                                            │
│  ────────────────────────────────────────                  │
│  Show error to user with actionable suggestions             │
│  Log failure for debugging                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 🔄 Complete Retry Flow

```python
FUNCTION: upload_with_retry(file, trip_id)

# ============================================================
# CONSTANTS
# ============================================================
MAX_RETRIES_SAME_MEMBER = 1
MAX_FAILOVER_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 2

# ============================================================
# STEP 1: Initial Placement
# ============================================================
primary_member = placement_algorithm(file.size, trip_id)

IF primary_member IS NULL:
    RETURN error("No space available in pool")

# Reserve space in primary member's quota
reserve_space(primary_member, file.size)

# ============================================================
# STEP 2: Attempt Upload to Primary Member
# ============================================================
result = attempt_upload(primary_member, file)

IF result.success:
    commit_upload(primary_member, file)
    RETURN success(file_id, stored_in=primary_member)

# First attempt failed
log(f"Upload failed: {result.error}")

# ============================================================
# STEP 3: Retry Same Member (Once)
# ============================================================
log("Upload failed, retrying same member after delay")
wait(RETRY_DELAY_SECONDS)

result = attempt_upload(primary_member, file)

IF result.success:
    commit_upload(primary_member, file)
    log("Retry successful")
    RETURN success(file_id, stored_in=primary_member)

# Second attempt also failed
log(f"Retry failed: {result.error}")

# ============================================================
# STEP 4: Auto-Failover to Backup Members
# ============================================================
log("Primary member failed twice, initiating failover")

# Release reservation from primary member
release_reservation(primary_member, file.size)

# Track which members we've already tried
excluded_members = [primary_member]
failover_count = 0

WHILE failover_count < MAX_FAILOVER_ATTEMPTS:

    # Get next best member (excluding failed ones)
    backup_member = placement_algorithm(
        file.size,
        trip_id,
        exclude=excluded_members
    )

    # No more candidates available
    IF backup_member IS NULL:
        BREAK

    log(f"Failover attempt {failover_count + 1}: trying {backup_member.name}")

    # Reserve space in backup member
    reserve_space(backup_member, file.size)

    # Attempt upload to backup
    result = attempt_upload(backup_member, file)

    IF result.success:
        commit_upload(backup_member, file)
        log(f"Failover successful to {backup_member.name}")

        # Notify user (optional)
        notify_user("Upload successful (used backup storage)")

        RETURN success(file_id, stored_in=backup_member)

    # This backup also failed
    log(f"Backup member {backup_member.name} failed: {result.error}")
    release_reservation(backup_member, file.size)

    # Add to exclusion list
    excluded_members.APPEND(backup_member)
    failover_count += 1

    # Wait before trying next backup
    wait(RETRY_DELAY_SECONDS)

# ============================================================
# STEP 5: All Attempts Exhausted
# ============================================================
log("All upload attempts failed")

RETURN error({
    code: "UPLOAD_FAILED",
    message: "Upload failed after multiple attempts",
    attempts: 1 + MAX_RETRIES_SAME_MEMBER + failover_count,
    suggestion: "Please check your connection and try again"
})
```

---

### 📊 Error Type Handling Matrix

| Error Type                   | Retry Same Member?    | Failover? | User Action Required   |
| ---------------------------- | --------------------- | --------- | ---------------------- |
| **🌐 Network Timeout**       | ✅ Yes (1x)           | ✅ Yes    | None (auto-handled)    |
| **🚫 Drive API Rate Limit**  | ✅ Yes (with backoff) | ❌ No     | Wait 1 minute          |
| **🔑 Invalid OAuth Token**   | ❌ No                 | ❌ No     | Re-authenticate        |
| **💾 Member Quota Exceeded** | ❌ No                 | ✅ Yes    | None (auto-failover)   |
| **📏 File Too Large**        | ❌ No                 | ❌ No     | Compress or split file |
| **🗃️ Member Drive Full**     | ❌ No                 | ✅ Yes    | None (auto-failover)   |
| **🔌 Connection Lost**       | ✅ Yes (1x)           | ✅ Yes    | Check connection       |
| **🏢 Drive API Down**        | ✅ Yes (backoff)      | ❌ No     | Try again later        |

---

### 🎬 Example Scenario: Upload with Failover

**Setup:**

```yaml
File: vacation_video.mp4 (1.5 GB)
Trip Members:
  - Alice: 2 GB available
  - Bob: 1 GB available (not enough!)
  - Carol: 3 GB available
  - Dave: 2.5 GB available
```

**Execution Timeline:**

```
00:00 - Placement Algorithm selects Alice (2 GB available)
00:01 - Reserve 1.5 GB in Alice's quota
00:02 - Begin upload to Alice's Drive...
00:45 - ❌ Upload FAILED (Network timeout)
        Error: "Connection reset by peer"

00:46 - TIER 1: Retry Same Member
        Waiting 2 seconds...
00:48 - Retry upload to Alice...
01:30 - ❌ Upload FAILED AGAIN (Timeout persists)
        Error: "Connection timeout"

01:31 - TIER 2: Auto-Failover Initiated
        Release Alice's reservation
        Exclude Alice from candidates

01:32 - Run placement algorithm (exclude Alice)
        Candidates: Carol (3 GB), Dave (2.5 GB)
        Selected: Carol (highest score)

01:33 - Reserve 1.5 GB in Carol's quota
01:34 - Begin upload to Carol's Drive...
02:50 - ✅ Upload SUCCESS!

02:51 - Commit metadata to database
        File stored in Carol's Drive
        User sees: "Upload successful (used backup storage)"
```

**User Experience:**

```
┌─────────────────────────────────────────┐
│ Uploading vacation_video.mp4...        │
│ ████████░░░░░░░░  45%                  │
│ ⏱️ 1 minute remaining                   │
└─────────────────────────────────────────┘
        ↓ (Upload fails)
┌─────────────────────────────────────────┐
│ Upload interrupted, retrying...         │
│ ████████░░░░░░░░  45%                  │
│ Attempt 1 of 2                          │
└─────────────────────────────────────────┘
        ↓ (Retry fails)
┌─────────────────────────────────────────┐
│ Switching to backup storage...          │
│ ██░░░░░░░░░░░░░░  10%                  │
│ (Restarting upload)                     │
└─────────────────────────────────────────┘
        ↓ (Success with Carol)
┌─────────────────────────────────────────┐
│ ✅ vacation_video.mp4 uploaded          │
│ (Used backup storage)                   │
└─────────────────────────────────────────┘
```

---

# 🔒 6. Security & Privacy

## 6.1 Authentication

### 🔐 Google OAuth 2.0 Flow

#### Complete Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  OAUTH 2.0 FLOW DIAGRAM                     │
└─────────────────────────────────────────────────────────────┘

User                TripVault          Google OAuth        Google Drive
  │                   │                     │                    │
  │  1. Click Login   │                     │                    │
  ├──────────────────>│                     │                    │
  │                   │                     │                    │
  │                   │  2. Redirect to     │                    │
  │                   │     Google OAuth    │                    │
  │                   ├────────────────────>│                    │
  │                   │                     │                    │
  │  3. Google Login  │                     │                    │
  │<──────────────────┼─────────────────────┤                    │
  │   (Email/Password)│                     │                    │
  │                   │                     │                    │
  │  4. Consent Screen│                     │                    │
  │     "TripVault    │                     │                    │
  │      wants to:    │                     │                    │
  │      - Store data"│                     │                    │
  │                   │                     │                    │
  │  5. Click "Allow" │                     │                    │
  ├──────────────────────────────────────>│                    │
  │                   │                     │                    │
  │                   │  6. Auth Code       │                    │
  │                   │<────────────────────┤                    │
  │  7. Redirect Back │                     │                    │
  │<──────────────────┤                     │                    │
  │  (with auth code) │                     │                    │
  │                   │                     │                    │
  │                   │  8. Exchange Code   │                    │
  │                   │     for Tokens      │                    │
  │                   ├────────────────────>│                    │
  │                   │                     │                    │
  │                   │  9. Access Token +  │                    │
  │                   │     Refresh Token   │                    │
  │                   │<────────────────────┤                    │
  │                   │                     │                    │
  │                   │ 10. Encrypt Tokens  │                    │
  │                   │     Store in DB     │                    │
  │                   │                     │                    │
  │ 11. Session Token │                     │                    │
  │    (JWT)          │                     │                    │
  │<──────────────────┤                     │                    │
  │                   │                     │                    │
  │ 12. Access App    │                     │                    │
  │    (use JWT for   │                     │                    │
  │     all requests) │                     │                    │
  │                   │                     │                    │
  │                   │ 13. Upload File     │                    │
  │                   │     (decrypt token) │                    │
  │                   ├─────────────────────┼───────────────────>│
  │                   │                     │  14. Store File    │
  │                   │                     │<───────────────────┤
  │                   │                     │                    │
```

---

### 📋 OAuth Scopes Requested

```
┌─────────────────────────────────────────────────────────────┐
│                 OAUTH SCOPES BREAKDOWN                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Scope                          | Access Level             │
│  ───────────────────────────────┼──────────────────────── │
│                                                             │
│  openid                         | User's Google ID         │
│  email                          | User's email address     │
│  profile                        | Name, profile picture    │
│                                                             │
│  drive.appdata                  | App's hidden folder ONLY │
│  (CRITICAL)                     | User CANNOT see/delete   │
│                                                             │
│  drive.file                     | Files created by app     │
│  (CRITICAL)                     | Not other Drive files    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

❌ NOT REQUESTED:
   drive                    (Full Drive access - too invasive)
   drive.readonly           (Don't need to read user's files)
   drive.metadata.readonly  (Don't need metadata access)
```

**What User Sees on Consent Screen:**

```
┌─────────────────────────────────────────┐
│  TripVault wants to access your         │
│  Google Account                          │
│                                          │
│  This will allow TripVault to:          │
│                                          │
│  ✓ See your email address               │
│  ✓ See your personal info               │
│  ✓ Store data in its own folder         │
│    in your Google Drive                  │
│                                          │
│  ❌ NOT:                                 │
│     View/edit your existing Drive files │
│     Delete your personal files           │
│     Share your files with others         │
│                                          │
│  [Cancel]              [Allow]           │
└─────────────────────────────────────────┘
```

---

### 🔑 Token Management

#### Token Storage (Database)

```sql
-- User Credentials Table (Encrypted)
CREATE TABLE user_credentials (
    user_id UUID PRIMARY KEY
        REFERENCES users(id) ON DELETE CASCADE,

    -- AES-256 encrypted tokens
    encrypted_access_token TEXT NOT NULL,
    encrypted_refresh_token TEXT NOT NULL,

    -- Token metadata
    token_expires_at TIMESTAMP NOT NULL,
    scope TEXT NOT NULL,

    -- Audit fields
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Example encrypted token (what gets stored)
encrypted_access_token:
"gAAAAABh1Qi5_7K9ZX8vP3mYN4xR2jL5..."
(Original: "ya29.a0AfH6SMBx...")
```

#### Encryption Implementation

```python
from cryptography.fernet import Fernet
import os

class TokenEncryption:
    """
    Handles encryption/decryption of OAuth tokens
    Uses Fernet (symmetric encryption with AES-256)
    """

    def __init__(self):
        # Load encryption key from environment variable
        # Key should be generated once: Fernet.generate_key()
        # Store in environment, NEVER in code!
        key = os.getenv('TOKEN_ENCRYPTION_KEY').encode()
        self.cipher = Fernet(key)

    def encrypt(self, plaintext: str) -> str:
        """Encrypt OAuth token before storing"""
        encrypted = self.cipher.encrypt(plaintext.encode())
        return encrypted.decode()

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt OAuth token when needed"""
        decrypted = self.cipher.decrypt(ciphertext.encode())
        return decrypted.decode()

# Usage Example
encryptor = TokenEncryption()

# Storing token
access_token = "ya29.a0AfH6SMBx..."
encrypted = encryptor.encrypt(access_token)
# Store encrypted version in database

# Retrieving token
encrypted_from_db = "gAAAAABh1Qi5_7K9..."
access_token = encryptor.decrypt(encrypted_from_db)
# Use access_token to call Google Drive API
```

---

### 🎫 Session Management (JWT)

#### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_abc123", // Subject (user ID)
    "email": "user@example.com",
    "name": "John Doe",
    "iat": 1706000000, // Issued at (timestamp)
    "exp": 1706604800, // Expires (7 days later)
    "type": "session"
  },
  "signature": "SflKxwRJ..."
}
```

#### JWT Generation

```python
import jwt
from datetime import datetime, timedelta

def generate_session_token(user_id: str, email: str, name: str) -> str:
    """
    Generate JWT session token for authenticated user
    Token valid for 7 days
    """

    payload = {
        "sub": user_id,
        "email": email,
        "name": name,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=7),
        "type": "session"
    }

    # Sign with secret key (from environment)
    token = jwt.encode(
        payload,
        os.getenv('JWT_SECRET_KEY'),
        algorithm="HS256"
    )

    return token

# Example output:
# "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyX2FiYzEyMyIsImVtYWlsIjoidXNlckBleGFtcGxlLmNvbSIsIm5hbWUiOiJKb2huIERvZSIsImlhdCI6MTcwNjAwMDAwMCwiZXhwIjoxNzA2NjA0ODAwLCJ0eXBlIjoic2Vzc2lvbiJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
```

#### JWT Validation

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    """
    Validate JWT token and return current user
    Used as dependency in protected endpoints
    """

    try:
        # Decode and validate token
        payload = jwt.decode(
            token.credentials,
            os.getenv('JWT_SECRET_KEY'),
            algorithms=["HS256"]
        )

        user_id = payload.get("sub")

        # Verify user exists in database
        user = await db.fetch_one("""
            SELECT id, email, name
            FROM users
            WHERE id = $1
        """, user_id)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired. Please log in again."
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token. Please log in again."
        )

# Usage in endpoint
@app.get("/trips")
async def get_trips(current_user = Depends(get_current_user)):
    # current_user is automatically validated
    trips = await fetch_user_trips(current_user['id'])
    return trips
```

---

## 6.2 Data Protection

### 🔐 Data in Transit (HTTPS/TLS)

#### TLS Configuration

```nginx
# Nginx Configuration for TripVault API

server {
    listen 443 ssl http2;
    server_name api.tripvault.com;

    # SSL Certificate (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/tripvault.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tripvault.com/privkey.pem;

    # TLS Version (Only modern protocols)
    ssl_protocols TLSv1.2 TLSv1.3;

    # Cipher Suites (Strong encryption only)
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;

    # HSTS (Force HTTPS for 1 year)
    add_header Strict-Transport-Security
        "max-age=31536000; includeSubDomains" always;

    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Proxy to FastAPI backend
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name api.tripvault.com;
    return 301 https://$server_name$request_uri;
}
```

---

### 🗄️ Data at Rest (Database Encryption)

#### PostgreSQL Encryption

```yaml
# AWS RDS PostgreSQL Configuration

Encryption:
  Storage Encryption: Enabled (AES-256)
  Encryption Key: AWS KMS (Customer Managed Key)

Connection:
  SSL Mode: require
  SSL Certificate: AWS RDS CA Certificate

Backups:
  Automated Backups: Enabled
  Backup Encryption: Enabled (same key as storage)
  Retention: 30 days

Snapshots:
  Manual Snapshots: Encrypted by default
  Cross-Region Replication: Encrypted in transit
```

---

### 🔒 Sensitive Data Handling

#### What We Store vs What We Don't

```
┌─────────────────────────────────────────────────────────────┐
│                  DATA INVENTORY                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ STORED (Necessary for Service)                         │
│  ────────────────────────────────────────────────────────  │
│  • User email (from OAuth)                                  │
│  • User name (from Google profile)                          │
│  • OAuth tokens (ENCRYPTED with AES-256)                    │
│  • File metadata (names, sizes, hashes)                     │
│  • Storage allocations & usage                              │
│  • Trip names, dates, descriptions                          │
│                                                             │
│  ❌ NOT STORED (Privacy by Design)                         │
│  ────────────────────────────────────────────────────────  │
│  • Passwords (we don't have any!)                           │
│  • File contents (stored in user Drives)                    │
│  • Browsing history                                         │
│  • Location data                                            │
│  • Payment information (no payments in MVP)                 │
│  • User's other Drive files                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 📝 Logging Policy (Security Best Practices)

#### What Gets Logged

```python
# Good Logging Example (SAFE)
{
    "timestamp": "2026-01-23T10:30:00Z",
    "level": "INFO",
    "endpoint": "POST /trips/abc123/files/upload",
    "user_id": "user_xyz",              # OK - internal ID
    "file_size": 5242880,                # OK - metadata
    "duration_ms": 2340,
    "status": 200,
    "ip_address": "192.168.1.1"         # OK - for security
}

# Bad Logging Example (UNSAFE) ❌
{
    "timestamp": "2026-01-23T10:30:00Z",
    "level": "ERROR",
    "message": "Upload failed",
    "access_token": "ya29.a0AfH6...",  # ❌ NEVER LOG TOKENS!
    "file_content": "base64...",        # ❌ NEVER LOG FILE DATA!
    "email": "user@example.com",        # ❌ Unnecessary PII
    "error_details": {
        "oauth_token": "..."             # ❌ NEVER!
```
