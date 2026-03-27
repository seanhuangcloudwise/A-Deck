# Example: Using Optional Fields in TOGAF Loader Configs

This document shows practical examples of how to use the optional fields feature in your TOGAF architecture PPT configurations.

## Example 1: Two-Column Comparison (BA-07)

### Scenario A: All fields provided
```yaml
ba_07_as_is_to_be:
  tag: "BA-07"
  title: "Digital Transformation Journey"
  content:
    left_title: "Current State (As-Is)"
    left_items:
      - "Manual approval processes"
      - "Siloed departmental systems"
      - "Email-based communication"
      - "Paper-based documentation"
      - "Reactive support model"
    right_title: "Target State (To-Be)"
    right_items:
      - "Automated workflows"
      - "Integrated business platform"
      - "Real-time collaboration tools"
      - "Digital-first operations"
      - "Proactive analytics & insights"
    delta: "Δ 18-month transformation"
    note: "Driven by strategic cloud-first initiative"
```

### Scenario B: Omit delta (simpler comparison)
```yaml
ba_07_as_is_to_be:
  tag: "BA-07"
  title: "Platform Comparison"
  content:
    left_title: "Legacy System"
    left_items: ["On-premise", "Limited scalability", "High maintenance cost"]
    right_title: "Cloud Platform"
    right_items: ["Fully managed", "Auto-scaling", "Lower TCO"]
    # delta omitted - arrow shows connection without label
```

### Scenario C: Empty delta explicitly (same as omitting)
```yaml
ba_07_as_is_to_be:
  tag: "BA-07"
  title: "State Comparison"
  content:
    left_title: "Before"
    left_items: ["..."]
    right_title: "After"
    right_items: ["..."]
    delta: ""  # This has same effect as omitting - no label rendered
```

## Example 2: Customer Journey (BA-08)

### Scenario A: Full journey with emotions and pain points
```yaml
ba_08_scenario_journey:
  tag: "BA-08"
  title: "Customer Experience Journey"
  content:
    phases:
      - title: "Awareness"
        touchpoints: ["Google Search", "Social Media", "Referral"]
        emotion: "+"
        pain: "Hard to find detailed product info"
      
      - title: "Consideration"
        touchpoints: ["Product Demo", "Comparison", "Case Study"]
        emotion: "~"
        pain: "Unclear pricing models"
      
      - title: "Decision"
        touchpoints: ["Sales Proposal", "Legal Review", "Negotiation"]
        emotion: "-"
        pain: "Long approval cycles"
      
      - title: "Onboarding"
        touchpoints: ["Training", "Configuration", "Data Migration"]
        emotion: "-"
        pain: "Complex system setup"
      
      - title: "Advocacy"
        touchpoints: ["Success Reviews", "Referrals", "Community"]
        emotion: "+"
        pain: ""  # No significant pain at this stage
    
    note: "Based on 2024 customer feedback survey (n=200)"
```

### Scenario B: Simplified journey (minimal pain points)
```yaml
ba_08_scenario_journey:
  tag: "BA-08"
  title: "Simplified Journey"
  content:
    phases:
      - title: "Awareness"
        touchpoints: ["Search", "Social"]
        emotion: "+"
        # pain omitted - no pain point shown
      
      - title: "Conversion"
        touchpoints: ["Demo"]
        emotion: "+"
        # pain omitted
      
      - title: "Loyalty"
        touchpoints: ["Support", "Community"]
        emotion: "+"
        # pain omitted
```

## Example 3: Business Process Flow (BA-03)

### Scenario A: Full process with annotations
```yaml
ba_03_process_flow:
  tag: "BA-03"
  title: "Requirements Management Process"
  content:
    nodes:
      - id: "start"
        type: "event"
        lane: "业务方"
        x_in: 0.02
        start: true
      
      - id: "n1"
        type: "step"
        lane: "业务方"
        col: 0
        name: "提交需求"
        system: "Portal"          # System annotation shown
        duration: "<=2h"          # Duration badge shown
        critical: false
      
      - id: "n2"
        type: "step"
        lane: "产品经理"
        col: 1
        name: "需求分级"
        system: "Jira"           # System annotation shown
        duration: "<=1h"         # Duration badge shown
        critical: false
```

### Scenario B: Simple process (no system/duration)
```yaml
ba_03_process_flow:
  tag: "BA-03"
  title: "Simple Approval"
  content:
    nodes:
      - id: "n1"
        type: "step"
        lane: "Sales"
        name: "Request"
        # system and duration omitted - cleaner visual

      - id: "n2"
        type: "step"
        lane: "Manager"
        name: "Approve"
        # system and duration omitted
```

## Example 4: KPI Cascade (BA-09)

### Scenario A: Full KPI with owners
```yaml
ba_09_kpi_alignment:
  tag: "BA-09"
  title: "OKR Framework Cascade"
  content:
    objectives:
      - label: "Customer Satisfaction"
        owner: "Chief Customer Officer"  # Owner shown
        kpis:
          - "NPS > 50"
          - "CSAT > 90%"
          - "FCR > 85%"
      
      - label: "Revenue Growth"
        owner: "VP Sales"               # Owner shown
        kpis:
          - "ARR +$5M"
          - "Net ARR Retention 110%"
```

### Scenario B: Simplified KPI (no owners)
```yaml
ba_09_kpi_alignment:
  tag: "BA-09"
  title: "Q4 Targets"
  content:
    objectives:
      - label: "Efficiency"
        # owner omitted - cleaner display
        kpis:
          - "Automation +30%"
          - "Cost -15%"
      
      - label: "Quality"
        # owner omitted
        kpis:
          - "Defect rate -50%"
          - "Release cycle -2 weeks"
```

## Example 5: Network/Graph with Labels (AA-03, TA-01)

### Scenario A: Full connectivity diagram with labels
```yaml
aa_03_integration:
  tag: "AA-03"
  title: "Application Integration Map"
  content:
    edges:
      - from: "CRM"
        to: "ERP"
        label: "REST API"      # Connection label shown
      
      - from: "ERP"
        to: "Data Warehouse"
        label: "Nightly Batch" # Connection label shown
```

### Scenario B: Simplified diagram (no labels)
```yaml
aa_03_integration:
  tag: "AA-03"
  title: "System Architecture"
  content:
    edges:
      - from: "Frontend"
        to: "Backend"
        # label omitted - just shows connection arrow
      
      - from: "Backend"
        to: "Database"
        # label omitted
```

## Benefits Summary

✅ **Less Configuration:** Omit fields that aren't needed
✅ **Cleaner Slides:** Don't render empty elements  
✅ **Better UX:** Visual design isn't cluttered with unused elements
✅ **Flexible:** Same loader works for simple and complex scenarios

## Migration Guide

If you have existing configs with empty string values:

```yaml
# OLD: Required empty strings
ba_07_as_is_to_be:
  content:
    delta: ""  # Had to provide this

# NEW: Can simply omit
ba_07_as_is_to_be:
  content:
    # delta field can be removed entirely
    # or left empty - both work the same
```

Both approaches work - no breaking changes!
