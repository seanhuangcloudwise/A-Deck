"""Data Architecture loaders — one function per diagram type."""

from common import (
    render_er_diagram,
    render_node_graph,
    render_bounded_context,
    render_layered_stack,
    render_flow_stages,
    render_data_lineage,
    render_tree,
)

# ─── Default data per DA diagram ──────────────────────────────────────────────

_DA01_ER = {
    "entities": [
        {"name": "客户",     "attrs": ["客户ID PK", "名称", "联系方式"],        "x": 0.06, "y": 0.12},
        {"name": "订单",     "attrs": ["订单ID PK", "日期", "金额", "状态"],    "x": 0.06, "y": 0.60},
        {"name": "产品",     "attrs": ["产品ID PK", "名称", "价格", "类别"],    "x": 0.56, "y": 0.12},
        {"name": "订单行",   "attrs": ["订单ID FK", "产品ID FK", "数量"],       "x": 0.56, "y": 0.60},
    ],
    "relations": [
        {"from": "客户",   "to": "订单",   "label": "1..* 下单"},
        {"from": "订单",   "to": "订单行", "label": "1..* 包含"},
        {"from": "产品",   "to": "订单行", "label": "1..* 出现在"},
    ],
}

_DA02_ER = {
    "entities": [
        {"name": "Employee",    "attrs": ["emp_id PK","name","dept_id FK","role"],  "x": 0.06, "y": 0.10},
        {"name": "Department",  "attrs": ["dept_id PK","name","manager_id FK"],     "x": 0.06, "y": 0.62},
        {"name": "Project",     "attrs": ["proj_id PK","title","budget","status"],  "x": 0.56, "y": 0.10},
        {"name": "Assignment",  "attrs": ["emp_id FK","proj_id FK","role","hours"], "x": 0.56, "y": 0.62},
    ],
    "relations": [
        {"from": "Department", "to": "Employee",   "label": "1..* belongs-to"},
        {"from": "Employee",   "to": "Assignment", "label": "1..* has"},
        {"from": "Project",    "to": "Assignment", "label": "1..* assigned-in"},
    ],
}

_DA03_GRAPH = {
    "nodes": [
        {"id": "CRM",  "label": "CRM(外部)",    "x": 0.06, "y": 0.15},
        {"id": "ERP",  "label": "ERP(外部)",    "x": 0.06, "y": 0.55},
        {"id": "ETL",  "label": "ETL 处理",     "x": 0.42, "y": 0.35},
        {"id": "DW",   "label": "数据仓库",      "x": 0.78, "y": 0.15},
        {"id": "RPTS", "label": "报表服务",      "x": 0.78, "y": 0.55},
    ],
    "edges": [
        {"from": "CRM",  "to": "ETL",  "label": "批量"},
        {"from": "ERP",  "to": "ETL",  "label": "增量"},
        {"from": "ETL",  "to": "DW",   "label": "加载"},
        {"from": "DW",   "to": "RPTS", "label": "查询"},
    ],
}

_DA04_CONTEXTS = {
    "contexts": [
        {"name": "客户数据域",   "items": ["客户档案", "联系方式", "分级标签"],   "color": 0},
        {"name": "交易数据域",   "items": ["订单记录", "支付记录", "退款记录"],   "color": 1},
        {"name": "产品数据域",   "items": ["产品目录", "库存数据", "价格数据"],   "color": 2},
        {"name": "运营数据域",   "items": ["行为日志", "活动数据", "渠道数据"],   "color": 3},
    ],
    "relations": [
        {"from": "交易数据域", "to": "客户数据域", "type": "关联"},
        {"from": "交易数据域", "to": "产品数据域", "type": "引用"},
        {"from": "运营数据域", "to": "客户数据域", "type": "补充"},
    ],
}

_DA05_LAYERS = [
    {"label": "治理策略层", "items": ["数据安全策略", "隐私保护",    "合规要求",    "数据分级"]},
    {"label": "标准规范层", "items": ["数据标准",     "命名规范",    "质量规则",    "元数据标准"]},
    {"label": "流程管控层", "items": ["数据接入流程", "变更管理",    "质量检核",    "问题处理"]},
    {"label": "工具平台层", "items": ["数据目录",     "血缘系统",    "质量平台",    "监控告警"]},
    {"label": "组织职责层", "items": ["数据Owner",    "数据Steward", "数据委员会",  "审计团队"]},
]

_DA06_STAGES = [
    {"title": "采集创建", "items": ["数据录入",  "系统生成",  "接口接入"]},
    {"title": "清洗验证", "items": ["格式校验",  "去重合并",  "异常标注"]},
    {"title": "加工丰富", "items": ["特征提取",  "关联融合",  "标签打标"]},
    {"title": "分发共享", "items": ["数据服务",  "订阅推送",  "接口开放"]},
    {"title": "归档下线", "items": ["冷热分层",  "合规归档",  "数据销毁"]},
]

_DA07_LINEAGE = {
    "sources":    ["CRM系统", "ERP系统", "埋点日志", "IoT数据"],
    "transforms": ["数据清洗", "字段映射", "聚合计算", "特征工程"],
    "targets":    ["数据仓库", "分析平台", "ML特征库", "数据报表"],
}

_DA08_TREE = {
    "root": "企业数据目录",
    "branches": [
        {"label": "客户数据",   "children": ["客户基本信息", "联系记录", "历史订单"]},
        {"label": "交易数据",   "children": ["订单明细", "支付流水", "物流记录"]},
        {"label": "产品数据",   "children": ["产品信息", "库存记录", "定价历史"]},
        {"label": "运营数据",   "children": ["营销活动", "用户行为", "渠道数据"]},
    ],
}


# ─── Individual load functions ─────────────────────────────────────────────────

def load_da_01_conceptual_data_model(ctx, data):
    return render_er_diagram(ctx, data, "DA", defaults=_DA01_ER)


def load_da_02_logical_data_model(ctx, data):
    return render_er_diagram(ctx, data, "DA", defaults=_DA02_ER)


def load_da_03_data_flow_diagram(ctx, data):
    return render_node_graph(ctx, data, "DA", defaults=_DA03_GRAPH)


def load_da_04_data_domain_map(ctx, data):
    return render_bounded_context(ctx, data, "DA", defaults=_DA04_CONTEXTS)


def load_da_05_data_governance_framework(ctx, data):
    return render_layered_stack(ctx, data, "DA", defaults=_DA05_LAYERS)


def load_da_06_master_data_lifecycle(ctx, data):
    return render_flow_stages(ctx, data, "DA", defaults=_DA06_STAGES)


def load_da_07_data_lineage(ctx, data):
    return render_data_lineage(ctx, data, "DA", defaults=_DA07_LINEAGE)


def load_da_08_data_catalog_structure(ctx, data):
    return render_tree(ctx, data, "DA", defaults=_DA08_TREE)
