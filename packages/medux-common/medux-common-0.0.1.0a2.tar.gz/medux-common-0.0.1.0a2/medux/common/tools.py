from menu import MenuItem as SimpleMenuItem


class MenuItem(SimpleMenuItem):
    """MedUX MenuItem with permission check.

    :param required_permission list|str: You can provide a list or a string as required permission for this
        menu item. If the user doesn't have that permission, the menu item will be invisible.
    :param classes: the CSS classes that will be added to the menu item
    :param badge str|callable: a callable that returns a str with the text of a badge, if needed.
    """

    def __init__(
        self,
        *args,
        required_permissions=None,
        classes=None,
        badge=None,
        **kwargs,
    ):
        if required_permissions is None:
            required_permissions = []
        elif not type(required_permissions) == list:
            required_permissions = [required_permissions]
        self.required_permissions = required_permissions
        # TODO add callable
        self.classes = classes
        self.badge = badge
        super().__init__(*args, **kwargs)

    def process(self, request):
        if callable(self.badge):
            self.badge = self.badge(request)
        super().process(request)
