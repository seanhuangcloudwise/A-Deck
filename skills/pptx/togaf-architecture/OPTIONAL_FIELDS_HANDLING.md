# Optional Fields Handling in Renders

## Overview

This document describes how optional fields are safely handled across all TOGAF loaders to ensure renders gracefully skip missing or empty values.

## Problem

Previously, many render functions would blindly render optional fields even when they were:
- Missing from user config (using defaults)
- Explicitly set to empty strings (`""`)
- Empty lists or dicts

This resulted in unnecessary elements in slides and diminished visual clarity.

## Solution: `should_render()` Helper

A centralized `should_render()` function in `common.py` now handles validation:

```python
def should_render(value):
    """Check if a field value should be rendered.
    
    Returns False if value is None, empty string, or empty list/dict.
    This allows loaders to conditionally skip rendering optional elements.
    """
    if value is None:
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    if isinstance(value, (list, dict)) and len(value) == 0:
        return False
    return True
```

## Usage Patterns

### Pattern 1: Conditional Textbox Rendering

**Before:**
```python
delta = c.get("delta", d["delta"])
textbox(slide, mx, y0 + th // 2 - int(Inches(0.0)), aw, int(Inches(0.22)),
        short(delta, 12), size="caption", color=C["gray"], align=PP_ALIGN.CENTER)
```

**After:**
```python
delta = c.get("delta", d["delta"])
if should_render(delta):
    textbox(slide, mx, y0 + th // 2 - int(Inches(0.0)), aw, int(Inches(0.22)),
            short(delta, 12), size="caption", color=C["gray"], align=PP_ALIGN.CENTER)
```

### Pattern 2: Shape + Text Rendering

**Before:**
```python
if system:
    pill = _bp_round_rect(slide, x + int(Inches(0.12)), y + int(Inches(0.34)),
                          w - int(Inches(0.24)), int(Inches(0.14)),
                          system_fill, line=system_fill)
    add_text(pill, short(system, 18), size=7, color=_rgb(system_text))
```

**After:**
```python
if should_render(system):
    pill = _bp_round_rect(slide, x + int(Inches(0.12)), y + int(Inches(0.34)),
                          w - int(Inches(0.24)), int(Inches(0.14)),
                          system_fill, line=system_fill)
    add_text(pill, short(system, 18), size=7, color=_rgb(system_text))
```

## Updated Functions

The following render functions now use `should_render()`:

1. **`_footer()`** - Validates `note` field
2. **`render_two_column()`** - Validates `delta` field
3. **`render_journey_stages()`** - Validates `pain` field in phases
4. **`_bp_step()`** - Validates `system` and `duration` fields
5. **`render_kpi_cascade()`** - Validates `owner` field

## Config Examples

### Example 1: Omitting Optional Fields

```yaml
ba_07_as_is_to_be:
  title: "Digital Transformation"
  content:
    left_title: "As-Is"
    left_items: ["Manual processes", "Siloed systems"]
    right_title: "To-Be"
    right_items: ["Automated workflows", "Unified platform"]
    # delta omitted - will not be rendered
```

### Example 2: Explicitly Empty Fields

```yaml
ba_08_scenario_journey:
  title: "Customer Journey"
  content:
    phases:
      - title: "Awareness"
        touchpoints: ["Ad Campaign"]
        emotion: "+"
        pain: ""  # Empty string - will not be rendered
      - title: "Decision"
        touchpoints: ["Proposal"]
        emotion: "+"
        pain: "Long approval process"  # Will be rendered
```

### Example 3: Business Process without Annotations

```yaml
ba_03_process_flow:
  title: "Approval Workflow"
  content:
    nodes:
      - id: "n1"
        type: "step"
        name: "Submit Request"
        system: ""      # Will not render system pill
        duration: ""    # Will not render duration badge
      - id: "n2"
        type: "step"
        name: "Review"
        system: "Jira"  # Will render system pill
        duration: "<=2h"  # Will render duration badge
```

## Benefits

- **Cleaner Configs**: Users can omit optional fields entirely
- **Cleaner Slides**: Empty fields don't clutter the visual output
- **Consistency**: All renders follow the same validation pattern
- **Flexibility**: Each render independently decides which fields are optional

## Best Practices

1. **Use `should_render()` for all optional elements**:
   - Field labels that might be empty
   - Annotation boxes or pills
   - Secondary content like notes, system names, durations

2. **Document optional fields in loader defaults**:
   ```python
   _BA07_COMPARE = {
       "left_title":  "As-Is",
       "right_title": "To-Be",
       "left_items":  [...],
       "right_items": [...],
       "delta":       "Δ Transform",  # Optional - can be omitted or set to ""
   }
   ```

3. **Preserve required fields validation**:
   - Don't use `should_render()` for fields that MUST be present
   - E.g., `title`, `left_title`, `right_title` should always render

4. **Test with edge cases**:
   - Omitted field + default value
   - Explicitly empty string (`""`)
   - Whitespace-only string (`"   "`)
   - Empty lists/dicts for structural fields

## Testing Checklist

- [ ] Default values still render when user doesn't specify
- [ ] Empty strings (`""`) do NOT render
- [ ] Whitespace-only strings do NOT render
- [ ] Missing fields using defaults still render
- [ ] Related elements (pills, boxes) don't appear when content is empty
- [ ] Slide layout doesn't break when optional fields are omitted
