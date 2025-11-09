import asyncio
import time
from fastapi import APIRouter

router = APIRouter() 

# Объявляем асинхронную функцию
async def fetch_data():
    print('Начинаем загрузку данных...')
    # Приостанавливаем выполнение на 2 секунды, имитируя сетевой запрос
    await asyncio.sleep(2)
    print('Загрузка данных')
    return {'data': 'Некоторая информация'}

async def main():
    print('Выполняем главную функцию')
    result = await fetch_data() # Ожидаем результат
    print(f'Результат: {result}')
    
# Запуск
@router.get('/example/1',
            summary='Первый пример асинхронных функций ')
def example_aync():
    return asyncio.run(main())

async def task(name: str, delay: int = 0):	
    print(f"Задача: {name}: старт, ждём {delay} сек")
    await asyncio.sleep(delay)
    print(f"Задача '{name}': конец")
    

async def async_tasks():
    print('Выполняем главную функцию')
    start_time = time.time()
    # Запускаем задачи конкурентно
    await asyncio.gather(
        task(name="A", delay=0),
        task(name="B", delay=0),
        task(name="C", delay=0)
    )
    print(f'Результат: Задачи завершены за {time.time() - start_time:.5f} сек')
    
# Запуск
@router.get('/example/2',
            summary='Второй пример асинхронной функции')
def example_aync():
    return asyncio.run(async_tasks())