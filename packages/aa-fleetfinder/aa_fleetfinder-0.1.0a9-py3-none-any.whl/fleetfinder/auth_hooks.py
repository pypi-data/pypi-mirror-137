"""
auth hooks
"""

# Django
from django.utils.translation import ugettext_lazy as _

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# AA Fleet Finder
from fleetfinder import urls


class FleetFinderMenuItem(MenuItemHook):
    """
    This class ensures only authorized users will see the menu entry
    """

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _("Fleet Finder"),
            "fas fa-users fa-fw",
            "fleetfinder:dashboard",
            navactive=["fleetfinder:"],
        )

    def render(self, request):
        """
        render
        :param request:
        :return:
        """

        if request.user.has_perm("fleetfinder.access_fleetfinder"):
            return MenuItemHook.render(self, request)

        return ""


@hooks.register("menu_item_hook")
def register_menu():
    """
    register our menu
    :return:
    """

    return FleetFinderMenuItem()


@hooks.register("url_hook")
def register_urls():
    """
    register our urls
    :return:
    """

    return UrlHook(urls, "fleetfinder", "^fleetfinder/")
