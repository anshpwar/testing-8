"""Consumer added independently of the base-side change (scenario 78)."""


from .contract import build_summary


def archive_row(record):
    return build_summary(record)["ref"]
