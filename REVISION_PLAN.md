# A-Grade Revision Plan: VC Hype Simulation

**Planning Committee Report**
**Date**: November 2025
**Goal**: Transform from D-grade (unpublishable) to A-grade (top journal submission)

---

## EXECUTIVE SUMMARY

This document outlines a **12-week action plan** to transform the VC Hype Simulation from a circular toy model into an empirically grounded, publishable research paper.

**Target Venue**: *Management Science* or *Journal of Financial Economics*
**Required Effort**: ~400 hours
**Key Deliverable**: Empirically calibrated model with out-of-sample validation

---

## PHASE 1: DATA ACQUISITION (Weeks 1-3)

### 1.1 Regional Capital Data (Critical)

**Task**: Replace estimates with exact figures

| Data Source | Access Method | Priority | Owner |
|-------------|---------------|----------|-------|
| PitchBook API | Academic subscription ($2-5K) | P0 | Data Lead |
| NVCA Yearbook | Free download | P0 | Data Lead |
| Carta Partnership | Academic partnership request | P1 | PI |
| Crunchbase Pro | Academic license | P1 | Data Lead |

**Deliverable**: `data/regions_empirical.yml` with exact capital shares, confidence intervals

### 1.2 VC Decision Data (Critical)

**Task**: Obtain real VC scoring/decision data

**Options**:
1. **Partner with VC firm** (anonymized deal flow data)
   - Reach out to: First Round, USV, Foundry Group (known for academic collaboration)
   - Offer: Co-authorship, anonymization, pre-publication review

2. **Survey approach** (like Gompers et al. 2016)
   - Survey 100+ VCs on decision weights
   - IRB approval required (~4 weeks)

3. **Revealed preference** (from public data)
   - Analyze Crunchbase funding patterns
   - Infer weights from company characteristics → funding outcomes

**Deliverable**: Empirically estimated `w_region` vectors with standard errors

### 1.3 Outcome Data (Critical)

**Task**: Obtain startup exit/failure rates

| Outcome | Data Source | Variables |
|---------|-------------|-----------|
| IPO | SEC EDGAR, Crunchbase | Date, valuation, return |
| Acquisition | Crunchbase, PitchBook | Price, acquirer, time-to-exit |
| Failure | CB Insights, Crunchbase | Date, last funding, burn rate |

**Deliverable**: `data/outcomes.csv` with 10,000+ companies, 2010-2024

### 1.4 Hype/Sentiment Data (Important)

**Task**: Construct empirical Hype(t) measure

**Methods**:
1. **Text-based**: Scrape TechCrunch/The Information, apply FinBERT sentiment
2. **Market-based**: VIX, IPO volume, SPAC activity, median VC valuation
3. **Survey-based**: VC confidence surveys (if available)

**Deliverable**: Monthly Hype index 2010-2024, validated against Baker-Wurgler

---

## PHASE 2: EMPIRICAL CALIBRATION (Weeks 4-6)

### 2.1 Estimate Feature Weights

**Method**: Regression of funding outcomes on founder characteristics

```python
# Pseudo-code for weight estimation
funded ~ revenue + growth + charisma_proxy + vision_proxy + domain + region
```

**Proxies**:
- `charisma_proxy`: Founder Twitter followers, media mentions, speaking appearances
- `vision_proxy`: Mission statement analysis, pitch deck language (if available)

**Deliverable**: Table of estimated weights by region with confidence intervals

### 2.2 Estimate Hype Sensitivity (β)

**Method**: Interaction model

```python
funded ~ features + Hype(t) + features × Hype(t) + region + region × Hype(t)
```

The coefficient on `region × Hype(t)` estimates β_region

**Deliverable**: Empirical β estimates showing Bay Area > LA > NYC > Boston (or not!)

### 2.3 Calibrate Markov Chain

**Method**: Maximum likelihood estimation from Hype(t) series

```python
# Estimate transition probabilities from observed state sequences
P(state_t+1 | state_t) = count(transitions) / count(state_t)
```

**Deliverable**: Empirically estimated transition matrix with confidence intervals

### 2.4 Moment Matching

**Task**: Ensure simulated distributions match real data

| Moment | Real Data | Simulated | Tolerance |
|--------|-----------|-----------|-----------|
| Mean funding by region | From PitchBook | From simulation | ±10% |
| Funding Gini by domain | From Crunchbase | From simulation | ±15% |
| Stage distribution | From NVCA | From simulation | ±5% |

**Deliverable**: Calibration table showing model matches data on 10+ moments

---

## PHASE 3: VALIDATION (Weeks 7-9)

### 3.1 In-Sample Fit

**Task**: How well does calibrated model explain observed patterns?

- R² for funding prediction
- AUC for funded/not-funded classification
- Regional allocation accuracy

### 3.2 Out-of-Sample Prediction

**Task**: Train on 2010-2020, predict 2021-2024

**Tests**:
1. Does model predict 2021 hype boom funding patterns?
2. Does model predict 2022-2023 correction?
3. Regional predictions hold out-of-sample?

**Deliverable**: Out-of-sample R², prediction intervals

### 3.3 Placebo Tests

**Task**: Model should NOT predict irrelevant outcomes

- Does model predict founder height? (No)
- Does model predict company name length? (No)
- Does model predict outcomes in non-VC sectors? (No)

### 3.4 Historical Validation

**Task**: Would model have flagged Theranos/WeWork/Quibi?

Use `data/cases.csv` to backtest:
- What scores did these companies receive?
- Did they score high on hype factors, low on fundamentals?
- Would a β-adjusted investor have avoided them?

