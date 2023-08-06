from pathlib import Path

from jinja2 import Template

template_path = Path(__file__).parent / "skeleton.jinja2"


def say(text: str) -> str:
    """Return an ASCII art skeleton with a speech bubble

    Args:
        text: What to put in the speech bubble

    >>> print(say("Hello")[1:28])
     -------
    ( Hello )
     -------
    """
    template = Template(template_path.read_text())
    return template.render(text=text)
