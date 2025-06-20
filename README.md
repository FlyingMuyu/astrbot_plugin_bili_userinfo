# AstrBot B站用户信息查询插件


通过Bilibili API快速查询用户基础信息的AstrBot插件

## ✨ 功能特性

- 🔍 **精准查询**  
  通过用户UID快速获取详细信息
- 🎨 **丰富展示**  
  包含：
  - 用户名 & 个性签名
  - 等级标识 & 粉丝数量
  - 个人主页链接
  - 高清头像显示
- 🛡️ **智能验证**  
  自动检测MID有效性
- ⚡ **实时响应**  
  毫秒级API响应处理
- 🚨 **异常处理**  
  支持多种错误类型提示：
  ```bash
  # 示例错误提示
  [参数错误]  [用户不存在]  [网络异常]  [系统繁忙]
 ## 📖 使用说明
基础查询
# 指令格式
/up [用户UID]

# 示例（查询账号）
/up 123456
## 响应示例
🏷️ 用户名：哔哩哔哩大会员  
📝 签名：官方认证账号  
⭐ 等级：Lv6  
👥 粉丝数：25,860,000  
🔗 主页：https://space.bilibili.com/123456  
🖼️ 头像：[显示高清头像图片]
## 获取MID帮助
访问用户B站空间页：
https://space.bilibili.com/用户MID
## 二次开发
1.克隆仓库
2.创建特性分支
3.提交Pull Request
欢迎贡献以下类型代码：

性能优化
错误处理增强
新功能模块
文档改进
## 📜 开源协议
MIT License © 2025 FlyingMuyu

## 🙏 特别致谢
AstrBot 核心开发团队
Bilibili API 开放接口
aiohttp 异步HTTP客户端
