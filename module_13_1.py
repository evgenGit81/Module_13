import asyncio

async def start_strongman(name, power):
    print(f"Силач {name} начал соревнования")
    for i in range(5):
        numglob = i + 1
        await asyncio.sleep(1 / power)
        print(f"Силач {name} поднял {numglob} шар")
    print(f"Силач {name} закончил соревнования.")

async def start_tournament():
    print("Старт")
    task1 = asyncio.create_task(start_strongman('Юрий', 6))
    task2 = asyncio.create_task(start_strongman('Василий', 9))
    task3 = asyncio.create_task(start_strongman('Петр', 5.5))
    await task1
    await task2
    await task3
    print('Соревнования закончены!')

asyncio.run(start_tournament())
