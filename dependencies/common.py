from fastapi import Query
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    price: float = Field(gt=0)

class OrderIn(BaseModel):
    customer: str
    items: list[Item]   # 嵌套：订单里带多个商品，逐个校验

# 依赖就是一个普通函数：负责"从请求里取出公共参数"
def pagination_params(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页条数"),
):
    return {"page": page, "size": size}