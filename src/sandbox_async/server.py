from aiohttp import web
import asyncio


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name + "\n"
    return web.Response(text=text)


async def handle_delay(request):
    name = request.match_info.get('name', "Anonymous")
    delay = int(request.match_info.get('delay', "3"))
    text = "Hello, " + name + "... Sorry for delay\n"
    await asyncio.sleep(delay)
    return web.Response(text=text)


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle),
                web.get('/{name}/{delay}', handle_delay)])

if __name__ == '__main__':
    web.run_app(app)
