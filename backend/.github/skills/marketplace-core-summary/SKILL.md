---
name: marketplace-core-summary
description: "Summarize the project core, objectives, and requirements for the B2B produtor-varejo marketplace. Use when you need a concise project overview, functional requirements (RF), non-functional requirements (RNF), and business rules (RN)."
argument-hint: "Provide source docs or point to a README/brief to summarize."
---

# Marketplace Core Summary

## Documentation Context (Reference)
Use this section as the primary source of truth when gathering context.

### Core Proposal
- Marketplace B2B connects pequeno produtor (fonte) to varejo (movimento) to reduce dependence on large suppliers and expand small producer visibility.
- Addresses lack of access to technology/information for small producers and their low visibility in retail supply chains.
- Reduces predatory intermediaries ("atravessador") and aims for fair pricing without incentivizing price wars.
- Aligns with ODS 9, especially Meta 9.3 (inclusive industrialization, access to markets and value chains).

### Objectives and Expected Outcomes
- Deliver an intelligent ecosystem for buying/selling between small producers and retailers.
- Provide intelligent supplier search and demand forecasting.
- Provide dynamic pricing based on regional/national market data.
- Monetization: fee based on weight/volume charged during transaction (platform revenue), while protecting producer margin.
- Expected results: higher producer visibility and revenue, diversified retail supply, fair and traceable supply chain.

### Core Flow
- Data input: producers register products, availability, and quantities; retailers register needs and wish lists with dates and location.
- Matchmaking: filters by product type and geolocation to connect demand to nearby/adequate supply.
- Business intelligence: demand forecasting from wish lists; dynamic pricing without predatory competition.

### Functional Requirements (RF)
- RF1: user registration and authentication for producer and retailer profiles.
- RF2: retailer wish list with items, future need dates, and geographic info.
- RF3: producer portfolio management for products, availability, and quantities.
- RF3 (pricing): dynamic pricing engine using web scraping of regional/national markets.
- RF4: demand forecasting module based on retailer wish lists.
- RF5: monetization fee calculation based on weight or volume during transaction.
- RF6: supplier search and filtering by product type and stock availability.
- RF7: payment processing (credit, debit, PIX, boleto).
- RF8: sales history tracking with statuses and key data.
- RF9: payment receipts for both parties.

### Non-Functional Requirements (RNF)
- RNF1: runs on mobile devices.
- RNF2: good response time over varied networks (2G, 3G, 4G).
- RNF3: scales with growth of producers and retailers without major performance loss.
- RNF4: simple, accessible UI for low-tech users.
- RNF5: fast query response for products and supplier searches at high volume.
- RNF6: detailed operational and transaction logs for audit and traceability.

### Business Rules (RN)
- RN1: fee per kilogram sold, based on price per kilo of item type, charged during the sale.
- RN2: recommend producers based on geolocation and supply that meets retailer needs.
- RN3: avoid predatory competition; do not rank solely by lowest price.
- RN4: prioritize geographically closer producers meeting minimum quantity, availability, and product type.
- RN5: retailer wish lists must include product, estimated quantity, and needed date.
- RN6: demand forecasts derived from retailer wish lists and their specified periods.

## What This Skill Does
Creates a concise, structured summary of the project core, objectives, and requirements for the B2B marketplace connecting pequeno produtor and varejo. It consolidates the problem statement, solution goals, functional requirements, non-functional requirements, and business rules in one place.

## When to Use
- You need a quick project overview for onboarding
- You need a clean, consistent requirements recap
- You are validating scope against RF/RNF/RN lists
- You are preparing briefs for design, dev, or review

## Inputs
- Project documentation, proposal, or README
- Any explicit RF/RNF/RN lists

## Procedure
1. Read the provided docs and identify the core problem, target users, and value proposition.
2. Extract objectives and expected outcomes.
3. List Functional Requirements (RF) as numbered items with short titles.
4. List Non-Functional Requirements (RNF) as numbered items with short titles.
5. List Business Rules (RN) as numbered items with short titles.
6. Capture key constraints, assumptions, and monetization model.
7. Produce the output using the format below.

## Output Format
- **Core**: 3-6 sentences describing the marketplace, actors, and social/economic goal.
- **Objectives**: 3-6 bullets.
- **Functional Requirements (RF)**: numbered list.
- **Non-Functional Requirements (RNF)**: numbered list.
- **Business Rules (RN)**: numbered list.
- **Notes/Constraints**: bullets for monetization, logistics scope, and data sources.

## Quality Checks
- All RF/RNF/RN are present and aligned with the source docs.
- The summary is concise, non-duplicated, and uses consistent wording.
- The monetization model and pricing logic are explicitly stated.
- Avoids encouraging predatory price competition.