**Deliverable**: Table showing model correctly identifies 80%+ of high-profile failures

---

## PHASE 4: ROBUSTNESS (Weeks 10-11)

### 4.1 Parameter Perturbation

**Task**: Results robust to ±30% weight changes

### 4.2 Alternative Specifications

**Task**: Test different functional forms

- Nonlinear scoring (neural network)
- Multiplicative instead of additive
- Different noise distributions

### 4.3 Additional Regions

**Task**: Add Seattle, Austin, Denver, Miami

Verify β ranking holds and model generalizes

### 4.4 Time Periods

**Task**: Test on different eras

- Dot-com era (1998-2001)
- Post-GFC (2009-2012)
- ZIRP era (2020-2021)
- Rate hike era (2022-2024)

---

## PHASE 5: WRITING & SUBMISSION (Week 12)

### 5.1 Revised Paper Structure

1. **Introduction**: Motivation (unchanged but sharpened)
2. **Data**: NEW section describing empirical sources
3. **Model**: Theory and mechanism (revised with empirical grounding)
4. **Calibration**: How parameters were estimated
5. **Results**: Empirical findings (not assumptions!)
6. **Validation**: Out-of-sample, placebo, historical
7. **Discussion**: Implications, limitations
8. **Conclusion**

### 5.2 New Figures

1. **Figure 1**: Empirical Hype(t) series 2010-2024
2. **Figure 2**: Estimated feature weights by region (with CI)
3. **Figure 3**: Model fit vs. actual funding patterns
4. **Figure 4**: Out-of-sample predictions
5. **Figure 5**: Historical case validation (Theranos, etc.)

### 5.3 Contribution Statement

**New claims (defensible)**:
- "We estimate that Bay Area VCs weight narrative factors 1.8× higher than NYC (p<0.01)"
- "Hype sensitivity varies 3× across regions, with Boston most conservative"
- "Model correctly identifies 85% of high-profile failures in holdout sample"

---

## RESOURCE REQUIREMENTS

### Budget

| Item | Cost | Priority |
|------|------|----------|
| PitchBook Academic Access | $3,000 | P0 |
| Crunchbase Pro | $500 | P1 |
| AWS/GCP compute | $200 | P2 |
| RA time (200 hrs @ $25/hr) | $5,000 | P0 |
| **Total** | **$8,700** | |

### Personnel

| Role | Hours | Skills |
|------|-------|--------|
| PI | 80 | Oversight, writing, VC outreach |
| Data RA | 200 | Python, SQL, web scraping |
| Econometrics RA | 100 | Stata/R, causal inference |
| NLP RA | 50 | FinBERT, text analysis |

### Timeline

| Week | Phase | Deliverable |
|------|-------|-------------|
| 1-3 | Data Acquisition | Raw datasets collected |
| 4-6 | Calibration | Parameters estimated |
| 7-9 | Validation | Out-of-sample results |
| 10-11 | Robustness | Sensitivity tables |
| 12 | Writing | Submission draft |

---

## SUCCESS CRITERIA

### Minimum Viable Paper (B-grade)

- [ ] At least ONE parameter empirically estimated
- [ ] Out-of-sample validation on 1+ test
- [ ] Clear distinction between calibrated vs. stylized parameters
- [ ] Honest limitations section

### Strong Paper (A-grade)

- [ ] ALL parameters empirically estimated with CI
- [ ] Multiple out-of-sample validations
- [ ] Historical validation on known cases
- [ ] Comparison to baseline models
- [ ] Policy implications quantified

### Top Journal (A+ grade)

- [ ] Novel identification strategy
- [ ] Causal interpretation (IV, RDD, or diff-in-diff)
- [ ] Real outcome data (exits, returns)
- [ ] VC firm partnership for inside data

---

## IMMEDIATE NEXT STEPS

### This Week

1. **Email NVCA** for 2024 Yearbook data clarifications
2. **Apply for PitchBook** academic access
3. **Draft VC partnership letter** to First Round/USV
4. **Set up web scraper** for TechCrunch sentiment data
5. **IRB application** for potential VC survey

### This Month

1. **Hire data RA** (post on EconJobMarket, RA-ship boards)
2. **Complete data acquisition** for Phase 1
3. **Begin calibration** with available data
4. **Present at lab meeting** for feedback

---

## RISK MITIGATION

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| PitchBook denies access | Medium | High | Use Crunchbase + NVCA aggregates |
| No VC willing to partner | High | Medium | Use survey approach instead |
| Calibration shows model wrong | Medium | High | Revise model, report negative result |
| Hype measure not predictive | Low | High | Use multiple proxies, ensemble |

---

## CONCLUSION

This project has **excellent infrastructure** (code, documentation, reproducibility) but **no scientific content** (circular reasoning, no validation).

The 12-week plan transforms it by:
1. Replacing assumptions with estimates
2. Adding validation tests
3. Making falsifiable predictions

**Expected outcome**: Submission-ready paper for *Management Science* or *Journal of Financial Economics*

---

## APPENDIX: Key Contacts

### Academic Data

- **NVCA**: research@nvca.org
- **PitchBook Academic**: academic@pitchbook.com
- **Carta Research**: research@carta.com

### Potential VC Partners

- **First Round Capital**: Known for research collaboration
- **Union Square Ventures**: Public about decision processes
- **Foundry Group**: Brad Feld is academic-friendly

### Academic Collaborators

- **Michael Ewens** (Caltech) - VC empirics expert
- **Josh Lerner** (HBS) - VC research dean
- **Steve Kaplan** (Chicago Booth) - PE/VC expert

---

**Planning Committee Signature**:
*Research Strategy Team*
*November 2025*
