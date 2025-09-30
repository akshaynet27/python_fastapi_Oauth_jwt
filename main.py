from fastapi import FastAPI
import login
import product
import seller

app=FastAPI(title="Product Management website",description="This is a simple product management website",version="1.0.0")

app.include_router(login.router,tags=["Login"])
app.include_router(product.router,tags=["Products"])
app.include_router(seller.router,tags=["Sellers"])
