from fastapi import FastAPI
from app.controllers.auth_controller import router as auth_router
from app.controllers.product_controller import router as product_router
from app.controllers.cart_controller import router as cart_router
from app.controllers.order_controller import router as order_router  
from app.middleware.admin_middleware import AdminMiddleware
from app.middleware.auth_middleware import AuthMiddleware


app = FastAPI(title="Ecommerce API", description="API для электронной коммерции", version="1.0.0")


# Подключаем AuthMiddleware ко всем маршрутам
app.add_middleware(AuthMiddleware)

# Админское middleware только для административных маршрутов
admin_routers = [product_router, cart_router, order_router]
for router in admin_routers:
    app.add_middleware(AdminMiddleware)

# Подключаем маршрутизаторы с тегами для документации
app.include_router(auth_router, tags=["Authentication"])
app.include_router(product_router, tags=["Products"])
app.include_router(cart_router, tags=["Cart"])
app.include_router(order_router, tags=["Orders"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the API"}

# Настройка документации
@app.get("/docs", tags=["Documentation"])
async def custom_docs():
    return {"message": "This is a custom documentation endpoint"}