"""Business Architecture loaders — one function per diagram type."""

from common import (
    render_capability_grid,
    render_flow_stages,
    render_swimlane,
    render_actor_grid,
    render_tree,
    render_matrix_table,
    render_two_column,
    render_journey_stages,
    render_kpi_cascade,
)

# ─── Default data per BA diagram ──────────────────────────────────────────────

_BA01_ROWS = [
    {"label": "客户管理",   "items": ["客户获取", "客户服务", "客户留存", "客户分析"]},
    {"label": "产品管理",   "items": ["产品研发", "产品运营", "定价策略", "市场发布"]},
    {"label": "运营支撑",   "items": ["财务管理", "人力资源", "法务合规", "采购管理"]},
    {"label": "数字底座",   "items": ["数据平台", "AI能力",   "安全合规", "技术架构"]},
]

_BA02_STAGES = [
    {"title": "需求识别", "items": ["市场调研", "客户访谈", "竞品分析"]},
    {"title": "产品开发", "items": ["需求分析", "原型设计", "研发实现"]},
    {"title": "市场推广", "items": ["渠道策略", "内容营销", "活动推广"]},
    {"title": "销售转化", "items": ["线索管理", "商机跟进", "合同签署"]},
    {"title": "客户成功", "items": ["交付实施", "续费管理", "口碑运营"]},
]

_BA03_PROCESS = {
    "lanes": ["业务方", "产品经理", "架构师", "系统"],
    "columns": 8,
    "nodes": [
        {"id": "start",  "type": "event",    "lane": "业务方",   "x_in": 0.02, "start": True},
        {"id": "n1",     "type": "step",     "lane": "业务方",   "col": 0, "name": "提交需求", "system": "Portal",   "duration": "<=2h"},
        {"id": "n2",     "type": "step",     "lane": "产品经理", "col": 1, "name": "需求分级", "system": "Jira",     "duration": "<=1h"},
        {"id": "n3",     "type": "step",     "lane": "产品经理", "col": 2, "name": "业务澄清", "system": "Workshop", "duration": "<=2h"},
        {"id": "d1",     "type": "decision", "lane": "产品经理", "col": 3, "text": "范围清晰?", "w_in": 0.56, "h_in": 0.52},
        {"id": "n4",     "type": "step",     "lane": "架构师",   "col": 4, "name": "约束评估", "system": "EA Repo",  "duration": "<=2h"},
        {"id": "n5",     "type": "step",     "lane": "系统",     "col": 5, "name": "建档",     "system": "Tracker",  "duration": "<=30m"},
        {"id": "n6",     "type": "step",     "lane": "产品经理", "col": 6, "name": "范围冻结", "system": "Workflow", "duration": "<=30m", "critical": True},
        {"id": "n7",     "type": "step",     "lane": "架构师",   "col": 2, "name": "补充材料", "system": "Manual",   "duration": "<=4h", "manual": True},
        {"id": "end",    "type": "event",    "lane": "产品经理", "x_in": 8.05, "end": True},
    ],
    "links": [
        {"from": "n1", "to": "n2", "label": "handoff"},
        {"from": "n2", "to": "n3"},
        {"from": "n3", "to": "d1"},
        {"from": "d1", "to": "n4", "label": "Yes"},
        {"from": "n4", "to": "n5"},
        {"from": "n5", "to": "n6", "label": "sync"},
        {"from": "n6", "to": "end"},
        {"from": "d1", "to": "n7", "label": "No", "dashed": True, "start_side": "bottom", "end_side": "top"},
    ],
    "note": "BA-03 Detailed SOP | branch + exception + system annotation",
}

_BA04_ACTOR = {
    "hub": "客户服务中心",
    "spokes": [
        {"label": "销售团队",   "interaction": "提供线索与商机"},
        {"label": "产品团队",   "interaction": "提供产品信息"},
        {"label": "交付团队",   "interaction": "执行实施服务"},
        {"label": "技术支持",   "interaction": "解决技术问题"},
        {"label": "财务团队",   "interaction": "账单与合同"},
        {"label": "客户",       "interaction": "提交需求与反馈"},
    ],
}

