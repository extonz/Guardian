"""
Sistema de reportes y estadÃ­sticas avanzadas.
Genera reportes PDF, grÃ¡ficos, comparativas.
"""

from datetime import datetime, timedelta
from src.settings_manager import load_stats
import json

def get_daily_stats(date=None):
    """Obtiene estadÃ­sticas de un dÃ­a especÃ­fico."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    stats = load_stats()
    blocks = stats.get('blocks', [])
    
    day_blocks = [b for b in blocks if b['timestamp'].startswith(date)]
    
    app_counts = {}
    for block in day_blocks:
        app = block['app']
        app_counts[app] = app_counts.get(app, 0) + 1
    
    return {
        'date': date,
        'total_blocks': len(day_blocks),
        'apps_blocked': app_counts,
        'most_blocked': max(app_counts, key=app_counts.get) if app_counts else None,
        'hours_active': len(set([b['timestamp'].split('T')[1].split(':')[0] for b in day_blocks]))
    }

def get_weekly_stats():
    """Obtiene estadÃ­sticas de la Ãºltima semana."""
    stats = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        stats.append(get_daily_stats(date))
    return stats

def get_monthly_stats():
    """Obtiene estadÃ­sticas del mes actual."""
    stats = []
    today = datetime.now()
    for i in range(today.day):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        stats.append(get_daily_stats(date))
    return stats

def get_top_blocked_apps(days=7):
    """Obtiene las apps mÃ¡s bloqueadas en los Ãºltimos N dÃ­as."""
    stats = load_stats()
    blocks = stats.get('blocks', [])
    
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    recent_blocks = [b for b in blocks if b['timestamp'] > cutoff_date]
    
    app_counts = {}
    for block in recent_blocks:
        app = block['app']
        app_counts[app] = app_counts.get(app, 0) + 1
    
    return sorted(app_counts.items(), key=lambda x: x[1], reverse=True)

def get_usage_comparison(week1_start, week2_start):
    """Compara el uso de dos semanas."""
    week1_stats = []
    week2_stats = []
    
    for i in range(7):
        week1_stats.append(get_daily_stats((week1_start + timedelta(days=i)).strftime("%Y-%m-%d")))
        week2_stats.append(get_daily_stats((week2_start + timedelta(days=i)).strftime("%Y-%m-%d")))
    
    week1_total = sum(s['total_blocks'] for s in week1_stats)
    week2_total = sum(s['total_blocks'] for s in week2_stats)
    
    improvement = ((week1_total - week2_total) / week1_total * 100) if week1_total > 0 else 0
    
    return {
        'week1': {'start': week1_start.strftime("%Y-%m-%d"), 'total': week1_total},
        'week2': {'start': week2_start.strftime("%Y-%m-%d"), 'total': week2_total},
        'improvement': improvement,
        'direction': 'mejor' if improvement > 0 else 'peor'
    }

def generate_csv_report(filename, days=7):
    """Genera reporte en formato CSV."""
    import csv
    
    stats_data = load_stats()
    blocks = stats_data.get('blocks', [])
    
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    recent_blocks = [b for b in blocks if b['timestamp'] > cutoff_date]
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'App', 'Date', 'Time'])
            
            for block in recent_blocks:
                ts = block['timestamp']
                date, time = ts.split('T')
                writer.writerow([ts, block['app'], date, time])
        
        return True
    except Exception as e:
        print(f"Error generando CSV: {e}")
        return False

def generate_json_report(filename, days=7):
    """Genera reporte en formato JSON."""
    stats = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        stats.append(get_daily_stats(date))
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error generando JSON: {e}")
        return False

def generate_pdf_report(filename, days=7):
    """Genera reporte en PDF (requiere reportlab o similar)."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # TÃ­tulo
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#3498db'),
            spaceAfter=30
        )
        elements.append(Paragraph("ðŸ“Š Reporte Guardian", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Datos de la semana
        weekly = get_weekly_stats()
        table_data = [['Fecha', 'Bloques', 'Horas Activas', 'App Principal']]
        
        for stat in weekly:
            app = stat.get('most_blocked', 'N/A')
            table_data.append([
                stat['date'],
                str(stat['total_blocks']),
                str(stat['hours_active']),
                app
            ])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        return True
    except ImportError:
        print("âš ï¸ Para generar PDF requiere: pip install reportlab")
        return False
    except Exception as e:
        print(f"Error generando PDF: {e}")
        return False

def get_progress_percentage():
    """Calcula el porcentaje de reducciÃ³n de distracciones."""
    week_ago = datetime.now() - timedelta(days=7)
    two_weeks_ago = datetime.now() - timedelta(days=14)
    
    comparison = get_usage_comparison(two_weeks_ago, week_ago)
    return max(0, comparison['improvement'])

