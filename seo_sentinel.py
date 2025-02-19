import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ['http', 'https'] and bool(parsed.netloc)

def get_valid_url():
    """
    Meminta input URL dari pengguna hingga didapatkan URL yang valid.
    Jika pengguna tidak menyertakan scheme (http/https), maka secara otomatis
    akan ditambahkan "http://".
    """
    while True:
        console.print("[bold yellow]Masukkan URL website yang ingin dianalisa:[/bold yellow]")
        target_url = input("URL: ").strip()
        if not target_url:
            console.print("[red]URL tidak boleh kosong. Silahkan coba lagi.[/red]")
            continue
        parsed = urlparse(target_url)
        if not parsed.scheme:
            target_url = "http://" + target_url
            parsed = urlparse(target_url)
        if is_valid_url(target_url):
            return target_url
        else:
            console.print("[red]URL tidak valid. Silahkan masukkan URL yang valid.[/red]")

def crawl_seo(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        console.print(f"[red]Gagal mengambil halaman: {url}[/red]\nError: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else "Tidak ada judul"
    
    # Mendapatkan meta tags
    meta_tags = soup.find_all("meta")
    meta_data = []
    for tag in meta_tags:
        attrs = { key: value for key, value in tag.attrs.items() }
        meta_data.append(attrs)
    
    headings = {}
    for level in range(1, 7):
        tag = f"h{level}"
        headings[tag] = [h.get_text(strip=True) for h in soup.find_all(tag)]
    
    domain = urlparse(url).netloc
    internal_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        parsed_href = urlparse(href)
        if parsed_href.netloc == "" or parsed_href.netloc == domain:
            full_url = urljoin(url, href)
            internal_links.append(full_url)
    
    result = {
        "url": url,
        "title": title,
        "meta": meta_data,
        "headings": headings,
        "internal_links": list(set(internal_links))
    }
    
    return result

def display_seo_data(data):
    console.print("\n[bold magenta]Laporan SEO Website[/bold magenta]\n", justify="center")
    console.print(f"[bold green]URL:[/bold green] {data['url']}")
    console.print(f"[bold green]Judul Halaman:[/bold green] {data['title']}\n")
    
    # Tabel Meta Tags
    meta_table = Table(title="Meta Tags", box=box.SIMPLE)
    meta_table.add_column("No", justify="center", style="cyan", width=4)
    meta_table.add_column("Atribut", style="white")
    for i, meta in enumerate(data["meta"], start=1):
        attr_str = ", ".join([f"{k}={v}" for k, v in meta.items()])
        meta_table.add_row(str(i), attr_str)
    console.print(meta_table)
    
    # Tabel Headings per level (h1 - h6)
    for level in range(1, 7):
        tag = f"h{level}"
        headings = data["headings"].get(tag, [])
        if headings:
            heading_table = Table(title=f"{tag.upper()} (Total: {len(headings)})", box=box.SIMPLE)
            heading_table.add_column("No", justify="center", style="cyan", width=4)
            heading_table.add_column("Teks", style="white")
            for i, text in enumerate(headings, start=1):
                heading_table.add_row(str(i), text)
            console.print(heading_table)
    
    # Tabel Internal Links
    links_table = Table(title=f"Internal Links (Total: {len(data['internal_links'])})", box=box.SIMPLE)
    links_table.add_column("No", justify="center", style="cyan", width=4)
    links_table.add_column("URL", style="white")
    for i, link in enumerate(data["internal_links"], start=1):
        links_table.add_row(str(i), link)
    console.print(links_table)

if __name__ == "__main__":
    target_url = get_valid_url()
    data = crawl_seo(target_url)
    if data:
        display_seo_data(data)
