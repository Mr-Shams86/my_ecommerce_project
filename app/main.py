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

app = FastAPI()


# Инициализируем базу данных
@app.on_event("startup")
async def startup_event():
    print("SECRET_KEY:", settings.secret_key)
    await init_db()
    
# Подключение middleware
app.add_middleware(AdminMiddleware)    
app.add_middleware(AuthMiddleware)

# Подключаем маршруты
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(category_router, prefix="/categories", tags=["categories"])
app.include_router(cart_router, prefix="/cart", tags=["cart"])
app.include_router(order_router, prefix="/orders", tags=["orders"])  