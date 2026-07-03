"""
Max Gym GHL — Flask Blueprint Server
======================================
Sirve todos los HTML de Max Gym + archivos estáticos.
Rutas HTML:
  /dashboard      → Sprint_Dashboard_MAX_GYM.html
  /ghl-workflows → workflows-dashboard.html
  + 15 artefactos más (strategy-brief, conversation-flow, etc.)
Rutas estáticas:
  /screenshots/<file>   → screenshots/
  /research/<file>      → research/
  /assets/<file>        → assets/
"""

from flask import Flask, redirect, send_from_directory, Response, request, abort
import os

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(BASE, 'templates')

ROUTES = {
    '/dashboard':           'Sprint_Dashboard_MAX_GYM.html',
    '/ghl-workflows':       'workflows-dashboard.html',
    '/strategy-brief':      '01_Strategy_Brief.html',
    '/bot-pipeline-map':    '02_Bot_Pipeline_Map.html',
    '/conversation-flow':   '02_Conversation_Flow.html',
    '/custom-fields':       '03_Custom_Fields_Table.html',
    '/bot-agent-summary':   '04_Bot_Agent_Summary.html',
    '/ai-agent-actions':    '05_AI_Agent_Actions.html',
    '/pipeline-stage-map':  '06_Pipeline_Stage_Map.html',
    '/calendar-config':     '07_User_Calendar_Config.html',
    '/whatsapp-templates':  '08_WhatsApp_Templates.html',
    '/email-templates':      '09_Email_Templates.html',
    '/workflow-templates':   '10_Workflow_Templates.html',
    '/tags-map':            '11_Tags_Map.html',
    '/landing-mockup':      '12_Landing_Page_Mockup.html',
    '/business-profile':     '13_Business_Profile_Settings.html',
    '/knowledgebase':       '14_Knowledgebase_Content.html',
}

# Alias /artifacts/NN_<name>.html → same HTML file
ARTIFACT_ALIAS = {
    '01_Strategy_Brief.html':          '/strategy-brief',
    '02_Bot_Pipeline_Map.html':        '/bot-pipeline-map',
    '02_Conversation_Flow.html':       '/conversation-flow',
    '03_Custom_Fields_Table.html':     '/custom-fields',
    '04_Bot_Agent_Summary.html':       '/bot-agent-summary',
    '05_AI_Agent_Actions.html':        '/ai-agent-actions',
    '06_Pipeline_Stage_Map.html':      '/pipeline-stage-map',
    '07_User_Calendar_Config.html':    '/calendar-config',
    '08_WhatsApp_Templates.html':     '/whatsapp-templates',
    '09_Email_Templates.html':         '/email-templates',
    '10_Workflow_Templates.html':      '/workflow-templates',
    '11_Tags_Map.html':               '/tags-map',
    '12_Landing_Page_Mockup.html':     '/landing-mockup',
    '13_Business_Profile_Settings.html': '/business-profile',
    '14_Knowledgebase_Content.html':  '/knowledgebase',
}

# Also serve these from /artifacts/ (no NN_ prefix) to handle relative links in HTML
ARTIFACT_SIMPLE = {
    'artifacts/Strategy_Brief.html':        '/strategy-brief',
    'artifacts/Bot_Pipeline_Map.html':      '/bot-pipeline-map',
    'artifacts/Conversation_Flow.html':     '/conversation-flow',
    'artifacts/Custom_Fields_Table.html':   '/custom-fields',
    'artifacts/Bot_Agent_Summary.html':    '/bot-agent-summary',
    'artifacts/AI_Agent_Actions.html':      '/ai-agent-actions',
    'artifacts/Pipeline_Stage_Map.html':   '/pipeline-stage-map',
    'artifacts/User_Calendar_Config.html':  '/calendar-config',
    'artifacts/WhatsApp_Templates.html':   '/whatsapp-templates',
    'artifacts/Email_Templates.html':       '/email-templates',
    'artifacts/Workflow_Templates.html':    '/workflow-templates',
    'artifacts/Tags_Map.html':            '/tags-map',
    'artifacts/Landing_Page_Mockup.html':   '/landing-mockup',
    'artifacts/Business_Profile_Settings.html': '/business-profile',
    'artifacts/Knowledgebase_Content.html': '/knowledgebase',
}

