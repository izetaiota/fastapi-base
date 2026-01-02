# fastapi-base

一个面向**中大型项目**的 FastAPI 项目骨架（单体结构 + 业务域模块化），目标是提供：

- 可扩展的目录结构与分层边界
- 生产必备中间件（请求日志/耗时、异常兜底、Request-ID、CORS、限流、缓存）
- 异步 ORM（SQLAlchemy 2.0+ async）+ Alembic 迁移
- 统一配置（多环境 `.env.*`）

---

## 技术栈

- **Web 框架**：FastAPI
- **数据校验**：Pydantic + pydantic-settings
- **ORM**：SQLAlchemy 2.0+（AsyncEngine/AsyncSession）
- **数据库迁移**：Alembic
- **JWT**：PyJWT
- **日志**：loguru
- **限流**：slowapi
- **缓存**：fastapi-cache2（Redis backend）
- **ASGI Server**：uvicorn
- **生产部署**：gunicorn + uvicorn worker
- **缓存/存储/消息队列（预留）**：redis / mongo / rabbitmq / kafka

依赖在 `pyproject.toml` 中维护。

---

## 目录结构总览

```text
.
├── main.py                     # 项目启动入口（FastAPI app 创建、挂载路由、中间件）
├── pyproject.toml              # 依赖与工具配置
├── .env.example                # 配置模板（可提交）
├── .env.dev                    # 开发环境（已被 gitignore）
├── .env.test                   # 测试环境（已被 gitignore）
├── .env.prod                   # 生产环境（已被 gitignore）
├── app/                        # API 层（版本化路由、依赖注入）
│   ├── deps.py
│   └── v1/
│       ├── __init__.py
│       ├── user_router.py
│       ├── order_router.py
│       └── product_router.py
├── modules/                    # 业务域模块（推荐：中大型项目核心组织方式）
│   ├── user/
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   ├── crud.py
│   │   └── models.py
│   ├── order/...
│   └── product/...
├── core/                       # 核心配置与全局横切能力
│   ├── config.py               # Settings（支持 .env.<ENV> + .env 覆盖）
│   ├── constant.py             # 常量/错误码
│   ├── exceptions.py           # 业务异常基类
│   └── handlers.py             # 全局异常处理器注册（统一响应）
├── middlewares/                # 生产级中间件
│   ├── __init__.py             # setup_middlewares(app)
│   ├── request_id_middleware.py
│   ├── log_middleware.py
│   ├── exception_middleware.py
│   ├── cors_middleware.py
│   ├── rate_limit_middleware.py
│   └── cache_middleware.py
├── db/                         # DB 连接与模型
│   ├── session.py              # AsyncEngine/AsyncSession
│   └── models/
│       ├── __init__.py         # Base
│       ├── user.py
│       └── order.py
├── crud/                       # 数据访问层（可选：也可以下沉到 modules/*/crud.py）
├── services/                   # 业务服务层（可选：也可以下沉到 modules/*/service.py）
├── schemas/                    # 全局通用 schema（分页/统一返回等）
├── utils/                      # 工具（logger/jwt/http client/time 等）
├── security/                   # 安全相关封装（JWT 入口等）
├── messaging/                  # 事件/消息契约（预留）
├── outbox/                     # outbox 一致性骨架（预留）
├── alembic/                    # 数据库迁移
│   └── versions/
├── tests/                      # 测试
└── scripts/                    # 运维/辅助脚本
```

---

## 分层与模块职责

- **app/**
  - 负责“API 适配层”：版本化路由聚合、依赖注入入口。
  - `app/v1/*_router.py` 为薄封装，最终路由实现位于 `modules/*/router.py`。

- **modules/**（推荐的中大型组织方式）
  - 一个业务域一个目录，域内自洽。
  - 建议在这里实现：`router/schemas/service/crud/models`。

- **core/**
  - 全局配置、错误码、异常体系、统一异常 handler。

- **db/**
  - 数据库连接与 ORM 模型定义。

- **middlewares/**
  - 生产必备中间件统一挂载位置。

- **messaging/** / **outbox/**
  - 为 RabbitMQ/Kafka 与最终一致性预留。
  - 如果你的业务存在“写库 + 发消息”，建议引入 outbox 模式。

---

## 生产级中间件（对应 README 要求）

中间件：fastapi-cache2，slowapi，生产级必备中间件：

- **请求日志 + 耗时统计**：`middlewares/log_middleware.py`
- **全局异常兜底捕获**：
  - 注册入口：`middlewares/exception_middleware.py`
  - 统一处理逻辑：`core/handlers.py`
- **请求 ID 注入（链路追踪必备）**：`middlewares/request_id_middleware.py`
- **跨域 CORS**：`middlewares/cors_middleware.py`
- **限流 slowapi**：`middlewares/rate_limit_middleware.py`
- **缓存 fastapi-cache2**：`middlewares/cache_middleware.py`

统一挂载入口：`middlewares/__init__.py -> setup_middlewares(app)`。

---

## 配置（多环境 .env）

配置文件：

- `.env.example`：模板（可提交）
- `.env.dev`：开发环境
- `.env.test`：测试环境
- `.env.prod`：生产环境

加载规则（见 `core/config.py`）：

1. 先加载 `.env.<ENV>`（例如 `.env.dev`）
2. 再加载 `.env`（如存在，作为本地覆盖）

常用配置项：

- `ENV`
- `PROJECT_NAME`
- `DATABASE_URL`
- `JWT_SECRET` / `JWT_ALG`
- `REDIS_URL`
- `CORS_ORIGINS`
- `RATE_LIMIT`
- `CACHE_PREFIX`

---

## 依赖文件与安装

本项目使用 `pyproject.toml` 管理依赖（PEP 621）。仓库中不使用 `requirements.txt`。

建议使用虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e .
```

如果你不需要可编辑安装，也可以：

```bash
pip install .
```

环境文件准备（示例）：

```bash
cp .env.example .env.dev
```

## 启动方式

开发环境（示例）：

```bash
ENV=dev uvicorn main:app --reload
```

生产环境（示例）：

```bash
ENV=prod gunicorn -k uvicorn.workers.UvicornWorker main:app -w 2 -b 0.0.0.0:8000
```

---

## 数据库迁移（Alembic）

迁移目录：`alembic/`。

- 生成迁移（示意）：`alembic revision --autogenerate -m "init"`
- 执行迁移（示意）：`alembic upgrade head`

`alembic/env.py` 已接入 `db.models.Base.metadata`。

---

## 测试

测试目录：`tests/`，pytest 配置在 `pyproject.toml`。

运行测试（示例）：

```bash
ENV=test pytest
```

---

## 参考项目

https://github.com/smileluck/SmileX-Fastapi-Cloud

https://github.com/atpuxiner/fastapi-scaff/tree/main

https://github.com/Jakkwj/fastapi-skeleton-template/blob/master/README-zh.md