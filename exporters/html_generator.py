import datetime
from core.constants import APP_VERSION
from jinja2 import Environment, FileSystemLoader
from core.utils import resource_path

class HTMLExporter:
    def generate(self, plugins, output_path, theme_colors=None) -> bool:

        if theme_colors is None:
            theme_colors = {"ACCENT": "#10b981", "BG_APP": "#09090b", "BG_CARD": "#18181b"}

        total = len(plugins)
        total_instances = sum(len(p.instances) for p in plugins)

        stats = {
            "version": APP_VERSION,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total": total,
            "instances": total_instances
        }

        template_dir = resource_path("exporters/templates")
        env = Environment(loader=FileSystemLoader(template_dir))

        try:
            template = env.get_template('report.html')
        except Exception as e:
            return False

        html_content = template.render(plugins=plugins, stats=stats, colors=theme_colors)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            return True
        except Exception as e:
            return False