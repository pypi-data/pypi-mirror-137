"""
providers
"""

# Alliance Auth
from esi.clients import EsiClientProvider

# AA Fleet Finder
from fleetfinder import __user_agent__

esi = EsiClientProvider(app_info_text=__user_agent__)
