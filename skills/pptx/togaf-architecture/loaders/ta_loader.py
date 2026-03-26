"""Technology Architecture loaders — one function per diagram type."""

from common import (
    render_node_graph,
    render_layered_stack,
    render_two_column,
    render_bounded_context,
    render_capability_grid,
)

# ─── Default data per TA diagram ──────────────────────────────────────────────

_TA01_GRAPH = {
    "nodes": [
        {"id": "LB",   "label": "Load Balancer",   "x": 0.45, "y": 0.06},
        {"id": "WEB1", "label": "Web Node 1",       "x": 0.20, "y": 0.30},
        {"id": "WEB2", "label": "Web Node 2",       "x": 0.70, "y": 0.30},
        {"id": "APP1", "label": "App Server 1",     "x": 0.20, "y": 0.60},
        {"id": "APP2", "label": "App Server 2",     "x": 0.70, "y": 0.60},
        {"id": "DB",   "label": "DB Primary",       "x": 0.33, "y": 0.88},
        {"id": "DBS",  "label": "DB Replica",       "x": 0.60, "y": 0.88},
    ],
    "edges": [
        {"from": "LB",   "to": "WEB1", "label": "HTTP"},
        {"from": "LB",   "to": "WEB2", "label": "HTTP"},
        {"from": "WEB1", "to": "APP1", "label": "RPC"},
        {"from": "WEB2", "to": "APP2", "label": "RPC"},
        {"from": "APP1", "to": "DB",   "label": "SQL"},
        {"from": "APP2", "to": "DB",   "label": "SQL"},
        {"from": "DB",   "to": "DBS",  "label": "Repl"},
    ],
}

_TA02_LAYERS = [
    {"label": "用户接入",     "items": ["Web Browser",   "Mobile Client",  "Third-party API"]},
    {"label": "接入网关",     "items": ["CDN",            "WAF",           "Load Balancer"]},
    {"label": "应用服务",     "items": ["Web Servers",    "App Servers",   "API Servers"]},
    {"label": "容器平台",     "items": ["Kubernetes",     "Docker",        "Service Mesh"]},
    {"label": "存储 & 数据",  "items": ["PostgreSQL",     "Redis",         "Object Storage"]},
    {"label": "基础设施",     "items": ["物理/虚拟机",    "网络设备",       "监控系统"]},
]

_TA03_LAYERS = [
    {"label": "外网区",     "items": ["Internet",       "CDN边缘节点",   "外部合作伙伴"]},
    {"label": "DMZ",        "items": ["WAF",            "负载均衡",      "反向代理"]},
    {"label": "业务区",     "items": ["Web应用层",       "API服务层",     "业务逻辑层"]},
    {"label": "数据区",     "items": ["关系型数据库",    "缓存集群",      "搜索引擎"]},
    {"label": "管理区",     "items": ["跳板机",         "堡垒机",        "审计日志"]},
]

_TA04_LAYERS = [
    {"label": "SaaS",       "items": ["ERP (SAP)",      "CRM (Salesforce)", "协同(钉钉/飞书)"]},
    {"label": "PaaS",       "items": ["容器平台(K8s)",   "数据库PaaS",       "消息队列MQ"]},
    {"label": "基础IaaS",   "items": ["计算(ECS)",       "存储(OSS/块存储)", "网络(VPC/SLB)"]},
    {"label": "安全能力",   "items": ["IAM身份认证",     "加密KMS",          "安全审计"]},
    {"label": "自建数据中心","items": ["私有云(VMware)",  "HPC集群",          "裸金属服务器"]},
]

_TA05_CONTEXTS = {
    "contexts": [
        {"name": "Ingress 层",   "items": ["Ingress Controller","TLS终止","域名路由"],  "color": 0},
        {"name": "Service Mesh", "items": ["Istio Sidecar","mTLS","流量策略"],          "color": 1},
        {"name": "App Pods",     "items": ["Deployment","ReplicaSet","HPA"],            "color": 2},
        {"name": "DB StatefulSet","items":["MySQL Cluster","Redis Sentinel","PVC"],     "color": 3},
        {"name": "监控 & 日志",  "items": ["Prometheus","Grafana","EFK Stack"],         "color": 4},
        {"name": "CI/CD",        "items": ["Jenkins","Harbor镜像仓","ArgoCD"],          "color": 5},
    ],
    "relations": [
        {"from": "Ingress 层",    "to": "Service Mesh", "type": "流量入口"},
        {"from": "Service Mesh",  "to": "App Pods",     "type": "服务治理"},
        {"from": "App Pods",      "to": "DB StatefulSet","type": "数据访问"},
    ],
}

