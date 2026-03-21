# Cordys CRM 查询规则

> 最后更新：2026-03-15  
> 用途：规范 CRM 查询的 JSON 结构、关联查询逻辑和专业术语映射

---

## 📋 标准查询结构

**所有 `page` 查询必须使用以下完整结构：**

```json
{
  "current": 1,
  "pageSize": 30,
  "sort": {},
  "combineSearch": {
    "searchMode": "AND",
    "conditions": []
  },
  "keyword": "",
  "viewId": "ALL",
  "filters": []
}
```

**字段说明：**
| 字段 | 默认值 | 说明 |
|------|--------|------|
| `current` | 1 | 页码（从 1 开始） |
| `pageSize` | 30 | 每页条数（最大 500） |
| `sort` | `{}` | 排序（如 `{"createTime":"desc"}`） |
| `combineSearch.conditions` | `[]` | 条件数组 |
| `keyword` | "" | 关键词搜索 |
| `viewId` | "ALL" | 视图 ID |
| `filters` | `[]` | 过滤器数组 |

---

## 🔍 条件拼接规则

### 1. 下拉选择字段（SELECT 类型）

```json
{"value": ["东区"], "operator": "IN", "name": "1751888184000015"}
```

### 2. 时间字段（DYNAMICS 类型）

```json
{"name": "createTime", "operator": "DYNAMICS", "value": "LAST_WEEK"}
```

**支持的动态值：**
- `TODAY` / `YESTERDAY` / `TOMORROW`
- `WEEK` / `LAST_WEEK` / `NEXT_WEEK`
- `MONTH` / `LAST_MONTH` / `NEXT_MONTH`
- `LAST_SEVEN` / `SEVEN` / `THIRTY` / `LAST_THIRTY`
- `QUARTER` / `LAST_QUARTER` / `NEXT_QUARTER`
- `YEAR` / `LAST_YEAR` / `NEXT_YEAR`

### 3. 关联查询（IN 操作符）

```json
{"value": ["id1", "id2", "id3"], "operator": "IN", "name": "customerId"}
```

---

## 🎯 关联查询规则（核心）

### 原则：能单模块就不关联

**✅ 单模块查询（优先）：**
```bash
# 查东区商机（商机有自己的区域字段 1751888184000030）
cordys crm page opportunity '{
  "combineSearch":{"conditions":[{"value":["东区"],"operator":"IN","name":"1751888184000030"}]}
}'
```

### 必须关联的场景

| 场景 | 原因 | 查询步骤 |
|------|------|---------|
| **行业 + 商机** | 商机无行业字段 | 1. 查客户 (行业) → 2. 查商机 (customerId + SUCCESS) |
| **省市 + 商机** | 商机无省市字段 | 1. 查客户 (省市) → 2. 查商机 (customerId + SUCCESS) |
| **产品 + 客户** | 客户无产品字段 | 1. 查商机 (产品) → 2. 查客户 (customerId) |

**重要规则：** 查询"XX 行业客户"或"XX 省市客户"时，默认商机阶段 = `SUCCESS`（已成交）

**关联查询示例（政务行业客户的商机）：**
```bash
# 步骤 1: 查政务行业客户，拿 customerId 列表
cordys crm page account '{
  "combineSearch":{"conditions":[{"value":["政府和军工"],"operator":"IN","name":"1751888184000005"}]}
}' | jq -r '.data.list[].id'

# 步骤 2: 用 customerId 列表查商机
cordys crm page opportunity '{
  "combineSearch":{"conditions":[{"value":["id1","id2"],"operator":"IN","name":"customerId"}]}
}'
```

---

## 📖 专业术语映射

### 产品简称映射

| 简称 | 产品 ID | 产品名称 |
|------|--------|---------|
| `js` / `jms` | `1751888184000091` | JumpServer 企业版 |
| `mk` | `1751888184000102` / `8327632349528064` | MaxKB 专业版 / 企业版 |
| `ms` | `1751888184000098` | MeterSphere 企业版 |
| `de` | `1751888184000101` / `1751888184000092` / `1751888184000097` | DataEase 企业版/专业版/嵌入式版 |

### 行业映射

| 用户输入 | 标准化行业 |
|---------|-----------|
| 汽车 | 制造 |
| 医院、医药 | 医疗（医药、医院、医学检测等） |
| 证券、基金、保险 | 非银金融（证券、基金、保险等） |
| 学校 | 教育 |
| 政府 | 政府和军工 |

