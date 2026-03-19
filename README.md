# Civic Communication Authenticity Infrastructure (CCAI)

CCAI is an explainable AI system designed to help citizens verify the authenticity of institutional communications and discover legitimate government schemes they may be eligible for.

The platform analyzes messages such as SMS, emails, links, or forwarded content and evaluates structural authenticity signals including institutional domains, semantic similarity to known communications, and fraud indicators. Instead of censoring information, CCAI provides transparent authenticity scores and explanations that help users assess credibility.

---

## Problem

In many regions, citizens learn about government programs through forwarded messages on messaging platforms. These messages often:

* contain misleading or outdated information
* impersonate official institutions
* promote fraudulent schemes
* fail to clearly explain eligibility

As a result:

* citizens miss legitimate public benefits
* misinformation spreads quickly
* trust in institutional communication weakens

CCAI addresses these challenges by helping users verify communications and discover legitimate public programs.

---

## Key Features

### Authenticity Verification

Users can submit digital communications such as SMS messages, emails, or links. The system analyzes authenticity signals and returns an explainable authenticity score.

Signals analyzed include:

* verified institutional domains
* semantic similarity to known communications
* fraud indicators
* suspicious language patterns

---

### Government Scheme Discovery

The platform helps users identify government schemes they may be eligible for based on:

* income range
* occupation
* location
* demographic category

Users receive relevant programs with links to official government sources.

---

### Real-Time Analysis

All verification and discovery processes operate in real time, allowing users to quickly evaluate information they encounter online.

---

### Multilingual Translation

The platform supports translation into multiple languages, enabling citizens to access verified information in their preferred language.

---

### Privacy-Preserving Design

User inputs are processed anonymously.

The system:

* does not store personal attributes
* does not log eligibility signals
* processes requests only in memory

---

## System Architecture

CCAI uses a serverless architecture designed for scalability and reliability:

User
↓
Next.js Frontend
↓
API Gateway
↓
AWS Lambda (Flask Backend)
↓
AWS Services

* DynamoDB (registry and analysis results)
* S3 (datasets and configuration)
* Bedrock (semantic similarity embeddings)
* Comprehend (PII detection)
* Translate (multilingual support)
* SQS (appeal workflow)

---

## Core Components

* **Authenticity Engine** — evaluates communications and produces explainable scores
* **Registry Explorer** — enables browsing of verified sources and public programs
* **Scheme Eligibility Engine** — matches user signals with scheme criteria
* **Translation Engine** — provides multilingual explanations

---

## Example Workflow

1. A user receives a forwarded message about a government scheme
2. The user submits the message to CCAI
3. The system evaluates authenticity signals
4. An explainable authenticity score is returned
5. Relevant government schemes are suggested
6. The user accesses official sources directly

---

## Technology Stack

**Frontend**

* Next.js
* React
* TypeScript

**Backend**

* Python
* Flask

**Cloud Infrastructure**

* AWS Lambda
* API Gateway
* DynamoDB
* S3
* SQS

**AI Services**

* Amazon Bedrock
* Amazon Comprehend
* Amazon Translate

**Infrastructure as Code**

* Terraform

---

## Demo

The demo demonstrates:

* communication authenticity verification
* government scheme discovery
* multilingual translation
* registry exploration

---

## Repository Structure

frontend/
backend/
terraform/
scripts/
datasets/

---

## Running the Project

Install dependencies:

```
pip install -r backend/requirements.txt
npm install
```

Run backend:

```
python backend/run.py
```

Run frontend:

```
npm run dev
```

---

## Deployment

Infrastructure is deployed using Terraform:

```
terraform init
terraform plan
terraform apply
```

---

## Dataset

This project uses a structured dataset of government schemes derived from publicly available official sources such as:

- https://scholarships.gov.in  
- https://www.india.gov.in  
- https://pmkisan.gov.in  

The dataset is stored in:

datasets/sample_schemes.json

It is used for eligibility matching and scheme discovery.

Note: The dataset is a structured sample derived from publicly available government sources for demonstration purposes. The system is designed to scale with larger official datasets.

---

## Project Vision

CCAI aims to become a public civic infrastructure for trustworthy digital communication.

By helping citizens verify institutional messages and discover legitimate public programs, the platform strengthens:

* information integrity
* civic participation
* transparency in public communication

---

## Contributing

Contributions are welcome from developers, civic technologists, researchers, and community organizations interested in strengthening democratic information ecosystems.

---

## License

Open source license information will be provided as the project evolves.