_TA06_LAYERS = [
    {"label": "安全策略层", "items": ["安全标准",  "等保合规",   "风险评估",   "审计要求"]},
    {"label": "边界防护层", "items": ["防火墙",    "WAF",        "IDS/IPS",    "DDoS防护"]},
    {"label": "访问控制层", "items": ["IAM",       "MFA多因素",  "RBAC",       "零信任"]},
    {"label": "数据安全层", "items": ["数据加密",  "脱敏处理",   "DLP防泄漏",  "密钥管理"]},
    {"label": "监控响应层", "items": ["SIEM",      "SOC",        "威胁情报",   "应急响应"]},
]

_TA07_LAYERS = [
    {"label": "数据采集",   "items": ["日志采集(Fluentd)", "指标采集(Prometheus)", "Trace(Jaeger)"]},
    {"label": "数据传输",   "items": ["Kafka消息队列",     "数据总线",             "流处理引擎"]},
    {"label": "存储层",     "items": ["Elasticsearch",     "InfluxDB",             "对象存储"]},
    {"label": "可视化",     "items": ["Grafana Dashboard", "Kibana",               "自定义大屏"]},
    {"label": "告警响应",   "items": ["AlertManager",      "PagerDuty",            "On-call机制"]},
]

_TA08_DR = {
    "left_title":  "主站点 (Primary)",
    "right_title": "容灾站点 (DR)",
    "left_items":  ["全量活跃流量", "实时读写数据库", "完整应用栈", "RTO: 生产"],
    "right_items": ["热备/温备实例", "异步数据同步", "镜像应用环境", "RTO: < 4h / RPO: < 1h"],
    "delta":       "↔ 复制同步",
}

_TA09_ROWS = [
    {"label": "计算能力",   "items": ["弹性计算(ECS)", "GPU计算",   "Serverless", "边缘计算"]},
    {"label": "存储能力",   "items": ["块存储",        "对象存储",  "文件存储",   "数据库服务"]},
    {"label": "网络能力",   "items": ["VPC专有网络",   "CDN加速",   "DNS解析",    "专线接入"]},
    {"label": "安全能力",   "items": ["身份认证",      "加密服务",  "安全审计",   "合规认证"]},
    {"label": "运维能力",   "items": ["统一监控",      "自动化运维","成本优化",   "容量规划"]},
]


# ─── Individual load functions ─────────────────────────────────────────────────

def load_ta_01_infrastructure_topology(ctx, data):
    return render_node_graph(ctx, data, "TA", defaults=_TA01_GRAPH)


def load_ta_02_deployment_architecture(ctx, data):
    return render_layered_stack(ctx, data, "TA", defaults=_TA02_LAYERS)


def load_ta_03_network_zoning(ctx, data):
    return render_layered_stack(ctx, data, "TA", defaults=_TA03_LAYERS)


def load_ta_04_cloud_architecture(ctx, data):
    return render_layered_stack(ctx, data, "TA", defaults=_TA04_LAYERS)


def load_ta_05_container_orchestration(ctx, data):
    return render_bounded_context(ctx, data, "TA", defaults=_TA05_CONTEXTS)


def load_ta_06_security_architecture(ctx, data):
    return render_layered_stack(ctx, data, "TA", defaults=_TA06_LAYERS)


def load_ta_07_monitoring_observability(ctx, data):
    return render_layered_stack(ctx, data, "TA", defaults=_TA07_LAYERS)


def load_ta_08_disaster_recovery(ctx, data):
    return render_two_column(ctx, data, "TA", defaults=_TA08_DR)


def load_ta_09_platform_capability_map(ctx, data):
    return render_capability_grid(ctx, data, "TA", defaults=_TA09_ROWS)
