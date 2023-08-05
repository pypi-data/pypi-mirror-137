from django import template

register = template.Library()


@register.inclusion_tag("highlights/footer.html", takes_context=True)
def highlight_btn_show(context, url: str):
    context["save_highlight_url"] = url
    return context
