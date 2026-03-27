"""
BPMN 2.0 Style Tokens — local to bpmn-architecture skill.

Defines semantic color tokens and sizing constants.
Colors are resolved at runtime from ctx.colors (master theme).
No hardcoded brand RGB except documented semantic reserved colors.
"""

from pptx.util import Inches, Pt


def _luminance(rgb):
    r, g, b = rgb
    return (r * 0.2126 + g * 0.7152 + b * 0.0722) / 255


# ---------------------------------------------------------------------------
# Semantic reserved colors (BPMN-specific, allowed to hardcode per spec)
# ---------------------------------------------------------------------------

SEMANTIC_COLORS = {
    "error": (217, 64, 64),        # #D94040 — Error events, error boundary
    "compensation": (230, 168, 23), # #E6A817 — Compensation events/handlers
    "cancel": (230, 138, 23),       # #E68A17 — Cancel events
    "timer": None,                  # Resolved from ctx.colors["secondary"] at runtime
    "message": None,                # Resolved from ctx.colors["secondary"] at runtime
    "escalation": (217, 140, 64),   # #D98C40 — Escalation events
    "signal": (100, 149, 237),      # #6495ED — Signal events
}


# ---------------------------------------------------------------------------
# Standard element sizing (10" x 5.63" slide, all in inches)
# ---------------------------------------------------------------------------

class Size:
    """Default element sizes in inches."""
    TASK_W = 1.3
    TASK_H = 0.55
    TASK_W_COMPACT = 1.0
    TASK_H_COMPACT = 0.45

    EVENT_DIAMETER = 0.24
    EVENT_DIAMETER_SMALL = 0.18

    GATEWAY_SIZE = 0.32
    GATEWAY_SIZE_SMALL = 0.25

    POOL_HEADER_W = 0.4     # for horizontal pool: left strip width
    LANE_HEADER_W = 0.8     # lane label strip width
    NESTED_LANE_HEADER_W = 0.6

    HEXAGON_W = 0.8
    HEXAGON_H = 0.5

    SUBPROCESS_CORNER_RADIUS = 4  # Pt
    TASK_CORNER_RADIUS = 4        # Pt

    # Message envelope icon
    ENVELOPE_W = 0.15
    ENVELOPE_H = 0.10

    # Spacing
    TASK_GAP_H = 0.35       # horizontal gap between tasks
    BRANCH_GAP_V = 0.55     # vertical gap between parallel branches
    POOL_GAP = 0.45          # gap between pools (for message flows)
    LANE_SEPARATOR = 0.75    # Pt line width


# ---------------------------------------------------------------------------
# Line widths
# ---------------------------------------------------------------------------

class LineWidth:
    SEQUENCE_FLOW = Pt(1)
    MESSAGE_FLOW = Pt(1.5)
    ASSOCIATION = Pt(1)
    CONVERSATION_LINK = Pt(1)
    START_EVENT = Pt(1.5)
    END_EVENT = Pt(3)
    INTERMEDIATE_EVENT_OUTER = Pt(1.5)
    INTERMEDIATE_EVENT_INNER = Pt(1)
    GATEWAY = Pt(1.25)
    TASK = Pt(1)
    SUBPROCESS = Pt(1.5)
    TRANSACTION_OUTER = Pt(2)
    TRANSACTION_INNER = Pt(1.5)
    CALL_ACTIVITY = Pt(2.5)
    POOL_BORDER = Pt(1)
    LANE_SEPARATOR_LINE = Pt(0.75)


# ---------------------------------------------------------------------------
# Font sizes
# ---------------------------------------------------------------------------

class FontSize:
    POOL_NAME = Pt(11)
    LANE_NAME = Pt(9)
    TASK_LABEL = Pt(8)
    TASK_LABEL_COMPACT = Pt(7)
    GATEWAY_CONDITION = Pt(7)
    EVENT_LABEL = Pt(7)
    MESSAGE_NAME = Pt(7)
    ANNOTATION = Pt(7)
    SUBTITLE = Pt(7)
    CHOREOGRAPHY_PARTICIPANT = Pt(7)
    CHOREOGRAPHY_INTERACTION = Pt(8)
    PATTERN_CARD_TITLE = Pt(9)
    AUTOMATION_PCT = Pt(10)


# ---------------------------------------------------------------------------
# Runtime color resolver
# ---------------------------------------------------------------------------

def resolve_colors(ctx_colors):
    """Merge theme colors with BPMN semantic reserved colors.

    Returns a dict usable by all loaders.
    ctx_colors comes from ctx.colors (theme-extracted from master template).

    This function guarantees every key that loaders/primitives reference will
    exist.  Neutral-gray fallbacks are used ONLY when the master theme does
    not supply the key — no brand colour is ever hardcoded here.
    """
    c = dict(ctx_colors)  # shallow copy

    # -- Structural keys (neutral fallbacks, never brand-specific) ----------
    c.setdefault("white", (255, 255, 255))
    c.setdefault("light", (230, 230, 230))
    c.setdefault("dark", (60, 60, 60))
    c.setdefault("text", c["dark"])
    c.setdefault("primary", (80, 80, 80))
    c.setdefault("secondary", (120, 120, 120))

    # Derive mode from extracted theme colors.
    # Dark mode: dark token is truly dark and text token is light.
    dark_mode = _luminance(c["dark"]) < 0.25 and _luminance(c["text"]) > 0.7

    if dark_mode:
        ink = c["dark"]
        stroke = c["text"]
        c["mode"] = "dark"
        c["ink"] = ink
        c["stroke"] = stroke
        # Keep card/body text dark so it stays readable on white task fills.
        c["text"] = ink
        # Repurpose `dark` as the global high-contrast stroke token because many
        # existing loaders/primitives reference it directly for borders/lines.
        c["dark"] = stroke
    else:
        c["mode"] = "light"
        c["ink"] = c["dark"]
        c["stroke"] = c["dark"]

    # -- BPMN semantic reserved colours (spec-mandated, ok to hardcode) -----
    c["error"] = SEMANTIC_COLORS["error"]
    c["compensation"] = SEMANTIC_COLORS["compensation"]
    c["cancel"] = SEMANTIC_COLORS["cancel"]
    c["escalation"] = SEMANTIC_COLORS["escalation"]
    c["signal"] = SEMANTIC_COLORS["signal"]

    # Timer / message derive from theme secondary (never a fixed brand hue)
    c.setdefault("timer", c["secondary"])
    c.setdefault("message", c["secondary"])
    return c
