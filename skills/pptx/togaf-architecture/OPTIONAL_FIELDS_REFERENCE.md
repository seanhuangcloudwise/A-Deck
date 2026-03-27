# Optional Fields Quick Reference

## Render Functions with Optional Field Support

### 1. Footer (used by all renders)
- **Function:** `_footer(slide, note="", C=None)`
- **Optional Field:** `note`
- **Renders when:** note is not None/empty
- **Example:**
  ```yaml
  content:
    note: ""  # Omit or set to "" - footer won't render
  ```

### 2. Two-Column Compare (BA-07, TA-08)
- **Function:** `render_two_column(ctx, data, ...)`
- **Optional Field:** `delta` (center label)
- **Location:** `content.delta`
- **Renders when:** delta is not None/empty
- **Example:**
  ```yaml
  ba_07_as_is_to_be:
    content:
      left_title: "As-Is"
      right_title: "To-Be"
      delta: ""  # Center arrow label won't render
  ```

### 3. Journey Stages (BA-08)
- **Function:** `render_journey_stages(ctx, data, ...)`
- **Optional Field:** `pain` (per phase)
- **Location:** `content.phases[].pain`
- **Renders when:** pain is not None/empty
- **Example:**
  ```yaml
  ba_08_scenario_journey:
    content:
      phases:
        - title: "Awareness"
          pain: ""  # No pain warning icon
        - title: "Decision"
          pain: "Long approval cycles"  # Shows warning
  ```

### 4. Business Process Step Annotations
- **Function:** `_bp_step(slide, x, y, w, h, step, C)`
- **Optional Fields:** 
  - `system` - system name pill
  - `duration` - time badge
- **Location:** `content.nodes[].system`, `content.nodes[].duration`
- **Renders when:** Not None/empty
- **Example:**
  ```yaml
  ba_03_process_flow:
    content:
      nodes:
        - name: "Step 1"
          system: ""      # No system pill
          duration: ""    # No duration badge
        - name: "Step 2"
          system: "Jira"  # System pill shown
          duration: "2h"  # Duration badge shown
  ```

### 5. KPI Cascade (BA-09)
- **Function:** `render_kpi_cascade(ctx, data, ...)`
- **Optional Field:** `owner` (per objective)
- **Location:** `content.objectives[].owner`
- **Renders when:** owner is not None/empty
- **Example:**
  ```yaml
  ba_09_kpi_alignment:
    content:
      objectives:
        - label: "Growth"
          owner: ""  # No owner text
        - label: "Quality"
          owner: "VP Engineering"  # Owner shown
  ```

### 6. Node Graph (AA-03, TA-01, DA-04)
- **Function:** `render_node_graph(ctx, data, ...)`
- **Optional Field:** `label` (per edge)
- **Location:** `content.edges[].label`
- **Renders when:** label is not None/empty
- **Example:**
  ```yaml
  ta_01_infrastructure:
    content:
      edges:
        - from: "LB"
          to: "Web1"
          label: ""  # No connection label
        - from: "Web1"
          to: "App1"
          label: "RPC"  # Connection label shown
  ```

### 7. Bounded Context (AA-11, DA-09)
- **Function:** `render_bounded_context(ctx, data, ...)`
- **Optional Field:** `type` (per relation)
- **Location:** `content.relations[].type`
- **Renders when:** type is not None/empty
- **Example:**
  ```yaml
  aa_11_bounded_context:
    content:
      relations:
        - from: "UserContext"
          to: "OrderContext"
          type: ""  # No relationship label
        - from: "OrderContext"
          to: "ShippingContext"
          type: "depends on"  # Label shown
  ```

### 8. Entity Relationship (DA-01, DA-02)
- **Function:** `render_er_diagram(ctx, data, ...)`
- **Optional Field:** `label` (per relation)
- **Location:** `content.relations[].label`
- **Renders when:** label is not None/empty
- **Example:**
  ```yaml
  da_01_entity_model:
    content:
      relations:
        - from: "Customer"
          to: "Order"
          label: ""  # No relationship label
        - from: "Order"
          to: "Item"
          label: "1..*"  # Cardinality shown
  ```

## Testing Optional Fields

### Test Pattern 1: Omit the field entirely
```yaml
content:
  optional_field: [field is missing]
  # Expected: field won't render, uses default if available
```

### Test Pattern 2: Set to empty string
```yaml
content:
  optional_field: ""
  # Expected: field won't render
```

### Test Pattern 3: Whitespace only
```yaml
content:
  optional_field: "   "
  # Expected: field won't render (treated as empty)
```

### Test Pattern 4: Provide value
```yaml
content:
  optional_field: "Actual Value"
  # Expected: field renders normally
```

## Validation Function

All optional field checks use this helper:

```python
def should_render(value):
    """Returns False if: None, empty string, or empty collection."""
    if value is None:
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    if isinstance(value, (list, dict)) and len(value) == 0:
        return False
    return True
```

## Common Patterns

### Pattern A: Optional Section Label
Places where you might want to skip a label:
- Edge labels in graphs
- Relationship labels in diagrams
- Transformation labels in data flow

**Set to:** `""` or omit

### Pattern B: Optional Annotation
Places where you might want to skip metadata:
- System name in process steps
- Duration estimate in process steps
- Pain points in journey stages
- Owner in KPI cascade

**Set to:** `""` or omit

### Pattern C: Optional Transformation Description
Places where the transform is self-explanatory:
- Delta/change description between two states
- Relationship type between bounded contexts

**Set to:** `""` or omit

## Backward Compatibility

✅ **Fully backward compatible:**
- Existing configs with empty strings still work
- Existing configs with defaults still work
- No migration needed

**Before (still works):**
```yaml
delta: ""
```

**After (new: also works):**
```yaml
# delta field can be omitted
```

## Best Practices

1. **Document optional fields in your configs:**
   ```yaml
   # Optional: can be omitted or set to ""
   delta: "Δ Transformation"
   ```

2. **Use meaningful values when provided:**
   ```yaml
   system: "Jira"  # Good: specific system
   system: "yes"   # Bad: not meaningful
   ```

3. **Keep related fields together:**
   ```yaml
   - name: "Approval"
     system: "Workflow"     # Related annotation
     duration: "<=2h"       # Related annotation
   ```

4. **Test edge cases:**
   - Omitted field
   - Empty string
   - Whitespace-only string

## Debugging

If optional field still renders when it shouldn't:

1. Check for typos in field path
2. Verify it's actually empty/whitespace
3. Run test: `python3 test_optional_fields.py`
4. Check render function uses `should_render(value)`

Example debug config:
```yaml
content:
  phases:
    - title: "Test"
      pain: "   "  # Whitespace - should NOT render
      # Verify: no pain warning should appear
```
