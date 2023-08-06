import subprocess
import xml.etree.ElementTree as xml
from datetime import date
from logging import error
from pathlib import Path
from typing import Set

import chevron  # type: ignore

import yatte
from yatte import task
from yatte.utils import check_envvars, is_newer, mkdir, run, stderr

docs = Path("docs")
pages = docs / "pages"
static = docs / "static"
scd = docs / "man" / "yatte.1.scd"
page_template = docs / "templates" / "page.html"
outdir = docs / "_built"
man = outdir / "yatte.1"
tarball = outdir / "site.tar.gz"

version_file = Path(yatte.__file__)


@task("man")
def render_man():
    """Generate user manual."""
    if not uptodate(man, deps={scd, version_file}):
        mkdir(man.parent)
        scdoc2man(scd, man)


@task("docs")
def render_docs_site():
    """Generate documentation site."""
    mkdir(outdir)
    cp(static / "style.css", outdir / "style.css")

    template = page_template.read_text()

    for page in pages.glob("*.html"):
        out_html = outdir / page.name
        if not uptodate(out_html, deps={page, page_template}):
            render_page(page, template, out_html)


@task("publish")
def upload_docs():
    """Upload documentation site."""
    if check_envvars({"PAGES_SRHT_TOKEN"}):
        error("Environment variable PAGES_SRHT_TOKEN is undefined; cannot upload docs.")
        raise SystemExit(1)

    render_docs_site()
    render_man()
    tar_docs()
    url = "https://pages.sr.ht/publish/yatte.javiljoen.net"
    run(f'curl --oauth2-bearer "$PAGES_SRHT_TOKEN" -Fcontent=@{tarball} {url}')


# Helper functions


def pipe(cmd: str, input=None) -> str:
    """Run a shell command and return its stdout output.

    If `input` is not None, pipes in the text via stdin.
    """
    p = subprocess.run(cmd, shell=True, input=input, capture_output=True, text=True)
    if p.stderr:
        stderr(p.stderr)
    if p.returncode:
        raise SystemExit(p.returncode)
    return p.stdout


def scdoc2man(scd: Path, man: Path):
    """Convert manual in scdoc format to man format."""
    stderr(f"$ chevron {scd} | scdoc > {man}")
    scdoc = chevron.render(scd.read_text(), {"version": yatte.__version__})
    pipe(f"scdoc > {man}", input=scdoc)


def cp(src: Path, dest: Path):
    if not dest.is_file() or is_newer(src, than=dest):
        run(f"cp -p {src} {dest}")


def uptodate(f: Path, deps: Set[Path]) -> bool:
    # like is_newer() but takes multiple files as 2nd arg.
    return f.is_file() and all(f.stat().st_mtime > d.stat().st_mtime for d in deps)


def render_page(page: Path, template: str, out_html: Path):
    """Inject page into template and write to HTML file."""
    content = page.read_text()

    try:
        title = get_title(content)
    except (ValueError, xml.ParseError) as e:
        error(f"{e} in {page}")
        raise SystemExit(1)

    data = {"title": f"{title} | yatte", "content": content, "date": date.today()}
    stderr(f"chevron {page} {page_template} > {out_html}")
    rendered = chevron.render(template, data)
    out_html.write_text(rendered)


def get_title(doc: str) -> str:
    """Return body of first h1 element in an HTML document.

    The doc must be a well-formed XML snippet:
    self-closing tags; all content wrapped in an outer element.
    """
    h1 = xml.fromstring(doc).find("h1")

    if h1 is None or h1.text is None:
        raise ValueError("missing <h1> as child of document root")

    return h1.text


def tar_docs():
    """Create a tarball from the contents of `outdir`."""
    # Prevent an old tarball from being included in the new one:
    tarball.unlink(missing_ok=True)
    # Write the tarball to a separate folder first,
    # to prevent it including a partial version of itself:
    run(f"f=$(mktemp); tar -C {outdir} -czv . > $f && mv $f {tarball}")
