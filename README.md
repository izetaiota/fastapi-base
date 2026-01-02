fastapi-base：中大型项目项目架构，采用最新技术栈，最新稳定版本依赖。

路由
ORM：SQLAlchemy 2.0+
JWT：PyJWT
数据库迁移：Alembic
数据验证：Pydantic
asgi服务器：uvicorn
生产环境：gunicorn
中间件：fastapi-cache2，slowapi，生产级必备中间件：
1.请求日志 + 耗时统计
2.全局异常兜底捕获
3.请求 ID 注入（链路追踪必备）
4.跨域 CORS 配置（前后端分离必用）



日志系统：loguru
错误处理/异常处理
定时任务/任务调度：https://funboost.readthedocs.io/zh-cn/latest/#
缓存：redis,mongo
消息队列：rabbitmq,kafka




参考项目：
https://github.com/smileluck/SmileX-Fastapi-Cloud

https://github.com/atpuxiner/fastapi-scaff/tree/main

https://github.com/Jakkwj/fastapi-skeleton-template/blob/master/README-zh.md