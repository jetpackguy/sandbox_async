import aiohttp
import asyncio
import time


async def fetch(url, session: aiohttp.ClientSession, timeout=None):
    if timeout is None:
        async with session.get(url) as response:
            return await response.text()

    async with session.get(url, timeout=timeout) as response:
        return await response.text()


async def main(fast, slow, slow_delay, session_timeout, request_timeout, connections):
    conn = aiohttp.TCPConnector(limit=connections)
    session_timeout = aiohttp.ClientTimeout(total=session_timeout)
    request_timeout = aiohttp.ClientTimeout(total=request_timeout)
    async with aiohttp.ClientSession(
        connector=conn, timeout=session_timeout
    ) as session:  # noqa
        tasks = []
        url_fast = "http://localhost:8080/fast/"
        url_delay = f"http://localhost:8080/delay/{slow_delay}"
        for _ in range(fast):
            tasks.append(asyncio.create_task(fetch(url_fast, session, request_timeout)))
        for _ in range(slow):
            tasks.append(
                asyncio.create_task(fetch(url_delay, session, request_timeout))
            )

        begin = time.time()
        original_result = await asyncio.gather(*tasks, return_exceptions=True)
        end = time.time()

        fast_answer_count = 0
        slow_answer_count = 0
        timeout_answer_count = 0
        for res in original_result:
            try:
                if res == "Fast":
                    fast_answer_count += 1
                if res.startswith("With delay"):
                    slow_answer_count += 1
            except AttributeError:
                timeout_answer_count += 1
            # print(res)
        print(
            f"Done in {end - begin:0.3}s got {fast_answer_count} fast, "
            f"{slow_answer_count} slow responses and {timeout_answer_count} timeouts"
        )


asyncio.run(
    main(
        fast=60,
        slow=10,
        slow_delay=10,
        session_timeout=3,
        request_timeout=None,
        connections=5
    )
)
