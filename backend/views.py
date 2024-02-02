from fastapi import APIRouter, Response, Query
from slugify import slugify
from urllib.parse import urlparse, urlunparse


def text(content: str) -> Response:
    return Response(content=content, media_type="text/plain")


api = APIRouter()


@api.get("/healthz")
def healthz() -> Response:
    return text("healthy!")


@api.get("/slugify")
def slugify_name(name: str, is_bpl: bool = Query(default=False, alias="is-bpl")) -> Response:
    if not name:
        return text("")

    slug = slugify(name)
    if is_bpl:
        slug = f"bpl-{slug}"
    return text(slug)


@api.get("/reflected-url")
def reflected_url(
    join_url_mocked: bool = Query(default=False, alias="join-url-mocked"),
    join_url: str = Query(default="", alias="join-url"),
    export_url_mocked: bool = Query(default=False, alias="export-url-mocked"),
    export_url: str = Query(default="", alias="export-url"),
) -> Response:
    url = join_url or export_url
    if not url:
        return text("")

    parts = urlparse(url)
    if not parts.netloc:
        return text("")

    mocked = join_url_mocked or export_url_mocked

    slug = slugify(parts.netloc)

    if mocked:
        path = parts.path.strip("/")
        netloc = "api-reflector.olympus"
        path = f"mock/{slug}/{path}"
        url = urlunparse(
            (parts.scheme, netloc, path, parts.params, parts.query, parts.fragment)
        )
    else:
        url = ""

    return text(url)


@api.post("/plans")
def create_plan() -> Response:
    return text("no")
