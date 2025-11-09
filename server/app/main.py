"""
FastAPI应用主入口
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.api.v1 import auth, users, poetry, author, interaction, comment, search, recommend, follow, post, message
from app.utils.elasticsearch_client import ESClient

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description="星语诗词平台API文档",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 应用生命周期事件
@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    # 初始化ES客户端
    ESClient.get_client()


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    # 关闭ES客户端
    await ESClient.close()


# 健康检查
@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查接口"""
    return JSONResponse(
        content={
            "status": "ok",
            "service": settings.APP_NAME,
            "version": "1.0.0",
            "environment": settings.APP_ENV,
        }
    )


# 根路径
@app.get("/", tags=["根路径"])
async def root():
    """根路径"""
    return {
        "message": "欢迎使用星语诗词平台API",
        "docs": "/docs",
        "health": "/health",
    }


# 注册路由
app.include_router(auth.router, prefix="/api/v1", tags=["认证"])
app.include_router(users.router, prefix="/api/v1", tags=["用户"])
app.include_router(poetry.router, prefix="/api/v1", tags=["诗词"])
app.include_router(author.router, prefix="/api/v1", tags=["作者"])
app.include_router(interaction.router, prefix="/api/v1", tags=["交互"])
app.include_router(comment.router, prefix="/api/v1", tags=["评论"])
app.include_router(search.router, prefix="/api/v1", tags=["搜索"])
app.include_router(recommend.router, prefix="/api/v1", tags=["推荐"])
app.include_router(follow.router, prefix="/api/v1", tags=["关注"])
app.include_router(post.router, prefix="/api/v1", tags=["广场"])
app.include_router(message.router, prefix="/api/v1", tags=["消息"])


# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """HTTP异常处理器 - 处理认证、权限等HTTP错误"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "status": False,
            "msg": exc.detail,
            "data": None,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """参数验证异常处理器"""
    errors = exc.errors()
    error_msgs = []
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"])
        msg = error["msg"]
        error_msgs.append(f"{field}: {msg}")

    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "status": False,
            "msg": "参数验证失败: " + "; ".join(error_msgs),
            "data": {"errors": errors} if settings.DEBUG else None,
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器 - 捕获所有未处理的异常"""
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "status": False,
            "msg": "服务器内部错误",
            "data": {"detail": str(exc)} if settings.DEBUG else None,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
