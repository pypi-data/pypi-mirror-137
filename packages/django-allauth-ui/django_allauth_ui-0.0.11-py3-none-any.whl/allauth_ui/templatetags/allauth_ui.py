from django import template

register = template.Library()


socialprovider_colors = {
    "GitHub": "bg-stone-900 hover:bg-black",
    "Facebook": "bg-blue-700 hover:bg-blue-800",
    "Google": "bg-red-700 bg-red-800",
}


@register.filter()
def socialprovider_color(socialprovider):
    return socialprovider_colors.get(socialprovider.name, "bg-stone-900 hover:bg-black")
