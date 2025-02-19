# seo_sentinel.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rich.console import Console
from rich.table import Table
from rich import box
import time

# Import fungsi generate_pdf_report dari file generate_pdf.py
from generate_pdf import generate_pdf_report

console = Console()

# ============================
# Fungsi Validasi URL
# ============================
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

# ============================
# Fungsi Analisa SEO
# ============================
def check_missing_alts(soup):
    images = soup.find_all('img')
    missing = []
    for img in images:
        alt = img.get("alt", "").strip()
        if not alt:
            src = img.get("src", "No src")
            missing.append(src)
    return missing

def check_broken_links(links):
    broken = []
    for link in links:
        try:
            # Menggunakan HEAD untuk efisiensi
            response = requests.head(link, timeout=5)
            if response.status_code >= 400:
                broken.append(link)
        except requests.RequestException:
            broken.append(link)
    return broken

def get_meta_description(soup):
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content", "").strip():
        return meta_desc["content"].strip()
    return None

def generate_recommendations(data):
    recs = []
    # Meta description
    meta_desc = data.get("meta_description")
    if not meta_desc:
        recs.append("Tambahkan meta description yang relevan untuk meningkatkan rangkuman halaman di hasil pencarian.")
    else:
        if len(meta_desc) < 50:
            recs.append("Meta description terlalu pendek. Pertimbangkan untuk menambahkan lebih banyak detail (minimal 50 karakter).")
        elif len(meta_desc) > 160:
            recs.append("Meta description terlalu panjang. Usahakan tidak melebihi 160 karakter agar tidak terpotong di hasil pencarian.")
    # Struktur Heading
    h1_count = len(data.get("headings", {}).get("h1", []))
    if h1_count == 0:
        recs.append("Halaman tidak memiliki tag H1. Tambahkan tag H1 yang mencerminkan topik utama halaman.")
    elif h1_count > 1:
        recs.append("Terdapat lebih dari satu tag H1. Pertimbangkan untuk hanya memiliki satu tag H1 per halaman untuk hierarki yang jelas.")
    # Gambar tanpa alt
    missing_alts = data.get("missing_alts", [])
    if missing_alts:
        recs.append(f"Terdapat {len(missing_alts)} gambar tanpa atribut alt. Tambahkan atribut alt untuk meningkatkan SEO gambar.")
    # Broken Links
    broken_links = data.get("broken_links", [])
    if broken_links:
        recs.append(f"Terdapat {len(broken_links)} broken link. Periksa dan perbaiki link-link yang tidak berfungsi.")
    return recs

