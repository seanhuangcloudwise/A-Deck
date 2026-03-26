"""Application Architecture loaders — one function per diagram type."""

from common import (
    render_layered_stack,
    render_tree,
    render_node_graph,
    render_bounded_context,
    render_flow_stages,
    render_event_bus,
    render_matrix_table,
    render_swimlane,
    render_capability_grid,
)

# ─── Default data per AA diagram ──────────────────────────────────────────────

_AA01_LAYERS = [
    {"label": "渠道层",   "items": ["Web Portal",     "Mobile App",      "Open API",      "Partner Portal"]},
    {"label": "前端应用", "items": ["CRM系统",         "订单管理",        "库存管理",       "客服系统"]},
    {"label": "中台服务", "items": ["用户中心",         "支付中心",        "消息中心",       "搜索推荐"]},
    {"label": "后台系统", "items": ["ERP",              "财务系统",        "HR系统",         "OA系统"]},
    {"label": "数据基础", "items": ["数据湖",           "数据仓库",        "实时流处理",     "BI平台"]},
]

_AA02_TREE = {
    "root": "业务系统",
    "branches": [
        {"label": "用户域", "children": ["注册登录", "用户画像", "权限管理"]},
        {"label": "交易域", "children": ["订单中心", "支付网关", "退款服务"]},
        {"label": "商品域", "children": ["商品目录", "库存管理", "价格引擎"]},
        {"label": "运营域", "children": ["活动系统", "推荐引擎", "通知服务"]},
    ],
}

_AA03_GRAPH = {
    "nodes": [
        {"id": "GW",   "label": "API Gateway",    "x": 0.45, "y": 0.08},
        {"id": "US",   "label": "User Service",   "x": 0.08, "y": 0.35},
        {"id": "OS",   "label": "Order Service",  "x": 0.45, "y": 0.35},
        {"id": "PS",   "label": "Product Service","x": 0.82, "y": 0.35},
        {"id": "PAY",  "label": "Payment",        "x": 0.25, "y": 0.72},
        {"id": "MSG",  "label": "Message Bus",    "x": 0.65, "y": 0.72},
        {"id": "DB",   "label": "Database",       "x": 0.08, "y": 0.72},
    ],
    "edges": [
        {"from": "GW",  "to": "US",  "label": "REST"},
        {"from": "GW",  "to": "OS",  "label": "REST"},
        {"from": "GW",  "to": "PS",  "label": "REST"},
        {"from": "OS",  "to": "PAY", "label": "API"},
        {"from": "OS",  "to": "MSG", "label": "Event"},
        {"from": "US",  "to": "DB",  "label": "SQL"},
    ],
}

_AA04_CONTEXTS = {
    "contexts": [
        {"name": "Order Context",     "items": ["Order","OrderLine","Cart"],         "color": 0},
        {"name": "Inventory Context", "items": ["Product","SKU","StockLevel"],       "color": 1},
        {"name": "User Context",      "items": ["Customer","Account","Auth"],        "color": 2},
        {"name": "Payment Context",   "items": ["Invoice","Transaction","Refund"],   "color": 3},
        {"name": "Notification",      "items": ["Email","SMS","Push"],               "color": 4},
        {"name": "Reporting",         "items": ["Dashboard","Report","Export"],      "color": 5},
    ],
    "relations": [
        {"from": "Order Context",     "to": "Inventory Context", "type": "Customer-Supplier"},
        {"from": "Order Context",     "to": "Payment Context",   "type": "Conformist"},
        {"from": "Order Context",     "to": "User Context",      "type": "Partnership"},
    ],
}

_AA05_STAGES = [
    {"title": "Client App",    "items": ["Send HTTP Request", "Token Attach"]},
    {"title": "API Gateway",   "items": ["Auth / Rate Limit",  "Route & Load Balance"]},
    {"title": "Svc A",         "items": ["Validate Request",   "Fetch Upstream"]},
    {"title": "Svc B",         "items": ["Process Logic",      "Write to DB"]},
    {"title": "Response",      "items": ["Build Response",     "Return 200 OK"]},
]

