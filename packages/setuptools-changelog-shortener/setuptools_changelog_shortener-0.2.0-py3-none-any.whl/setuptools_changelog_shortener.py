__version__ = "0.2.0"


def _load_toml(data):
    from tomli import loads

    return loads(data)


def _shorten_changelog(config):
    import re
    import sys

    read_from = config["read_from"]
    write_to = config["write_to"]
    count = config.get("count", 5)
    delimiter = config.get("delimiter", "^--+")
    title = config.get("title", "Changelog\n=========")
    if "bdist_rpm" in sys.argv:
        # exclude changelog when building rpm
        return ""
    with open(read_from, encoding="utf-8") as f:
        text = f.read()
    header_matches = list(re.finditer(delimiter, text, re.MULTILINE))
    # until "count" header
    count = min(count, len(header_matches))
    if count < len(header_matches):
        text = text[:header_matches[count].start()]
    # all lines without last release number
    lines = text.splitlines()[:-1]
    with open(write_to, "w", encoding="utf-8") as f:
        f.write(f"\n\n{title}\n\n\n" + "\n".join(lines))


def shorten_changelog(dist):
    import os

    config_name = "pyproject.toml"
    if not os.path.isfile(config_name):
        return
    with open(config_name, encoding="UTF-8") as f:
        data = f.read()
    config = _load_toml(data).get("tool", {}).get(
        "setuptools_changelog_shortener")
    if config is None:
        return
    return _shorten_changelog(config)
