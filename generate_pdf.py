# generate_pdf.py

from xhtml2pdf import pisa
from jinja2 import Template
from rich.console import Console

console = Console()

# Template HTML untuk laporan PDF dengan desain yang lebih menarik
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SEO Sentinel Report</title>
    <style>
        /* Reset & font */
        * {
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            background: #f7f7f7;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            text-align: center;
            margin-bottom: 20px;
        }
        h1 {
            font-size: 32px;
            color: #2c3e50;
        }
        h2 {
            font-size: 24px;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 8px;
            margin-top: 40px;
        }
        h3 {
            font-size: 20px;
            margin-top: 30px;
        }
        p {
            line-height: 1.6;
            margin: 10px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        ul {
            list-style: disc;
            margin-left: 40px;
            line-height: 1.6;
        }
        .section {
            margin-bottom: 30px;
        }
        .info {
            font-size: 16px;
            margin: 5px 0;
        }
        .info strong {
            color: #2c3e50;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>SEO Sentinel Report</h1>
        <div class="section">
            <p class="info"><strong>URL:</strong> {{ url }}</p>
            <p class="info"><strong>Judul Halaman:</strong> {{ title }}</p>
        </div>
        
        <div class="section">
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
        </div>
        
        <div class="section">
            <h2>Headings</h2>
            {% for level, texts in headings.items() %}
                <h3>{{ level | upper }} (Total: {{ texts|length }})</h3>
                <ul>
                    {% for text in texts %}
                        <li>{{ text }}</li>
                    {% endfor %}
                </ul>
            {% endfor %}
        </div>
        
        <div class="section">
            <h2>Internal Links (Total: {{ internal_links|length }})</h2>
            <ul>
                {% for link in internal_links %}
                    <li>{{ link }}</li>
                {% endfor %}
            </ul>
        </div>
        
        <div class="section">
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
        </div>
        
        <div class="section">
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
        </div>
        
        <div class="section">
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
        </div>
    </div>
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
