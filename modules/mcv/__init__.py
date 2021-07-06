from graia.application import MessageChain
from graia.application.message.elements.internal import Plain

from core.template import sendMessage
from core.decorator import command
from .mcv import mcv, mcbv, mcdv


@command(
    name='mcv',
    help='~mcv - 查询当前Minecraft Java版启动器内最新版本。')
async def mcv_loader(kwargs: dict):
    run = await mcv()
    msgchain = MessageChain.create([Plain(run)])
    await sendMessage(kwargs, msgchain)