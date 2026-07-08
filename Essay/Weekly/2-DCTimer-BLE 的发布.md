---
date: 2026/05/17
tags:
  - DCTImer-BLE
  - 迁移
  - codex
---
> 最流水账的一集：DCTimer-BLE ，新博客和服务器的迁移，Codex 折腾和开发

## 好物分享

1. [DESIGN.md](https://getdesign.md/)：面向 AI Agent 的设计文稿，收录了很多知名品牌/软件的设计
   Notion，Cursor，Apple，Claude......
2. [Yepanywhere](https://yepanywhere.com/)：远程接管 Codex 等 Agent ，官方提供中转，易上手，直观的 Web UI，推荐尝试~

## 流水账

### DCTimer-BLE 

 用三节课和一晚上，把 [DCTimer-BLE](https://github.com/huizhiLLL/DCTimer-BLE) 的  [官网](https://dctimer.huizhi.ink) 落地，布局设计上，参考了[妙言](https://miaoyan.app/) ~（爱来自 tw93）
 
<img src="./assets/26-02/dctimer.png" />

周五下午把 DCTimer 的 Logo 点缀了一下，把正式版打包好了，只剩最后的宣传视频。
对于虚拟 3D 魔方的渲染，有了一点头绪。在摸清技术栈和方案之后，顺利完成虚拟魔方 3D 渲染~
周六继续完善了官网的联动，剪了一晚上宣传视频，效果还不错~

截止周日下午，不到一天，播放已达 2k+ ，流量不错，大多反响也很好，收到很多建议，打算周更，频率适中~

### 迁移

 [新博客](https://blog.huizhi,ink/) 搭建并迁移数据，采用 Astor-Paper，是我喜欢的风格，随后在 bb空间 收获两个友链~
  
  狐蒂云的跑路  + AWS - EC2 一个月的到期，我把重要服务都迁到 RN 的 vps-2 了，2.5 G 内存勉强够用（用 Codex 迁移服务器非常方便，只需要扔账号密码给它hh）
  
### Codex 开发和折腾

简单了解了移动端远程接管 Codex 等 Agent 的方案，最后选择了  [Yepanywhere](https://yepanywhere.com)  —— 最符合需求
Happy 偏向 Session 的接管，而不是整体接管。

Codex 多项目同时推进开发很爽：
现在同时推进四个项目：DCTimer-BLE、SharpTimer、Cugent、HelloCube
  
DCTimer-BLE 即将完善，要上线正式版了
SharpTimer 核心功能基本完善，自用足够，但距离上线发布还有很多要打磨的地方
Cugent 只有核心 poc ，整体使用上还有很多地方要优化
HelloCube 还只是初步想法探讨，代码未开始落地
至于 RubiKey，我祝它好运💦

<img src="./assets/26-02/codex.png" />

又试了一下 Yepanywhere，使用官方中转的话，国内网络不是很稳定，易超时，需要代理，其他体验很不错。如果能继承 Codex APP 的项目顺序和额外对话就好了，而不是只能从 Session 开始，并且没有重命名。

### 其他

Tabbit：AI 原生浏览器，体验一般

周三晚上的 cpp ，尝试在服务器上跑了几个反代：最后四大外模，只有 Gemini 的 web 和 aistudio 反代成功了，哈基米慷慨！虽然降智，但聊天足够灵动。

周四上午把爱马仕接到 qq 官 bot 了，有好有坏，好在富文本，md 格式都能渲染，坏在非人后台。猜测相比 astr 的开发体验也一般 （不过单纯个人用的话，倒也足够了）