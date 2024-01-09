from fastapi import APIRouter
from controllers.rootController import rootController
from controllers.orderController import createPosition

router = APIRouter()

@router.get("/")
def root():
    return rootController()

@router.get("/test")
def order():
    return createPosition()