_AA06_GRAPH = {
    "nodes": [
        {"id": "GW",  "label": "API Gateway",    "x": 0.45, "y": 0.07},
        {"id": "A",   "label": "Service A",      "x": 0.08, "y": 0.35},
        {"id": "B",   "label": "Service B",      "x": 0.45, "y": 0.35},
        {"id": "C",   "label": "Service C",      "x": 0.82, "y": 0.35},
        {"id": "D",   "label": "Service D",      "x": 0.25, "y": 0.70},
        {"id": "E",   "label": "Ext API",        "x": 0.82, "y": 0.70},
    ],
    "edges": [
        {"from": "GW", "to": "A",  "label": "v2"},
        {"from": "GW", "to": "B",  "label": "v1"},
        {"from": "A",  "to": "D",  "label": "dep"},
        {"from": "B",  "to": "C",  "label": "async"},
        {"from": "C",  "to": "E",  "label": "webhook"},
    ],
}

_AA07_BUS = {
    "producers": ["Order Service", "Inventory Svc", "User Service", "Payment Svc"],
    "bus_title":  "Kafka Event Bus",
    "topics":     ["order.created", "inventory.updated", "user.registered", "payment.done"],
    "consumers":  ["Notification", "Analytics", "Audit Log", "Search Index"],
}

_AA08_LAYERS = [
    {"label": "接入层",   "items": ["Web BFF",          "Mobile BFF",      "API Gateway"]},
    {"label": "用户域",   "items": ["Auth Service",      "Profile Service", "RBAC"]},
    {"label": "交易域",   "items": ["Order Service",     "Payment Service", "Cart Service"]},
    {"label": "商品域",   "items": ["Catalog Service",   "Inventory Svc",   "Pricing Svc"]},
    {"label": "基础域",   "items": ["Notification Svc",  "File Storage",    "Config Center"]},
]

_AA09_MATRIX = {
    "row_headers": ["ERP System",    "CRM System",  "OA System",   "BI Platform",  "数据中台"],
    "col_headers": ["客户管理", "财务管理", "人力资源", "数据分析",  "流程自动化"],
    "cells": [
        ["·",  "R",  "·",  "C",  "·"],
        ["R",  "·",  "·",  "C",  "·"],
        ["·",  "·",  "R",  "·",  "C"],
        ["C",  "C",  "·",  "R",  "·"],
        ["A",  "A",  "A",  "A",  "A"],
    ],
}

_AA10_LANES = [
    {"actor": "Client",   "steps": ["Send Request",  "Receive Response", "Render UI"]},
    {"actor": "Gateway",  "steps": ["Authenticate",  "Route",            ""]},
    {"actor": "Service A","steps": ["Validate",      "Call Service B",   ""]},
    {"actor": "Service B","steps": ["",              "Process",          "Return Data"]},
]

_AA11_ROWS = [
    {"label": "平台服务层", "items": ["认证中心",  "消息平台", "文件存储", "配置中心"]},
    {"label": "应用能力层", "items": ["用户管理",  "订单引擎", "支付平台", "通知服务"]},
    {"label": "数据能力层", "items": ["数据采集",  "数据治理", "数据服务", "数据分析"]},
    {"label": "AI能力层",   "items": ["NLP引擎",    "推荐算法", "图像识别", "预测模型"]},
]


# ─── Individual load functions ─────────────────────────────────────────────────

def load_aa_01_application_landscape(ctx, data):
    return render_layered_stack(ctx, data, "AA", defaults=_AA01_LAYERS)


def load_aa_02_component_diagram(ctx, data):
    return render_tree(ctx, data, "AA", defaults=_AA02_TREE)


def load_aa_03_integration_map(ctx, data):
    return render_node_graph(ctx, data, "AA", defaults=_AA03_GRAPH)


def load_aa_04_bounded_context_map(ctx, data):
    return render_bounded_context(ctx, data, "AA", defaults=_AA04_CONTEXTS)


def load_aa_05_service_interaction(ctx, data):
    return render_flow_stages(ctx, data, "AA", defaults=_AA05_STAGES)


def load_aa_06_api_dependency_graph(ctx, data):
    return render_node_graph(ctx, data, "AA", defaults=_AA06_GRAPH)


def load_aa_07_event_driven_architecture(ctx, data):
    return render_event_bus(ctx, data, "AA", defaults=_AA07_BUS)


def load_aa_08_microservice_decomposition(ctx, data):
    return render_layered_stack(ctx, data, "AA", defaults=_AA08_LAYERS)


def load_aa_09_app_capability_mapping(ctx, data):
    return render_matrix_table(ctx, data, "AA", defaults=_AA09_MATRIX)


def load_aa_10_application_sequence_flow(ctx, data):
    return render_swimlane(ctx, data, "AA", defaults=_AA10_LANES)


def load_aa_11_product_capability_map(ctx, data):
    return render_capability_grid(ctx, data, "AA", defaults=_AA11_ROWS)
