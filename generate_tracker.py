#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
留学申请可视化跟踪台账生成器
输入：JSON格式的院校数据
输出：交互式HTML跟踪台账

使用方法：
    python generate_tracker.py --input schools.json --output tracker.html
    python generate_tracker.py --input schools.json  # 默认输出 tracker.html
"""

import json
import argparse
import os
import sys

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html style="margin:0;padding:0;">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;">
<div style="background-color:transparent;box-sizing:border-box;--accent:#9BBBF4;--accent-dark:#5B7FC4;--bg:#F7F8FA;--card:#FFFFFF;--text:#1A1B1C;--text2:#6B7280;--border:#E4E3DD;--green:#52C41A;--orange:#FAAD14;--red:#EA6668;--purple:#9B7BD4;font-family:'PingFang SC','Segoe UI',Arial,sans-serif;box-sizing:border-box;">

<div id="app" style="box-sizing:border-box;">

<!-- 顶部信息 -->
<div style="background:linear-gradient(135deg,rgba(155,187,244,0.18),rgba(155,187,244,0.35));border-radius:16px;padding:20px 24px;margin-bottom:16px;box-sizing:border-box;">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:12px;">
    <div>
      <div style="font-size:18px;font-weight:600;color:var(--text);">{{APPLICANT_NAME}} · {{PROGRAM}}申请跟踪台账</div>
      <div style="font-size:12px;color:var(--text2);margin-top:4px;">{{APPLICANT_BG}} · {{TARGET_YEAR}}入学</div>
    </div>
    <div style="display:flex;gap:16px;flex-wrap:wrap;">
      <div style="text-align:center;"><div id="stat-total" style="font-size:22px;font-weight:700;color:var(--accent-dark);">{{TOTAL_SCHOOLS}}</div><div style="font-size:11px;color:var(--text2);">目标院校</div></div>
      <div style="text-align:center;"><div id="stat-submitted" style="font-size:22px;font-weight:700;color:var(--orange);">0</div><div style="font-size:11px;color:var(--text2);">已提交</div></div>
      <div style="text-align:center;"><div id="stat-offer" style="font-size:22px;font-weight:700;color:var(--green);">0</div><div style="font-size:11px;color:var(--text2);">已录取</div></div>
      <div style="text-align:center;"><div id="stat-progress" style="font-size:22px;font-weight:700;color:var(--accent-dark);">0%</div><div style="font-size:11px;color:var(--text2);">总进度</div></div>
    </div>
  </div>
</div>

<!-- Tab导航 -->
<div style="display:flex;gap:4px;margin-bottom:14px;flex-wrap:wrap;">
  <button data-tab="overview" class="tab-btn" style="padding:8px 18px;border:none;border-radius:8px 8px 0 0;font-size:13px;cursor:pointer;background:var(--accent);color:#fff;font-weight:600;min-height:40px;">📊 总览对比</button>
  <button data-tab="track" class="tab-btn" style="padding:8px 18px;border:none;border-radius:8px 8px 0 0;font-size:13px;cursor:pointer;background:#EEF0F3;color:var(--text2);font-weight:500;min-height:40px;">📋 院校跟踪</button>
  <button data-tab="timeline" class="tab-btn" style="padding:8px 18px;border:none;border-radius:8px 8px 0 0;font-size:13px;cursor:pointer;background:#EEF0F3;color:var(--text2);font-weight:500;min-height:40px;">📅 截止时间线</button>
  <button data-tab="materials" class="tab-btn" style="padding:8px 18px;border:none;border-radius:8px 8px 0 0;font-size:13px;cursor:pointer;background:#EEF0F3;color:var(--text2);font-weight:500;min-height:40px;">📝 材料清单</button>
</div>

<div id="tab-content" style="box-sizing:border-box;">

<!-- 总览对比 -->
<div id="tab-overview" class="tab-panel">
  <div style="overflow-x:auto;border-radius:12px;border:1px solid var(--border);">
  <table style="width:100%;border-collapse:collapse;font-size:12px;min-width:720px;">
    <thead><tr style="background:linear-gradient(180deg,rgba(155,187,244,0.25),rgba(155,187,244,0.1));">
      <th style="padding:10px 8px;text-align:left;font-weight:600;color:var(--text);border-bottom:2px solid var(--accent);">院校</th>
      <th style="padding:10px 8px;text-align:center;font-weight:600;color:var(--text);border-bottom:2px solid var(--accent);">定位</th>
      <th style="padding:10px 8px;text-align:center;font-weight:600;color:var(--text);border-bottom:2px solid var(--accent);">QS排名</th>
      <th style="padding:10px 8px;text-align:center;font-weight:600;color:var(--text);border-bottom:2px solid var(--accent);">学费(万/年)</th>
      <th style="padding:10px 8px;text-align:center;font-weight:600;color:var(--text);border-bottom:2px solid var(--accent);">语言要求</th>
      <th style="padding:10px 8px;text-align:center;font-weight:600;color:var(--text);border-bottom:2px solid var(--accent);">匹配度</th>
      <th style="padding:10px 8px;text-align:center;font-weight:600;color:var(--text);border-bottom:2px solid var(--accent);">申请截止</th>
      <th style="padding:10px 8px;text-align:center;font-weight:600;color:var(--text);border-bottom:2px solid var(--accent);">状态</th>
    </tr></thead>
    <tbody id="overview-tbody"></tbody>
  </table></div>
  <div style="margin-top:12px;font-size:11px;color:var(--text2);display:flex;gap:16px;flex-wrap:wrap;">
    <span>🟢 预算内</span><span>🟡 略超预算</span><span>🔴 超预算</span>
    <span style="margin-left:auto;">数据来源：各大学官网 | 汇率基准：{{RATE_NOTE}}</span>
  </div>
</div>

<!-- 院校跟踪 -->
<div id="tab-track" class="tab-panel" style="display:none;">
  <div id="track-cards" style="display:flex;flex-direction:column;gap:12px;"></div>
</div>

<!-- 时间线 -->
<div id="tab-timeline" class="tab-panel" style="display:none;">
  <div id="timeline-container" style="position:relative;padding-left:28px;box-sizing:border-box;"></div>
</div>

<!-- 材料清单 -->
<div id="tab-materials" class="tab-panel" style="display:none;">
  <div style="background:var(--card);border-radius:12px;padding:16px;border:1px solid var(--border);margin-bottom:14px;">
    <div style="font-size:14px;font-weight:600;color:var(--text);margin-bottom:10px;">📦 通用申请材料（所有院校均需）</div>
    <div id="common-materials" style="display:flex;flex-direction:column;gap:6px;"></div>
  </div>
  <div id="school-materials" style="display:flex;flex-direction:column;gap:10px;"></div>
</div>

</div>
</div>

<script>
(function(){
try{
var schools = {{SCHOOLS_JSON}};
var statusList = ['未开始','准备中','已提交','审核中','已录取','已拒','已放弃'];
var statusColors = {'未开始':'#9CA3AF','准备中':'#60A5FA','已提交':'#FAAD14','审核中':'#A78BFA','已录取':'#52C41A','已拒':'#EA6668','已放弃':'#9CA3AF'};
var commonMats = {{COMMON_MATS_JSON}};
var schoolMats = {{SCHOOL_MATS_JSON}};

function renderOverview(){
  var tbody=document.getElementById('overview-tbody');var html='';
  schools.forEach(function(s){
    var tColor=s.tuitionStatus==='ok'?'var(--green)':s.tuitionStatus==='warn'?'var(--orange)':'var(--red)';
    var tIcon=s.tuitionStatus==='ok'?'🟢':s.tuitionStatus==='warn'?'🟡':'🔴';
    var sColor=statusColors[s.status]||'#9CA3AF';
    html+='<tr style="border-bottom:1px solid var(--border);">';
    html+='<td style="padding:9px 8px;"><div style="font-weight:600;color:var(--text);font-size:12.5px;">'+s.name+'</div><div style="font-size:10.5px;color:var(--text2);">'+s.en+' · '+s.program+'</div></td>';
    html+='<td style="padding:9px 8px;text-align:center;"><span style="display:inline-block;padding:2px 8px;border-radius:10px;font-size:10.5px;font-weight:600;color:#fff;background:'+s.tierColor+';">'+s.tier+'</span></td>';
    html+='<td style="padding:9px 8px;text-align:center;font-weight:600;color:var(--accent-dark);">'+s.qs+'</td>';
    html+='<td style="padding:9px 8px;text-align:center;color:'+tColor+';font-weight:600;">'+tIcon+' '+s.tuition+'</td>';
    html+='<td style="padding:9px 8px;text-align:center;font-size:11.5px;color:var(--text);">'+s.ielts+'</td>';
    html+='<td style="padding:9px 8px;text-align:center;"><div style="font-weight:700;color:var(--accent-dark);font-size:14px;">'+s.match+'</div><div style="width:50px;height:4px;background:#EEF0F3;border-radius:2px;margin:3px auto 0;overflow:hidden;"><div style="width:'+(s.match*10)+'%;height:100%;background:var(--accent);border-radius:2px;"></div></div></td>';
    html+='<td style="padding:9px 8px;text-align:center;font-size:11.5px;color:var(--text2);">'+s.deadlineText+'</td>';
    html+='<td style="padding:9px 8px;text-align:center;"><span style="display:inline-block;padding:3px 10px;border-radius:10px;font-size:11px;font-weight:600;color:#fff;background:'+sColor+';">'+s.status+'</span></td>';
    html+='</tr>';
  });tbody.innerHTML=html;
}

function renderTrack(){
  var c=document.getElementById('track-cards');var html='';
  schools.forEach(function(s){
    var sColor=statusColors[s.status]||'#9CA3AF';
    var tColor=s.tuitionStatus==='ok'?'var(--green)':s.tuitionStatus==='warn'?'var(--orange)':'var(--red)';
    html+='<div style="background:var(--card);border-radius:12px;padding:16px;border:1px solid var(--border);border-left:4px solid '+s.tierColor+';box-sizing:border-box;">';
    html+='<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:10px;">';
    html+='<div><span style="font-size:15px;font-weight:700;color:var(--text);">'+s.name+'</span> <span style="font-size:12px;color:var(--text2);">('+s.en+')</span><br/><span style="font-size:11.5px;color:var(--text2);">'+s.program+' · QS '+s.qs+' · '+s.region+'</span></div>';
    html+='<span style="display:inline-block;padding:4px 12px;border-radius:12px;font-size:12px;font-weight:600;color:#fff;background:'+sColor+';">'+s.status+'</span></div>';
    html+='<div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:10px;font-size:12px;">';
    html+='<div>💰 学费: <b style="color:'+tColor+';">'+s.tuition+'万/年</b></div>';
    html+='<div>📝 语言: <b>'+s.ielts+'</b></div>';
    html+='<div>🎯 匹配度: <b style="color:var(--accent-dark);">'+s.match+'/10</b></div>';
    html+='<div>⏰ 截止: <b>'+s.deadlineText+'</b></div></div>';
    html+='<div style="font-size:11.5px;color:var(--text2);margin-bottom:10px;padding:8px 10px;background:rgba(155,187,244,0.08);border-radius:6px;">💡 '+s.note+'</div>';
    html+='<div style="font-size:11px;color:var(--text2);margin-bottom:8px;">核心课程: '+s.courses.join('、')+'</div>';
    html+='<div style="display:flex;gap:4px;flex-wrap:wrap;margin-top:8px;">';
    html+='<span style="font-size:11px;color:var(--text2);margin-right:4px;align-self:center;">更新状态:</span>';
    statusList.forEach(function(st){var a=s.status===st;
    html+='<button data-school="'+s.id+'" data-status="'+st+'" class="status-btn" style="padding:5px 10px;border:1px solid '+(a?statusColors[st]:'#DDD')+';border-radius:6px;font-size:11px;cursor:pointer;min-height:32px;background:'+(a?statusColors[st]:'#fff')+';color:'+(a?'#fff':'#666')+';font-weight:'+(a?'600':'400')+');">'+st+'</button>';});
    html+='</div></div>';
  });c.innerHTML=html;
  c.querySelectorAll('.status-btn').forEach(function(b){b.addEventListener('click',function(){
    var sid=b.getAttribute('data-school'),st=b.getAttribute('data-status');
    schools.forEach(function(s){if(s.id===sid)s.status=st;});
    renderTrack();renderOverview();updateStats();
  });});
}

function renderTimeline(){
  var c=document.getElementById('timeline-container');
  var sorted=schools.slice().sort(function(a,b){return new Date(a.deadline)-new Date(b.deadline);});
  var html='<div style="position:absolute;left:-22px;top:0;bottom:0;width:2px;background:linear-gradient(180deg,#60A5FA,#9B7BD4,#FAAD14,#52C41A);"></div>';
  var phases=[{title:'准备阶段',date:'材料准备期',desc:'撰写PS/CV、联系推荐人、确认语言成绩、准备成绩单在读证明',color:'#60A5FA'}];
  phases.forEach(function(p){
    html+='<div style="position:relative;margin-bottom:18px;"><div style="position:absolute;left:-28px;top:2px;width:14px;height:14px;border-radius:50%;background:'+p.color+';border:3px solid #fff;box-shadow:0 0 0 2px '+p.color+';"></div>';
    html+='<div style="font-size:13px;font-weight:600;color:var(--text);">'+p.title+' <span style="font-size:11px;color:var(--text2);font-weight:400;">('+p.date+')</span></div>';
    html+='<div style="font-size:12px;color:var(--text2);margin-top:3px;">'+p.desc+'</div></div>';
  });
  sorted.forEach(function(s){
    html+='<div style="position:relative;margin-bottom:16px;"><div style="position:absolute;left:-28px;top:2px;width:14px;height:14px;border-radius:50%;background:'+s.tierColor+';border:3px solid #fff;box-shadow:0 0 0 2px '+s.tierColor+';"></div>';
    html+='<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;"><span style="font-size:13px;font-weight:600;color:var(--text);">'+s.name+'</span><span style="font-size:11px;padding:2px 8px;border-radius:8px;background:'+(statusColors[s.status]||'#9CA3AF')+';color:#fff;font-weight:600;">'+s.status+'</span></div>';
    html+='<div style="font-size:12px;color:var(--text2);margin-top:3px;">⏰ 申请截止: <b style="color:var(--text);">'+s.deadlineText+'</b> · 学费 '+s.tuition+'万/年 · 匹配度 '+s.match+'</div></div>';
  });
  c.innerHTML=html;
}

function renderMaterials(){
  var cm=document.getElementById('common-materials');var html='';
  commonMats.forEach(function(m,i){
    html+='<label style="display:flex;align-items:center;gap:8px;cursor:pointer;font-size:12.5px;padding:4px 0;"><input type="checkbox" data-mat="'+i+'" '+(m.done?'checked':'')+' style="width:16px;height:16px;cursor:pointer;"/><span style="'+(m.done?'text-decoration:line-through;color:#9CA3AF;':'color:var(--text);')+'">'+m.name+'</span></label>';
  });cm.innerHTML=html;
  cm.querySelectorAll('input[type=checkbox]').forEach(function(cb){cb.addEventListener('change',function(){
    var i=parseInt(cb.getAttribute('data-mat'));commonMats[i].done=cb.checked;renderMaterials();
  });});
  var sm=document.getElementById('school-materials');var h2='';
  schools.forEach(function(s){
    var ex=schoolMats[s.id]?schoolMats[s.id]:[];
    h2+='<div style="background:var(--card);border-radius:10px;padding:12px 14px;border:1px solid var(--border);border-left:3px solid '+s.tierColor+');">';
    h2+='<div style="font-size:13px;font-weight:600;color:var(--text);margin-bottom:6px;">'+s.name+' ('+s.en+')</div>';
    h2+='<div style="font-size:11.5px;color:var(--text2);">通用材料 + 以下特殊注意事项:</div>';
    ex.forEach(function(e){h2+='<div style="font-size:11.5px;color:var(--text);margin-top:4px;padding-left:12px;position:relative;"><span style="position:absolute;left:0;color:var(--accent-dark);">▸</span>'+e+'</div>';});
    h2+='</div>';
  });sm.innerHTML=h2;
}

function updateStats(){
  var sub=schools.filter(function(s){return ['已提交','审核中','已录取'].indexOf(s.status)>=0;}).length;
  var off=schools.filter(function(s){return s.status==='已录取';}).length;
  var prog=0;
  schools.forEach(function(s){
    if(s.status==='准备中')prog+=20;else if(s.status==='已提交')prog+=50;else if(s.status==='审核中')prog+=70;else if(s.status==='已录取')prog+=100;
  });prog=Math.round(prog/schools.length);
  document.getElementById('stat-submitted').textContent=sub;
  document.getElementById('stat-offer').textContent=off;
  document.getElementById('stat-progress').textContent=prog+'%';
}

var tabs=document.querySelectorAll('.tab-btn'),panels=document.querySelectorAll('.tab-panel');
tabs.forEach(function(t){t.addEventListener('click',function(){
  var tg=t.getAttribute('data-tab');
  tabs.forEach(function(x){x.style.background='#EEF0F3';x.style.color='var(--text2)';x.style.fontWeight='500';});
  t.style.background='var(--accent)';t.style.color='#fff';t.style.fontWeight='600';
  panels.forEach(function(p){p.style.display='none';});
  document.getElementById('tab-'+tg).style.display='block';
});});

renderOverview();renderTrack();renderTimeline();renderMaterials();updateStats();
}catch(e){console.error(e);}
})();
</script>
</div>
</body>
</html>'''


def load_schools(input_path):
    """加载院校JSON数据（支持BOM）"""
    for enc in ('utf-8-sig', 'utf-8'):
        try:
            with open(input_path, 'r', encoding=enc) as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
        return json.load(f)


def generate_html(data, output_path):
    """生成HTML跟踪台账"""
    schools = data.get('schools', [])
    applicant = data.get('applicant', {})
    common_mats = data.get('common_materials', [])
    school_mats = data.get('school_materials', {})
    rate_note = data.get('rate_note', '实时汇率')

    # 为每所学校设置默认状态
    for s in schools:
        if 'status' not in s:
            s['status'] = '未开始'
        if 'tuitionStatus' not in s:
            s['tuitionStatus'] = 'ok'
        if 'courses' not in s:
            s['courses'] = []
        if 'note' not in s:
            s['note'] = ''

    html = HTML_TEMPLATE
    html = html.replace('{{APPLICANT_NAME}}', applicant.get('name', '申请人'))
    html = html.replace('{{PROGRAM}}', applicant.get('program', '硕士'))
    html = html.replace('{{APPLICANT_BG}}', applicant.get('bg', ''))
    html = html.replace('{{TARGET_YEAR}}', applicant.get('target_year', '2026'))
    html = html.replace('{{TOTAL_SCHOOLS}}', str(len(schools)))
    html = html.replace('{{RATE_NOTE}}', rate_note)
    html = html.replace('{{SCHOOLS_JSON}}', json.dumps(schools, ensure_ascii=False))
    html = html.replace('{{COMMON_MATS_JSON}}', json.dumps(common_mats, ensure_ascii=False))
    html = html.replace('{{SCHOOL_MATS_JSON}}', json.dumps(school_mats, ensure_ascii=False))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path


def main():
    parser = argparse.ArgumentParser(description='留学申请可视化跟踪台账生成器')
    parser.add_argument('--input', '-i', required=True, help='院校数据JSON文件路径')
    parser.add_argument('--output', '-o', default='tracker.html', help='输出HTML文件路径')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f'错误：输入文件不存在: {args.input}', file=sys.stderr)
        sys.exit(1)

    data = load_schools(args.input)
    output = generate_html(data, args.output)
    print(f'✅ 跟踪台账已生成: {output}')
    print(f'   院校数量: {len(data.get("schools", []))}')


if __name__ == '__main__':
    main()
