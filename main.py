from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Plain, Image
import aiohttp
import json

@register("astrbot_plugin_bili_userinfo", 
         "FlyingMuyu",
         "B站用户信息查询",
         "v1.0",
         "https://github.com/FlyingMuyu/astrbot_plugin_bili_userinfo")
class BiliUserInfo(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.api_url = "http://api.bilibili.com/x/web-interface/card"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AstrBotPlugin/1.0"
        }

    @filter.command("up")
    async def get_user_info(self, event: AstrMessageEvent, uid: str):
        """B站用户信息查询"""
        try:
            # 构建请求参数
            params = {"mid": uid}
            
            # 发送API请求
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.api_url,
                    params=params,
                    headers=self.headers,
                    timeout=10
                ) as response:
                    if response.status != 200:
                        yield event.plain_result("⚠️ 接口请求失败，状态码：{}".format(response.status))
                        return
                    
                    data = await response.json()

                    # 处理API错误响应
                    if data.get("code") != 0:
                        error_mapping = {
                            -400: "请求参数错误",
                            -404: "用户不存在",
                            -412: "请求被拦截",
                            -500: "服务器内部错误"
                        }
                        msg = "⚠️ 接口返回错误：{} ({})".format(
                            error_mapping.get(data.get("code", -1), "未知错误"), 
                            data.get("message")
                        )
                        yield event.plain_result(msg)
                        return

                    # 解析用户数据
                    user_data = data.get("data", {})
                    card = user_data.get("card", {})
                    level_info = card.get("level_info", {})
                    vip_info = card.get("vip", {})

                    # 构建消息链
                    message_chain = []
                    
                    # 添加头像
                    if face_url := card.get("face"):
                        message_chain.append(Image.fromURL(face_url + "@200w.jpg"))
                    
                    # 基础信息
                    info_lines = [
                        f"🔍 用户昵称：{card.get('name', '未知')}",
                        f"🆔 UID：{card.get('mid', '未知')}",
                        f"⭐ 等级：Lv{level_info.get('current_level', 0)}",
                        f"👤 性别：{'男' if card.get('sex') == '男' else '女' if card.get('sex') == '女' else '未知'}",
                        f"💎 大会员状态：{self.parse_vip_type(vip_info.get('type', 1))}",
                        f"💎 大会员等级：{vip_info.get('label', {}).get('text', '无会员')}"
                    ]
                    
                    # 添加基础信息
                    message_chain.append(Plain("\n".join(info_lines)))

                    # 添加数据统计（带换行）
                    stats_lines = [
                        "",
                        f"👥 粉丝数：{self.format_number(user_data.get('follower', 0))}",
                        f"❤️ 关注数：{self.format_number(card.get('attention', 0))}",
                        f"📺 视频数：{self.format_number(user_data.get('archive_count', 0))}",
                        f"👍 获赞数：{self.format_number(user_data.get('like_num', 0))}"
                    ]
                    message_chain.append(Plain("\n".join(stats_lines)))

                    yield event.chain_result(message_chain)

        except aiohttp.ClientError as e:
            logger.error(f"网络请求错误：{str(e)}")
            yield event.plain_result("⚠️ 网络请求异常，请检查网络连接")
        except json.JSONDecodeError:
            logger.error("JSON解析失败")
            yield event.plain_result("⚠️ 数据解析失败，请稍后再试")
        except Exception as e:
            logger.error(f"未知错误：{str(e)}")
            yield event.plain_result("⚠️ 系统繁忙，请稍后再试")

    def parse_vip_type(self, vip_type: int) -> str:
        """解析大会员类型"""
        vip_map = {
            1: "无会员",
            2: "有会员"
        }
        return vip_map.get(vip_type, "未知")

    def format_number(self, num: int) -> str:
        """格式化数字显示"""
        if num >= 10000:
            return f"{num/10000:.1f}万"
        return str(num)

    async def terminate(self):
        """清理资源"""
        pass
