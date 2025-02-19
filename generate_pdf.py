# generate_pdf.py

from xhtml2pdf import pisa
from jinja2 import Template
from rich.console import Console

console = Console()

# Template HTML untuk laporan PDF
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SEO Sentinel Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1, h2, h3 { color: #333; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        table, th, td { border: 1px solid #ccc; }
        th, td { padding: 8px; text-align: left; }
        ul { list-style: disc; margin-left: 20px; }
    </style>
</head>
<body>
    <h1>SEO Sentinel Report</h1>
    <p><strong>URL:</strong> {{ url }}</p>
    <p><strong>Judul Halaman:</strong> {{ title }}</p>
    
    <h2>Meta Tags</h2>
    <table>
        <thead>
            <tr>
                <th>No</th>
                <th>Atribut</th>
            </tr>
        </thead>
        <tbody>
            {% for meta in meta %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>
                    {% for key, value in meta.items() %}
                        <strong>{{ key }}:</strong> {{ value }}<br>
                    {% endfor %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <h2>Headings</h2>
    {% for level, texts in headings.items() %}
        <h3>{{ level | upper }} (Total: {{ texts|length }})</h3>
        <ul>
            {% for text in texts %}
                <li>{{ text }}</li>
            {% endfor %}
        </ul>
    {% endfor %}
    
    <h2>Internal Links (Total: {{ internal_links|length }})</h2>
    <ul>
        {% for link in internal_links %}
            <li>{{ link }}</li>
        {% endfor %}
    </ul>
    
    <h2>Gambar tanpa Alt (Total: {{ missing_alts|length }})</h2>
    {% if missing_alts %}
    <ul>
        {% for src in missing_alts %}
            <li>{{ src }}</li>
        {% endfor %}
    </ul>
    {% else %}
    <p>Tidak ada gambar yang missing alt.</p>
    {% endif %}
    
    <h2>Broken Links (Total: {{ broken_links|length }})</h2>
    {% if broken_links %}
    <ul>
        {% for link in broken_links %}
            <li>{{ link }}</li>
        {% endfor %}
    </ul>
    {% else %}
    <p>Tidak ada broken links.</p>
    {% endif %}
    
    <h2>Rekomendasi Optimasi</h2>
    {% if recommendations %}
    <ul>
        {% for rec in recommendations %}
            <li>{{ rec }}</li>
        {% endfor %}
    </ul>
    {% else %}
    <p>Tidak ada rekomendasi.</p>
    {% endif %}
</body>
</html>
"""

def generate_pdf_report(data, output_pdf='seo_report.pdf'):
    """
    Render laporan SEO ke HTML menggunakan template dan konversi ke PDF menggunakan xhtml2pdf.
    """
    template = Template(html_template)
    rendered_html = template.render(**data)
    try:
        with open(output_pdf, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(rendered_html, dest=pdf_file)
        if pisa_status.err:
            console.print(f"[red]Gagal membuat PDF report. Terdapat {pisa_status.err} error.[/red]")
        else:
            console.print(f"[bold green]PDF report berhasil dibuat: {output_pdf}[/bold green]")
    except Exception as e:
        console.print(f"[red]Gagal membuat PDF report: {e}[/red]")

if __name__ == "__main__":
    console.print("[yellow]Modul generate_pdf.py dijalankan sebagai modul utama. Harap import modul ini pada seo_sentinel.py.[/yellow]")