def crawl_seo(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        console.print(f"[red]Gagal mengambil halaman: {url}[/red]\nError: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    # Judul halaman
    title = soup.title.string.strip() if soup.title and soup.title.string else "Tidak ada judul"
    
    # Meta tags
    meta_tags = soup.find_all("meta")
    meta_data = []
    for tag in meta_tags:
        attrs = { key: value for key, value in tag.attrs.items() }
        meta_data.append(attrs)
    
    # Headings (h1 hingga h6)
    headings = {}
    for level in range(1, 7):
        tag = f"h{level}"
        headings[tag] = [h.get_text(strip=True) for h in soup.find_all(tag)]
    
    # Internal links
    domain = urlparse(url).netloc
    internal_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        parsed_href = urlparse(href)
        if parsed_href.netloc == "" or parsed_href.netloc == domain:
            full_url = urljoin(url, href)
            internal_links.append(full_url)
    internal_links = list(set(internal_links))
    
    # Error SEO: missing alt & broken links
    missing_alts = check_missing_alts(soup)
    broken_links = check_broken_links(internal_links)
    meta_description = get_meta_description(soup)
    
    result = {
        "url": url,
        "title": title,
        "meta": meta_data,
        "headings": headings,
        "internal_links": internal_links,
        "missing_alts": missing_alts,
        "broken_links": broken_links,
        "meta_description": meta_description,
    }
    result["recommendations"] = generate_recommendations(result)
    return result

# ============================
# Tampilan Data di Terminal
# ============================
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
        headings_list = data["headings"].get(tag, [])
        if headings_list:
            heading_table = Table(title=f"{tag.upper()} (Total: {len(headings_list)})", box=box.SIMPLE)
            heading_table.add_column("No", justify="center", style="cyan", width=4)
            heading_table.add_column("Teks", style="white")
            for i, text in enumerate(headings_list, start=1):
                heading_table.add_row(str(i), text)
            console.print(heading_table)
    
    # Tabel Internal Links
    links_table = Table(title=f"Internal Links (Total: {len(data['internal_links'])})", box=box.SIMPLE)
    links_table.add_column("No", justify="center", style="cyan", width=4)
    links_table.add_column("URL", style="white")
    for i, link in enumerate(data["internal_links"], start=1):
        links_table.add_row(str(i), link)
    console.print(links_table)
    
    # Tabel gambar tanpa alt
    if data["missing_alts"]:
        alt_table = Table(title=f"Gambar tanpa Alt (Total: {len(data['missing_alts'])})", box=box.SIMPLE)
        alt_table.add_column("No", justify="center", style="cyan", width=4)
        alt_table.add_column("Src", style="white")
        for i, src in enumerate(data["missing_alts"], start=1):
            alt_table.add_row(str(i), src)
        console.print(alt_table)
    
    # Tabel broken links
    if data["broken_links"]:
        broken_table = Table(title=f"Broken Links (Total: {len(data['broken_links'])})", box=box.SIMPLE)
        broken_table.add_column("No", justify="center", style="cyan", width=4)
        broken_table.add_column("URL", style="white")
        for i, link in enumerate(data["broken_links"], start=1):
            broken_table.add_row(str(i), link)
        console.print(broken_table)
    
    # Rekomendasi optimasi
    if data.get("recommendations"):
        console.print("\n[bold blue]Rekomendasi Optimasi:[/bold blue]")
        for rec in data["recommendations"]:
            console.print(f"- {rec}")

# ============================
# Fungsi Monitoring Berkala
# ============================
def monitor_website(url, interval=300):
    console.print(f"\n[bold cyan]Monitoring dimulai untuk {url}.[/bold cyan]")
    console.print(f"Memeriksa perubahan setiap {interval} detik...\n")
    previous_data = crawl_seo(url)
    if not previous_data:
        console.print("[red]Monitoring tidak dapat dilakukan karena gagal mengambil data awal.[/red]")
        return
    while True:
        time.sleep(interval)
        new_data = crawl_seo(url)
        if not new_data:
            console.print("[red]Gagal mengambil data terbaru. Melewati siklus ini.[/red]")
            continue
        changes = []
        if new_data['title'] != previous_data['title']:
            changes.append("Judul halaman berubah.")
        if new_data.get("meta_description", "") != previous_data.get("meta_description", ""):
            changes.append("Meta description berubah.")
        if len(new_data.get("headings", {}).get("h1", [])) != len(previous_data.get("headings", {}).get("h1", [])):
            changes.append("Jumlah tag H1 berubah.")
        if len(new_data.get("internal_links", [])) != len(previous_data.get("internal_links", [])):
            changes.append("Jumlah internal links berubah.")
        if changes:
            console.print("[bold yellow]Perubahan terdeteksi:[/bold yellow]")
            for change in changes:
                console.print(f"- {change}")
            previous_data = new_data
        else:
            console.print("[green]Tidak ada perubahan signifikan.[/green]")

# ============================
# Main Program
# ============================
if __name__ == "__main__":
    target_url = get_valid_url()
    
    # Animasi loading saat analisa SEO
    with console.status("[bold green]Melakukan analisa SEO...[/bold green]", spinner="dots"):
        data = crawl_seo(target_url)
    
    if data:
        display_seo_data(data)
        
        # Pilihan untuk membuat PDF report
        console.print("\n[bold magenta]Apakah Anda ingin membuat PDF report?[/bold magenta]")
        pdf_choice = input("Ketik 'y' untuk ya atau tekan Enter untuk melewati: ").strip().lower()
        if pdf_choice == "y":
            generate_pdf_report(data)
        
        # Pilihan untuk mengaktifkan monitoring berkala
        console.print("\n[bold magenta]Apakah Anda ingin mengaktifkan fitur monitoring berkala?[/bold magenta]")
        monitor_choice = input("Ketik 'y' untuk ya atau tekan Enter untuk keluar: ").strip().lower()
        if monitor_choice == "y":
            monitor_website(target_url, interval=300)
