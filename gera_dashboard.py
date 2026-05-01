import yaml

plan = yaml.safe_load(open('plan.yml', encoding='utf-8'))

cards = []
for i, p in enumerate(plan['phases']):
    tasks = p.get('tasks', [])
    done = sum(1 for t in tasks if t['status'] == 'done')
    total = len(tasks)
    pct = int(done/total*100) if total else 0
    active = 'active' if i == 0 else ''
    cards.append(f'''
<div class="card {active}">
  <div style="font-size:12px;color:#6b7280">Fase {i+1}</div>
  <div style="font-weight:600">{p["name"]}</div>
  <div style="font-size:12px;margin-top:4px">{pct}%</div>
  <div class="progress"><div style="width:{pct}%"></div></div>
</div>''')

phase = plan['phases'][0]
tasks_html = []
for t in phase['tasks']:
    status = t['status']
    icon = '✓' if status == 'done' else '▶' if status == 'in_progress' else '○'
    cls = 'done' if status == 'done' else 'prog' if status == 'in_progress' else 'todo'
    tag = f"<span class='tag'>{t['tags'][0]}</span>" if t.get('tags') else ''
    desc = f"<div style='font-size:12px;color:#6b7280;margin-top:4px'>{t.get('description','')}</div>" if t.get('description') else ''
    tasks_html.append(f'''
<div class="task"><span class="{cls}">{icon}</span><div><div>{t["title"]}</div>{desc}</div>{tag}</div>''')

html = f'''<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><title>Plano</title>
<style>
body{{font-family:system-ui;background:#f6f7f9;margin:0;padding:24px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:24px}}
.card{{background:white;padding:16px;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.08);border:2px solid transparent}}
.card.active{{border-color:#3b82f6}}
.progress{{height:6px;background:#e5e7eb;border-radius:3px;overflow:hidden;margin-top:8px}}
.progress>div{{height:100%;background:#3b82f6}}
.task{{background:white;padding:12px 16px;border-radius:8px;margin-bottom:8px;display:flex;gap:8px}}
.done{{color:#16a34a}} .prog{{color:#eab308}} .todo{{color:#9ca3af}}
.tag{{background:#eef2ff;color:#4338ca;font-size:11px;padding:2px 6px;border-radius:4px;margin-left:auto}}
</style></head>
<body>
<h1>Plano de Arquitetura</h1>
<div class="grid">{''.join(cards)}</div>
<h2>{phase["name"]} - {sum(1 for t in phase["tasks"] if t["status"]=="done")}/{len(phase["tasks"])} concluídos</h2>
<div>{''.join(tasks_html)}</div>
</body></html>'''

open('index.html', 'w', encoding='utf-8').write(html)
print("index.html gerado")
