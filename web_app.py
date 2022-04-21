from aiogram import Bot, types
from aiohttp import web
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_response import Response

from config import settings

routes = web.RouteTableDef()


@routes.get('/')
async def index(request) -> Response:
    return FileResponse('static/index.html')

@routes.post('/submitOrder') -> Response:
async def submit_order(request):
    data = await request.json()
    init_data = parse_init_data()