### 商机阶段映射

| 用户用语 | CRM 阶段 |
|---------|---------|
| 赢单、下单、成交、案例 | `SUCCESS` |
| 新建 | `CREATE` |
| 需求明确 | `CLEAR_REQUIREMENTS` |
| 方案验证 | `SCHEME_VALIDATION` |
| 立项汇报 | `PROJECT_PROPOSAL_REPORT` |
| 失败 | `FAILURE` |

### 来源映射

| 用户用语 | CRM 来源 |
|---------|---------|
| 新签 | ≠ "多期续费、维保、扩容、增购" |
| 续费 | 多期续费、维保、扩容、增购 |

---

## 🔧 jq 常用命令（重要）

`jq` 是命令行 JSON 处理工具，用于解析、过滤、转换 API 返回的 JSON 数据。

### 基础用法

| 命令 | 作用 | 示例 |
|------|------|------|
| `.data.total` | 提取总数 | `curl ... \| jq '.data.total'` |
| `.data.list[]` | 遍历列表 | `curl ... \| jq '.data.list[]'` |
| `{name,amount}` | 提取指定字段 | `jq '.data.list[] \| {name,amount}'` |
| `select(.amount > 500000)` | 条件过滤 | `jq '[.data.list[] \| select(.amount > 500000)]'` |

### 关联查询专用

```bash
# 提取 ID 列表（纯文本，每行一个）
jq -r '.data.list[].id'

# 转 JSON 数组（供下一步使用）
jq -R . | jq -s .

# 完整流程：客户 ID → JSON 数组
CUSTOMER_IDS=$(cordys crm page account '...' | jq -r '.data.list[].id')
IDS_JSON=$(echo "$CUSTOMER_IDS" | jq -R . | jq -s .)
```

### 产品过滤

```bash
# 筛选包含某产品的记录（如 JS = 1751888184000091）
jq '[.data.list[] | select(.products | if . == null then false else (. | map(. | tostring) | any(. == "1751888184000091")) end)]'

# 筛选金额大于 50 万的记录
jq '[.data.list[] | select(.amount != null and .amount > 500000)]'
```

### 参数说明

| 参数 | 作用 |
|------|------|
| `-r` | 输出纯文本（去掉引号） |
| `-s` | 把多行输入合并成数组 |
| `[]` | 遍历数组元素 |
| `select()` | 条件过滤 |
| `any()` | 判断数组是否包含某值 |
| `map()` | 对数组每个元素应用函数 |

---

## ⚠️ 注意事项

1. **API 端点**：使用 `page` 命令，不要用 `search`（已废弃）
2. **pageSize 限制**：最大 500，超过需分页
3. **字段 ID**：自定义字段必须用字段 ID（参考 `field-mappings.md`）
4. **选项值**：下拉框用显示值（如"东区"），不是选项 ID
5. **金额单位**：元（不是万元）
6. **省市优先级**：优先使用省市字段，商机查询时需转为区域（参考 `region-mapping.md`）

---

## 📝 完整示例

**查询上周东区线索：**
```bash
cordys crm page lead '{
  "current": 1,
  "pageSize": 30,
  "sort": {"createTime": "desc"},
  "combineSearch": {
    "searchMode": "AND",
    "conditions": [
      {"value": ["东区"], "operator": "IN", "name": "1751888184000015"},
      {"name": "createTime", "operator": "DYNAMICS", "value": "LAST_WEEK"}
    ]
  },
  "keyword": "",
  "viewId": "ALL",
  "filters": []
}'
```

**查询政务行业客户的商机（关联查询）：**
```bash
# 步骤 1: 获取客户 ID 列表
CUSTOMER_IDS=$(cordys crm page account '{
  "current": 1,
  "pageSize": 500,
  "combineSearch": {
    "conditions": [
      {"value": ["政府和军工"], "operator": "IN", "name": "1751888184000005"}
    ]
  }
}' | jq -r '.data.list[].id')

# 步骤 2: 转 JSON 数组
IDS_JSON=$(echo "$CUSTOMER_IDS" | jq -R . | jq -s .)

# 步骤 3: 查询商机
cordys crm page opportunity "{
  \"current\": 1,
  \"pageSize\": 500,
  \"combineSearch\": {
    \"conditions\": [
      {\"value\": $IDS_JSON, \"operator\": \"IN\", \"name\": \"customerId\"}
    ]
  }
}"
```
