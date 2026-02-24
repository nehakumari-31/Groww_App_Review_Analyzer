# Groww App Review Analyzer - Architecture Document

This document outlines the four-phase architecture for the **Groww App Review Analyzer**, an automated system designed to ingest, analyze, and report on app store reviews with a premium Groww-inspired aesthetic.

---

## 🏗️ System Overview

The system uses **n8n** as the primary orchestration layer, **Groq** (LLM) for intelligent sentiment and theme analysis, and a standalone **Streamlit Dashboard** for visualization.

---

## 📅 Phase 1: Data Ingestion & Pre-processing
**Goal:** Establish a reliable pipeline to fetch and clean raw review data.

### Components:
*   **Source Scrapers:** Python scripts using `google-play-scraper` and `app-store-scraper`.
*   **PII Scrubber:** regex-based cleaning to remove:
    *   Full Names
    *   Phone Numbers
    *   Email Addresses
*   **Date Filter:** Limits ingestion to reviews from the **last 8–12 weeks (rating, title, text, date)**.
*   **Storage:** Raw and cleaned reviews stored in CSV/JSON format for downstream processing.

---

## 🧠 Phase 2: AI Engine (Groq & n8n)
**Goal:** Extract actionable insights using high-speed LLM inference.

### Components:
*   **LLM Provider:** [Groq](https://groq.com/) using `llama3-70b` or `mixtral-8x7b` for low-latency analysis.
*   **Thematic Classifier:** Categorizes reviews into exactly **5 themes** specifically for Groww (e.g., Onboarding, KYC, Payments, Statements, Withdrawals).g.onboarding, KYC, payments, statements, withdrawals)
*   **The "Groww Review Pulse":** A summarized insight block containing:
    *   **3 Key Themes** for the week.
    *   **3 Critical Quotes** (anonymized).
    *   **3 Actionable Ideas** for product improvement.

---

## 🎨 Phase 3: Premium Groww Dashboard
**Goal:** Visualize insights in a high-quality, responsive interface.

### Design Principles:
*   **Aesthetics:** Groww-inspired dark/light theme, glassmorphism, and vibrant accent colors.
*   **Framework:** Streamlit for rapid, interactive deployment.
*   **Key Features:**
    *   Pulse Header (Weekly overview).
    *   Interactive Theme Breakdown.
    *   "Voice of Customer" Quote Carousel.
    *   Action Item Checklist.

---

## 🤖 Phase 4: Automated Reporting & Orchestration
**Goal:** Automate the "last mile" of delivery.

### Workflow (n8n Master):
1.  **Trigger:** Weekly cron job or n8n webhook.
2.  **Analysis Trigger:** Calls Phase 2 script via n8n Node.
3.  **Communication Layer:**
    *   **Gmail Reporting:** Automated delivery of concise summaries (≤250 words) to stakeholders via Gmail SMTP.
4.  **Integration:** All scripts are hosted/triggered through n8n workflows for a "no-manual-effort" pipeline.

---

### 🛡️ Tech Stack
*   **Orchestration:** n8n
*   **LLM Inference:** Groq
*   **Frontend:** Streamlit / Vanilla CSS
*   **Language:** Python 3.x
*   **Libraries:** `pandas`, `groq`, `google-play-scraper`, `app-store-scraper`
