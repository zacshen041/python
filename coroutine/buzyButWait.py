import asyncio
import time

now = lambda: time.time()

async def dosomething(num):
    print('第 {} 任務，第一步'.format(num))
    await asyncio.sleep(2)
    print('第 {} 任務，第二步'.format(num))
    return '第 {} 任務完成'.format(num)

async def raise_error(num):
    raise ValueError
    print('will not print')

async def BMI_cal():
    name=input('name:')
    height=eval(input('(m):'))
    weight=eval(input('(kg):'))
    BMI=float(float(weight)/(float(height)**2))
    print(name,' 你的BMI值為: ',BMI)
    return 'BMI測量結束'

async def main():
    tasks0 = [dosomething(i) for i in range(5)]
    tasks1 = [BMI_cal()]
    tasks2 = [raise_error(i) for i in range(5)]

    results = await asyncio.gather(*tasks0, *tasks1, *tasks2, return_exceptions=True)
    print(results)


if __name__ == "__main__":

    start = now()
    asyncio.run(main())
    print('TIME: ', now() - start)