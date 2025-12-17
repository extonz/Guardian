"""
Sistema de exportación avanzada - Genera reportes en múltiples formatos
"""
import json
import csv
from datetime import datetime
import os


class AdvancedExporter:
    """Exporta datos en múltiples formatos (JSON, CSV, TXT)."""
    
    def __init__(self, data_path="data/"):
        self.data_path = data_path
        os.makedirs(data_path, exist_ok=True)
    
    def export_to_json(self, data, filename="report"):
        """Exporta a JSON."""
        filepath = os.path.join(self.data_path, f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filepath
    
    def export_to_csv(self, data_list, filename="report"):
        """Exporta a CSV."""
        if not data_list:
            return None
        
        filepath = os.path.join(self.data_path, f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data_list[0].keys())
            writer.writeheader()
            writer.writerows(data_list)
        
        return filepath
    
    def export_to_txt(self, content, filename="report"):
        """Exporta a TXT con formato readable."""
        filepath = os.path.join(self.data_path, f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"REPORTE GUARDIAN - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            f.write(content)
        
        return filepath
    
    def generate_weekly_report(self, stats_data):
        """Genera reporte semanal."""
        report_content = f"""
REPORTE SEMANAL DE PRODUCTIVIDAD
Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

RESUMEN:
- Tiempo de enfoque total: {stats_data.get('focus_time', 0)} minutos
- Aplicaciones bloqueadas: {stats_data.get('blocks_count', 0)}
- Sesiones completadas: {stats_data.get('sessions', 0)}
- Score de productividad: {stats_data.get('productivity_score', 0)}/100

APPS MÁS BLOQUEADAS:
{self._format_app_list(stats_data.get('top_blocked_apps', []))}

RECOMENDACIONES:
{self._generate_recommendations(stats_data)}
"""
        return self.export_to_txt(report_content, "weekly_report")
    
    def _format_app_list(self, apps):
        """Formatea lista de apps."""
        if not apps:
            return "Ninguna"
        return "\n".join([f"  - {app['name']}: {app['count']} bloqueos" for app in apps[:10]])
    
    def _generate_recommendations(self, stats_data):
        """Genera recomendaciones basadas en estadísticas."""
        recommendations = []
        
        if stats_data.get('focus_time', 0) < 120:
            recommendations.append("  ⚠️ Tu tiempo de enfoque está por debajo de lo recomendado (120 min/día)")
        
        if stats_data.get('blocks_count', 0) > 20:
            recommendations.append("  ⚠️ Muchas distracciones detectadas, considera aumentar restricciones")
        
        if stats_data.get('productivity_score', 0) > 80:
            recommendations.append("  ✅ ¡Excelente productividad! Mantén este ritmo")
        
        return "\n".join(recommendations) if recommendations else "  ✅ Tu productividad es sostenible"
