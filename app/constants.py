"""
Application-wide constants and configuration values.
"""

# Post Types
POST_TYPES = [
    'init',
    'update',
    'feature',
    'fix',
    'decision',
    'learning',
    'milestone',
    'reflection'
]

# Project Status
PROJECT_STATUSES = [
    'ideation',
    'in_progress',
    'beta',
    'launched'
]

# Status to Project Stage Mapping
STATUS_TO_STAGE = {
    'ideation': 'idea',
    'in_progress': 'active_development',
    'beta': 'stabilization',
    'launched': 'maintenance'
}

# AI Configuration
DEFAULT_AI_VERSION = '1.2.0'
AI_SUMMARY_MAX_LENGTH = 10000  # characters

# Post Intent Categories
POST_INTENTS = [
    'foundation',
    'progress',
    'decision',
    'milestone',
    'reflection',
    'maintenance'
]
