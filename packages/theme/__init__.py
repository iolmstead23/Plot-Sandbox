"""Visual theme constants shared by the ui/ and plot/ layers.

Edit values here to restyle the entire application — no other files need
to change. The BG colour is intentionally a single source of truth because
the Qt window background and the VisPy canvas background must match.
"""

# ── Surface colours ────────────────────────────────────────────────────────
BG     = "#1e1e2e"  # window / canvas background (Qt + VisPy must match)
TEXT   = "#cdd6f4"  # primary text
BORDER = "#45475a"  # divider lines

# ── Sidebar / button colours ───────────────────────────────────────────────
BUTTON_BG    = "#313244"  # button fill
BUTTON_HOVER = "#45475a"  # button hover

# ── Banner bar ─────────────────────────────────────────────────────────────
BANNER_FONT        = "Courier"
BANNER_FONT_SIZE   = 9
BANNER_HEIGHT      = 22        # px
BANNER_PADDING     = "2px 6px"

# ── Sidebar ────────────────────────────────────────────────────────────────
SIDEBAR_WIDTH = 160  # px
BUTTON_WIDTH  = 130  # px

# ── Scene edges ────────────────────────────────────────────────────────────
EDGE_COLOR = (0.7, 0.7, 0.7, 0.45)  # light on dark background, visible
EDGE_WIDTH  = 1.0                    # was 0.5 — int(0.5)=0 made lines invisible

# ── Axis arrows (X=red, Y=green, Z=blue) ───────────────────────────────────
AXIS_X_COLOR = (0.85, 0.15, 0.15, 0.75)
AXIS_Y_COLOR = (0.15, 0.70, 0.15, 0.75)
AXIS_Z_COLOR = (0.15, 0.15, 0.85, 0.75)
AXIS_WIDTH   = 2.0

# ── Node markers ───────────────────────────────────────────────────────────
NODE_HUE_STEP   = 0.38196601125  # golden angle in [0, 1] — maximally spreads hues
NODE_SATURATION = 0.80
NODE_VALUE      = 0.88
NODE_SIZE_MIN   = 2.0
NODE_SIZE_MAX   = 20.0