NAV = [
    ('/dashboard',          '📊 Dashboard',        'Sprint Dashboard — 5 stages, 13 workflows'),
    ('/ghl-workflows',      '⚡ Workflows',         'Workflow Builder — visual panels por workflow'),
    ('/strategy-brief',     '📋 Strategy Brief',    'Brand strategy, goals, target audience'),
    ('/conversation-flow',  '🔀 Conversation Flow', 'Phase 0-5 bot flow con branching'),
    ('/bot-agent-summary',  '🤖 Bot Agent',           'AI Agent config — personality, objectives, DQ'),
    ('/ai-agent-actions',   '⚙️ AI Actions',        'Bot actions dentro del conversation flow'),
    ('/pipeline-stage-map', '🔗 Pipeline',           '5 stages del pipeline con acciones'),
    ('/custom-fields',      '📝 Custom Fields',     '17 campos personalizados'),
    ('/calendar-config',    '📅 Calendar',          'Integración calendario para booking'),
    ('/whatsapp-templates','💬 WhatsApp',           'Plantillas WhatsApp del bot'),
    ('/email-templates',    '📧 Email',             'Secuencia de emails automatizados'),
    ('/workflow-templates', '⚡ WF Templates',       '13 templates de workflows GHL'),
    ('/tags-map',          '🏷️ Tags',              'Tags de clasificación de contactos'),
    ('/knowledgebase',      '📚 Knowledge Base',     'Contenido del AI Agent knowledge base'),
    ('/landing-mockup',    '🎨 Landing Page',      'Mockup landing para ads'),
    ('/business-profile',   '🏢 Business Profile', 'Google Business Profile config'),
]


def nav_html(current_path: str) -> str:
    items = ''.join(
        f'<li><a href="{r}" class="active" title="{d}">{l}</a></li>'
        if current_path == r
        else f'<li><a href="{r}" title="{d}">{l}</a></li>'
        for r, l, d in NAV
    )
    return f'''<style>
:root{{--bg:#0d1117;--surface:#161b22;--border:#30363d;--text:#e6edf3;--muted:#8b949e;--primary:#6366f1;--green:#3fb950}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.5}}
nav{{background:var(--surface);border-bottom:1px solid var(--border);padding:0 1rem;position:sticky;top:0;z-index:100}}
nav ul{{display:flex;list-style:none;gap:0;overflow-x:auto;max-width:1600px;margin:0 auto;padding:0}}
nav li{{flex-shrink:0}}
nav a{{display:block;padding:0.75rem 1rem;color:var(--muted);text-decoration:none;font-size:0.875rem;border-bottom:2px solid transparent;white-space:nowrap;transition:color .15s,border-color .15s}}
nav a:hover{{color:var(--text);background:rgba(255,255,255,.05)}}
nav a.active{{color:var(--primary);border-bottom-color:var(--primary);font-weight:600}}
main{{max-width:1600px;margin:0 auto;padding:1.5rem}}
</style><nav><ul>{items}</ul></nav>'''


def inject_nav(content: bytes, current_path: str) -> bytes:
    nav = nav_html(current_path).encode()
    body_tag_lower = b'<body'
    body_tag_upper = b'<BODY'
    idx = None
    for tag in [body_tag_lower, body_tag_upper]:
        if tag in content:
            idx = content.index(tag)
            end_idx = content.index(b'>', idx) + 1
            break
    if idx is not None:
        return content[:end_idx] + nav + content[end_idx:]
    return nav + content


# ── Static file serving ───────────────────────────────────────────────────────
STATIC = {
    '/screenshots': os.path.join(BASE, 'screenshots'),
    '/research':    os.path.join(BASE, 'research'),
    '/assets':      os.path.join(BASE, 'assets'),
}


@app.route('/screenshots/<path:filename>')
@app.route('/research/<path:filename>')
@app.route('/assets/<path:filename>')
def serve_static(filename):
    for prefix, dir_path in STATIC.items():
        if request.path.startswith(prefix):
            safe = os.path.normpath(os.path.join(dir_path, filename))
            if not safe.startswith(dir_path):
                abort(403)
            if os.path.isfile(safe):
                return send_from_directory(dir_path, filename)
            return f"File not found: {filename}", 404
    abort(404)


# ── HTML routes ──────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return redirect('/dashboard')


@app.route('/<path:route>')
def serve_html(route):
    route = '/' + route.strip('/')

    # Handle /artifacts/NN_<name>.html → redirect to canonical route
    if route.startswith('/artifacts/'):
        filename = route[len('/artifacts/'):]
        if filename in ARTIFACT_ALIAS:
            return redirect(ARTIFACT_ALIAS[filename])
        return {'error': f"Unknown artifact '{filename}'",
                'available': list(ARTIFACT_ALIAS.keys())}, 404

    # Handle relative artifacts/ links embedded in HTML (e.g. href="artifacts/Strategy_Brief.html")
    if route in ARTIFACT_SIMPLE:
        return redirect(ARTIFACT_SIMPLE[route])

    if route not in ROUTES:
        return {'error': f"Unknown route '{route}'", 'available': list(ROUTES.keys())}, 404

    filename = ROUTES[route]
    filepath = os.path.join(TEMPLATES, filename)

    if not os.path.isfile(filepath):
        return f"Template '{filename}' not found on server", 500

    with open(filepath, 'rb') as f:
        content = f.read()

    content = inject_nav(content, route)
    return Response(content, mimetype='text/html')


if __name__ == '__main__':
    print("\n🚀 Max Gym GHL Flask Server")
    print("=" * 50)
    for r in ROUTES:
        print(f"  {r:25} → {ROUTES[r]}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=False)
