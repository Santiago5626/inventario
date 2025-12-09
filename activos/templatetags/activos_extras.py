from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs passed to the tag.
    
    Usage: {% query_transform page=page_obj.next_page_number %}
    """
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()
