from fastapi import HTTPException, Query
from typing import Optional, List

from fastapi import APIRouter, HTTPException
from .schemas.schemas import Item
import asyncio

router = APIRouter() 

db = {
    0: {'name': 'Apple', 'is_available': True},
    1: {'name': 'Banana', 'is_available': False},
    2: {'name': 'Orange', 'is_available': True}
}

@router.post('/items',
            summary='Создание сущности')
async def add_item(item: Item):
    db.append(item)
    return {'response': 'success'}

@router.get('/items',
        summary='Получение списка сущностей')
def get_items():
    return {'items': list(db.values())}

@router.get('/item/{item_id}',
        summary='Получение сущности')
def get_item(item_id: int):
    item = db.get(item_id)
    if not item:
        raise HTTPException(status_code=404,
                        detail='Item with this id not found')
    return {'item_id': item_id, 'item': item}

@router.get('/search', 
            summary='Поиск сущности')
def search(name: str = Query(None, description="Название для поиска")):
    if name:
        results = [item for item in db.values() if name in item['name']]
        return {'results': results}
    return {'results': list(db.items())}

@router.get('/products', 
            summary='Получение списка сущностей')
def get_products(
        is_available: bool = True ,
        limit: int = Query(10, gt=1, le=100),
        tags: List[str] = Query(None)
    ):
        print(is_available)
        results = [item for item in db.values() if item.get('is_available', False) == is_available][:limit]
        return {'limit': limit,
                'is_availabel': is_available,
                'tags': tags,
                'products': results}

