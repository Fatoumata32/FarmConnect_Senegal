"""
Custom template filters for advice app
"""
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
import re

register = template.Library()


@register.filter(name='markdown_bold')
def markdown_bold(text):
    """
    Convert **text** to <strong>text</strong> for bold formatting
    Also converts newlines to <br> tags for proper display

    Security: Escapes HTML before processing to prevent XSS attacks
    """
    if not text:
        return ''

    # First, escape HTML to prevent XSS attacks
    text = escape(text)

    # Convert **text** to <strong>text</strong>
    # Note: We use &lt;strong&gt; after escaping, then convert back
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

    # Convert newlines to <br> tags
    text = text.replace('\n', '<br>')

    return mark_safe(text)
