"""
Map frequencies to 432 Hz tuning note names and build body region associations.
In 432 Hz tuning, A4 = 432 Hz. All other notes are derived from this.
"""

import math

# 432 Hz tuning: A4 = 432 Hz
# Note names in order (C, C#, D, D#, E, F, F#, G, G#, A, A#, B)
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def hz_to_note_432(hz):
    """Convert a frequency in Hz to the nearest note name in 432 Hz tuning."""
    if hz <= 0:
        return "Sub-bass pulse"
    # A4 = 432 Hz, MIDI note 69
    # n = 12 * log2(f / 432) + 69
    n = 12 * math.log2(hz / 432) + 69
    n_rounded = round(n)
    cents_off = round((n - n_rounded) * 100)
    note_index = n_rounded % 12
    octave = (n_rounded // 12) - 1
    note_name = NOTE_NAMES[note_index]
    cents_str = f" (+{cents_off}¢)" if cents_off > 5 else (f" ({cents_off}¢)" if cents_off < -5 else "")
    return f"{note_name}{octave}{cents_str}"

# Brainwave state by Hz range
def brainwave_state(hz):
    if hz < 0.5:
        return "Sub-delta (deep modulation)"
    elif hz < 4:
        return "Delta (deep sleep, restoration)"
    elif hz < 8:
        return "Theta (deep meditation, trauma release)"
    elif hz < 14:
        return "Alpha (relaxed awareness, integration)"
    elif hz < 30:
        return "Beta (focused attention)"
    elif hz < 100:
        return "Gamma (peak coherence, insight)"
    elif hz < 500:
        return "Audible tone (direct nervous system input)"
    else:
        return "High harmonic (crystalline, structural)"

# LFSX layer assignment
def lfsx_layer(hz):
    if hz < 20:
        return "foundation"  # sub-bass / earth tones
    elif hz < 300:
        return "foundation"  # low foundational tones
    elif hz < 600:
        return "mid"         # mid-tier modulations
    elif hz < 1000:
        return "binaural"    # binaural/spatial
    elif hz < 2000:
        return "crystalline" # high harmonic
    else:
        return "seal"        # crescendo seal

freqs = [
    {"hz": 7.83,   "name": "Schumann Resonance",          "cat": "grounding",     "archetype": "Earth Anchor"},
    {"hz": 14.1,   "name": "Schumann Harmonic 2",         "cat": "grounding",     "archetype": "Vitality Root"},
    {"hz": 40,     "name": "Gamma Coherence Shield",       "cat": "protective",    "archetype": "The Sentinel"},
    {"hz": 111,    "name": "Cell Regeneration",            "cat": "healing",       "archetype": "The Regenerator"},
    {"hz": 136.1,  "name": "OM — Earth Year",              "cat": "healing",       "archetype": "The Heartbeat"},
    {"hz": 174,    "name": "Foundation & Safety",          "cat": "solfeggio",     "archetype": "The Foundation Stone"},
    {"hz": 194.18, "name": "Earth Day Frequency",          "cat": "grounding",     "archetype": "The Circadian Keeper"},
    {"hz": 210.42, "name": "Synodic Moon",                 "cat": "grounding",     "archetype": "The Tide Turner"},
    {"hz": 256,    "name": "Middle C — Natural Tone",      "cat": "healing",       "archetype": "The Ground Note"},
    {"hz": 285,    "name": "Tissue Repair / Field Repair", "cat": "solfeggio",     "archetype": "The Restorer"},
    {"hz": 321,    "name": "Immune Activation",            "cat": "healing",       "archetype": "The Defender"},
    {"hz": 333,    "name": "Heart-Mind Bridge",            "cat": "consciousness", "archetype": "The Bridge Builder"},
    {"hz": 360,    "name": "Heart Field Coherence",        "cat": "healing",       "archetype": "The Heart Keeper"},
    {"hz": 396,    "name": "Liberation from Fear",         "cat": "solfeggio",     "archetype": "The Liberator"},
    {"hz": 417,    "name": "Cellular Clearing",            "cat": "solfeggio",     "archetype": "The Cleanser"},
    {"hz": 432,    "name": "Universal Tuning",             "cat": "solfeggio",     "archetype": "The Anchor"},
    {"hz": 528,    "name": "DNA Repair & Transformation",  "cat": "solfeggio",     "archetype": "The Transformer"},
    {"hz": 639,    "name": "Harmonising Relationships",    "cat": "solfeggio",     "archetype": "The Connector"},
    {"hz": 741,    "name": "Cellular Detox & Clarity",     "cat": "solfeggio",     "archetype": "The Clarifier"},
    {"hz": 852,    "name": "Pineal & Nervous System",      "cat": "solfeggio",     "archetype": "The Seer"},
    {"hz": 888,    "name": "Infinite Abundance",           "cat": "lfsx",          "archetype": "The Infinite Loop"},
    {"hz": 963,    "name": "Crown & Divine Connection",    "cat": "solfeggio",     "archetype": "The Crown"},
    {"hz": 999,    "name": "Completion & Transcendence",   "cat": "lfsx",          "archetype": "The Completer"},
    {"hz": 1074,   "name": "Mitochondrial Activation",     "cat": "healing",       "archetype": "The Energiser"},
    {"hz": 1111,   "name": "Alignment Gateway",            "cat": "lfsx",          "archetype": "The Gateway"},
    {"hz": 1331,   "name": "Crystalline Activation",       "cat": "lfsx",          "archetype": "The Crystal"},
    {"hz": 1500,   "name": "Celestial Bridge",             "cat": "lfsx",          "archetype": "The Bridge"},
    {"hz": 1777,   "name": "Divine Architecture",          "cat": "lfsx",          "archetype": "The Architect"},
    {"hz": 9999,   "name": "Harmonic Completion Seal",     "cat": "lfsx",          "archetype": "The Seal"},
]

print("FREQUENCY NOTE MAP (432 Hz tuning)")
print("=" * 80)
for f in freqs:
    note = hz_to_note_432(f["hz"])
    bw = brainwave_state(f["hz"])
    layer = lfsx_layer(f["hz"])
    print(f"  {f['hz']:8.2f} Hz | {note:12s} | {layer:12s} | {bw}")
    f["note"] = note
    f["brainwave"] = bw
    f["layer"] = layer

# Body region associations
print("\n\nBODY REGION FREQUENCY ASSOCIATIONS")
print("=" * 80)

body_regions = {
    "head": {
        "label": "Head & Mind",
        "desc": "Cognitive clarity, neural coherence, pineal activation",
        "freqs": [40, 852, 963, 1111, 741],
        "guidance": "These frequencies support neural coherence and cognitive clarity. Best used for focus, meditation, or mental pattern interruption."
    },
    "throat": {
        "label": "Throat & Expression",
        "desc": "Communication, truth, thyroid, vocal resonance",
        "freqs": [741, 639, 333, 417, 256],
        "guidance": "Associated with expression, truth-telling, and clearing what has been unsaid. Useful for communication blocks and thyroid support."
    },
    "chest": {
        "label": "Chest & Heart",
        "desc": "Heart coherence, grief, connection, lungs",
        "freqs": [360, 639, 528, 136.1, 333],
        "guidance": "Heart-centred frequencies for grief processing, relationship coherence, and cardiovascular regulation."
    },
    "solar": {
        "label": "Solar Plexus",
        "desc": "Personal power, identity, digestion, nervous system",
        "freqs": [528, 417, 321, 396, 432],
        "guidance": "Frequencies for identity, personal agency, and digestive system support. Useful when feeling powerless or stuck."
    },
    "abdomen": {
        "label": "Abdomen & Gut",
        "desc": "Gut-brain axis, ancestral patterns, reproductive system",
        "freqs": [285, 396, 174, 210.42, 194.18],
        "guidance": "The gut holds inherited patterns. These frequencies support the gut-brain axis and ancestral pattern interruption."
    },
    "spine": {
        "label": "Spine & Lower Back",
        "desc": "Structural support, nervous system highway, sacral",
        "freqs": [174, 136.1, 7.83, 194.18, 256],
        "guidance": "Foundational frequencies for structural integrity and nervous system regulation along the spinal column."
    },
    "arms": {
        "label": "Arms & Hands",
        "desc": "Action, giving, receiving, lymphatic flow",
        "freqs": [321, 639, 528, 285, 432],
        "guidance": "Frequencies associated with action, giving and receiving, and lymphatic circulation."
    },
    "legs": {
        "label": "Legs & Hips",
        "desc": "Grounding, stability, ancestral foundation, movement",
        "freqs": [7.83, 14.1, 174, 194.18, 396],
        "guidance": "Deep grounding frequencies. The legs carry inherited weight. These support physical grounding and ancestral release."
    }
}

for region, data in body_regions.items():
    print(f"\n{data['label']} ({region})")
    print(f"  {data['desc']}")
    for hz in data['freqs']:
        match = next((f for f in freqs if abs(f['hz'] - hz) < 0.5), None)
        if match:
            print(f"    {match['hz']:8.2f} Hz | {match['note']:12s} | {match['name']}")

# Save as JSON for use in the site
import json

output = {
    "freqs": freqs,
    "body_regions": body_regions
}

with open('/home/ubuntu/gh-repo/freq_data.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\n\nSaved to freq_data.json")
