from fastapi import FastAPI
from app.config import settings 
from app.database import init_db
from app.controllers.auth_controller import router as auth_router
from app.controllers.product_controller import router as product_router
from app.controllers.category_controller import router as category_router
from app.controllers.cart_controller import router as cart_router
from app.controllers.order_controller import router as order_router  
from app.middleware.admin_middleware import AdminMiddleware
from app.middleware.auth_middleware import AuthMiddleware
from app.logging_config import logger


app = FastAPI(title="Ecommerce API", description="API для электронной коммерции", version="1.0.0")


# Инициализируем базу данных
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Запуск приложения...")
        logger.info("SECRET_KEY: %s", settings.secret_key) # Логируем SECRET_KEY
        await init_db()
        logger.info("База данных инициализирована успешно.")
    except Exception as e:
        logger.error("Error during startup: %s", e)
    
# Подключение middleware
app.add_middleware(AdminMiddleware)    
app.add_middleware(AuthMiddleware)

# Подключаем маршруты
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(category_router, prefix="/categories", tags=["categories"])
app.include_router(cart_router, prefix="/cart", tags=["cart"])
app.include_router(order_router, prefix="/orders", tags=["orders"])