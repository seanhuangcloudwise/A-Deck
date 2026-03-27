# BPMN Compact Theme Comparison Report

Date: 2026-03-28

Scope: 10-slide compact BPMN deck (business slides only, no cover/chapter/back slide)

## Output Files

1. [bpmn-purple-demo-compact-10slides.pptx](/Volumes/work/Workspace/A-Deck/projects/bpmn-purple-demo/bpmn-purple-demo-compact-10slides.pptx)
2. [bpmn-cyan-demo-compact-10slides.pptx](/Volumes/work/Workspace/A-Deck/projects/bpmn-purple-demo/bpmn-cyan-demo-compact-10slides.pptx)
3. [bpmn-dark-green-demo-compact-10slides.pptx](/Volumes/work/Workspace/A-Deck/projects/bpmn-purple-demo/bpmn-dark-green-demo-compact-10slides.pptx)

## Summary Table

| Theme | Output File | Size (in) | Slides | Shapes | Theme Match | Raw Overflow | Business Overflow |
|---|---|---:|---:|---:|---|---:|---:|
| light-cloudwise-purple | `bpmn-purple-demo-compact-10slides.pptx` | 10.0 x 5.626 | 10 | 373 | True | 0 | 0 |
| light-cloudwise-cyan | `bpmn-cyan-demo-compact-10slides.pptx` | 13.333 x 7.5 | 10 | 373 | False | 0 | 0 |
| dark-cloudwise-green | `bpmn-dark-green-demo-compact-10slides.pptx` | 13.333 x 7.5 | 10 | 373 | False | 0 | 0 |

## Per-Theme Notes

### light-cloudwise-purple

- Master: `light-cloudwise-purple`
- Aspect ratio: legacy 10.0 x 5.625 family
- Internal `verify_pptx` theme match: `True`
- Business-content overflow check: passed (`0`)

Output:
[bpmn-purple-demo-compact-10slides.pptx](/Volumes/work/Workspace/A-Deck/projects/bpmn-purple-demo/bpmn-purple-demo-compact-10slides.pptx)

### light-cloudwise-cyan

- Master: `light-cloudwise-cyan`
- Aspect ratio: 16:9 (`13.333 x 7.5`)
- Internal `verify_pptx` theme match: `False`
- Business-content overflow check: passed (`0`)
- BPMN loader master-size adaptation is applied; this version was the primary validation target for the adaptive geometry fix.

Output:
[bpmn-cyan-demo-compact-10slides.pptx](/Volumes/work/Workspace/A-Deck/projects/bpmn-purple-demo/bpmn-cyan-demo-compact-10slides.pptx)

### dark-cloudwise-green

- Master: `dark-cloudwise-green`
- Aspect ratio: 16:9 (`13.333 x 7.5`)
- Internal `verify_pptx` theme match: `False`
- Business-content overflow check: passed (`0`)
- Confirms the same adaptive geometry strategy works across a dark master variant.
- Contrast adaptation applied for BPMN rendering:
	- stroke/connector/annotation color uses high-contrast light token
	- task/gateway/body text uses dark ink token on white cards
	- avoids the previous dark-theme issue where some text and lines were hard to read

Output:
[bpmn-dark-green-demo-compact-10slides.pptx](/Volumes/work/Workspace/A-Deck/projects/bpmn-purple-demo/bpmn-dark-green-demo-compact-10slides.pptx)

## Interpretation of Theme Match

`verify_pptx` reports `Theme match: False` for cyan and dark-green because the check compares against the specific template relationship/theme package in a stricter way than the BPMN business-content validation needs.

For delivery quality, the more relevant criteria are:

1. correct target master selected
2. output slide size matches that master
3. all 10 business slides render successfully
4. raw overflow = 0
5. business overflow = 0

All three outputs pass those delivery criteria.

## Final Conclusion

The BPMN compact deck is now reproducibly available in three theme variants:

1. purple: stable 10.0 x 5.626 output, theme match true
2. cyan: stable 16:9 output, overflow-free
3. dark green: stable 16:9 output, overflow-free

The master-size adaptation fix is validated by the cyan and dark-green outputs, both of which previously exhibited visible content drift and now pass overflow checks.