_BA05_TREE = {
    "root": "业务服务域",
    "branches": [
        {"label": "前台服务",   "children": ["客户门户", "移动App",  "在线商城"]},
        {"label": "中台服务",   "children": ["用户中心", "订单中心", "支付中心"]},
        {"label": "后台服务",   "children": ["财务系统", "人事系统", "仓储管理"]},
        {"label": "基础服务",   "children": ["消息推送", "文件存储", "日志审计"]},
    ],
}

_BA06_MATRIX = {
    "row_headers": ["战略规划", "需求管理", "架构设计", "研发交付", "运营管理"],
    "col_headers": ["产品经理", "架构师",   "开发团队", "测试团队",  "运营团队"],
    "cells": [
        ["R", "A", "C", "I", "I"],
        ["A", "C", "R", "C", "I"],
        ["C", "R", "A", "C", "I"],
        ["I", "C", "R", "A", "C"],
        ["I", "I", "C", "R", "A"],
    ],
}

_BA07_COMPARE = {
    "left_title":  "As-Is 现状",
    "right_title": "To-Be 目标",
    "left_items":  ["手工报表流程", "分散IT系统", "数据孤岛", "响应周期长"],
    "right_items": ["自动化工作流", "统一业务平台", "数据中台", "实时决策支持"],
    "delta":       "Δ 数字化转型",
}

_BA08_JOURNEY = [
    {"title": "认知",   "touchpoints": ["广告投放",  "口碑推荐"],  "emotion": "+", "pain": "信息难获取"},
    {"title": "考虑",   "touchpoints": ["产品演示",  "竞品对比"],  "emotion": "~", "pain": "定价不透明"},
    {"title": "决策",   "touchpoints": ["方案评审",  "合同谈判"],  "emotion": "+", "pain": "审批周期长"},
    {"title": "上线",   "touchpoints": ["培训交付",  "系统配置"],  "emotion": "-", "pain": "接入复杂"},
    {"title": "推荐",   "touchpoints": ["续费评审",  "转介绍"],    "emotion": "+", "pain": ""},
]

_BA09_KPI = [
    {"label": "客户满意度", "owner": "CEO", "kpis": ["NPS > 50", "CSAT > 90%", "客户留存 > 85%"]},
    {"label": "运营效率",   "owner": "COO", "kpis": ["自动化率 60%", "MTTR < 2h", "成本↓15%"]},
    {"label": "营收增长",   "owner": "CRO", "kpis": ["YoY +25%",  "新客占比 30%", "ARR $10M"]},
]

_BA10_RACI = {
    "row_headers": ["战略规划", "架构评审", "研发交付", "测试验收", "运营管理", "安全合规"],
    "col_headers": ["CTO", "架构师", "开发团队", "测试团队", "运维团队"],
    "cells": [
        ["A", "R", "C", "I", "I"],
        ["A", "R", "C", "C", "I"],
        ["I", "C", "R", "A", "I"],
        ["I", "C", "C", "R", "I"],
        ["I", "I", "C", "R", "A"],
        ["A", "R", "I", "I", "C"],
    ],
}


# ─── Individual load functions ─────────────────────────────────────────────────

def load_ba_01_capability_map(ctx, data):
    return render_capability_grid(ctx, data, "BA", defaults=_BA01_ROWS)


def load_ba_02_value_stream(ctx, data):
    return render_flow_stages(ctx, data, "BA", defaults=_BA02_STAGES)


def load_ba_03_business_process(ctx, data):
    return render_swimlane(ctx, data, "BA", defaults=_BA03_PROCESS)


def load_ba_04_actor_interaction(ctx, data):
    return render_actor_grid(ctx, data, "BA", defaults=_BA04_ACTOR)


def load_ba_05_service_decomposition(ctx, data):
    return render_tree(ctx, data, "BA", defaults=_BA05_TREE)


def load_ba_06_function_capability_mapping(ctx, data):
    return render_matrix_table(ctx, data, "BA", defaults=_BA06_MATRIX)


def load_ba_07_as_is_to_be(ctx, data):
    return render_two_column(ctx, data, "BA", defaults=_BA07_COMPARE)


def load_ba_08_scenario_journey(ctx, data):
    return render_journey_stages(ctx, data, "BA", defaults=_BA08_JOURNEY)


def load_ba_09_kpi_alignment(ctx, data):
    return render_kpi_cascade(ctx, data, "BA", defaults=_BA09_KPI)


def load_ba_10_raci_matrix(ctx, data):
    return render_matrix_table(ctx, data, "BA", defaults=_BA10_RACI)
