from aiohttp import web
import asyncio

routes = web.RouteTableDef()


@routes.get("/fast")
async def handle_fast(request):
    text = "Fast"
    await asyncio.sleep(1)
    return web.Response(text=text)


@routes.get("/delay/{delay:.*}")
async def handle_delay(request):
    DELAY = 3
    try:
        delay = int(request.match_info.get("delay", DELAY))
    except (ValueError, TypeError):
        delay = DELAY
    text = f"With {delay=}"
    await asyncio.sleep(delay)
    return web.Response(text=text)


app = web.Application(
    middlewares=[web.normalize_path_middleware(remove_slash=True, append_slash=False)]
)
app.router.add_routes(routes)
app.router.add_get("/", handle_fast)


if __name__ == "__main__":
    web.run_app(app)
