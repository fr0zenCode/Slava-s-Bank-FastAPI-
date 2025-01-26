import uvicorn
from fastapi import FastAPI

from endpoints.accounts import accounts_router
from endpoints.transactions import transactions_router
from endpoints.users import users_router

app = FastAPI()
app.include_router(users_router)
app.include_router(accounts_router)
app.include_router(transactions_router)


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True, port=8000)
