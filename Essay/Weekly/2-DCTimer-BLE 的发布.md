---
date: 2026/05/17
image: /assets/dctimer.png
description: 无
---

## 好物分享

1. [DESIGN.md](https://getdesign.md/)：面向 AI Agent 的设计文稿，收录了很多知名品牌/软件的设计
   Notion，Cursor，Apple，Claude......
   之前也刷到过好几回，今天才去实际看了看并简单尝试
2. [Yepanywhere](https://yepanywhere.com/)：远程接管 Codex 等 Agent 操作，有官方中转的 Web 面板服务，很容易上手，没有复杂的折腾，面板也很直观，推荐一手

## Done

- **周一** 晚上概率论+晚上时间 把 [DCTimer-BLE](https://github.com/huizhiLLL/DCTimer-BLE) 的  [官网](https://dctimer.huizhi.ink) 简单落地，设计上 主要是布局，参考了[妙言](https://miaoyan.app/) 的设计
<img src="./assets/dctimer.png" />
- **周二** 把自己的 [新博客](https://blog.huizhi,ink/) 搭好并迁移数据了 这一版的是我比较喜欢的风格
  下午花了会，捯饬了一般发了 bb 空间，收获两个友链
  
  然后因为狐蒂云跑路了 加上自己 AWS 的 EC2 也还有一个多月到期，顺便都把重要的服务迁到 RN 的第二台 vps 了，2.5 G 内存勉强撑得下（数据迁移这块，把 ssh 信息都扔给 codex 一会就完工了嘻嘻）
  
- **周三** 晚上概率论尝试在服务器跑了几个反代，最后四大外模，只有 Gemini 的 web 和 aistudio 反代成功了，哈基米还是很慷慨的，虽然会有降智，但是 g3f 我是越来越喜欢了
  
  晚点简单了解了一下移动端远程接管 Codex 等 Agent 的方案，最后选择了  [Yepanywhere](https://yepanywhere.com) ，最符合需求的，那个 Happy 似乎是偏向某个 Session 的接管，而不是整个后端的接管，不太灵活
  
  哦还有那个 AI 原生的 Tabbit 浏览器，感觉体验一般
  
- **周四** 上午把爱马仕接到 qq 官bot了，这个官 bot 有好也有坏了，好在富文本，md 格式都能渲染，坏在那个非人超级麻烦的后台管理逻辑，以及我猜测的开发体验也一般 相比 astr （不过单纯接爱马仕个人用的话，倒还行，配两个 ID 即可）
  
  Codex 多项目同时推进开发真的很爽：
  现在在同时写四个东西：DCTimer-BLE、SharpTimer、Cugent、HelloCube
  
  四个项目的完成度依次降低，第一个差不多完善好要上线第一个正式版了
  第二个核心功能基本完善，对于我自用，距离上线还有很多要打磨的地方
  第三个只有核心 poc 的功能验证，整体的使用上还有很多地方要优化
  第四个还只是想法初步探讨，代码还没开始落地
  至于 RubiKey，我祝它好运💦
<img src="./assets/codex.png" />
晚上又试了一下 Yepanywhere，使用官方中转的话，国内网络不是很稳定，容易超时，需要开一下代理，其他的体验都很不错，就是如果能继承 Codex APP 的项目顺序和额外对话历史就好了，而不是只能从 Session 开始，并且没有重命名

另外，我已经开始构建 HelloCube 了~
- 周五下午把 DCTimer 的 logo 点缀了一下，把正式版打包好了，只剩下最后一步，也就是把宣传视频做出来
  最后似乎对于 智能 3D 的渲染，有了一点头绪
  很顺利，摸清技术栈和方案之后，成功将智能 3D 的渲染搞了出来，顺便加上了可拖动
- 周六 继续完善了官网的联动，然后剪了一晚上的宣传视频，效果还不错~

截止周日下午，不到一天，播放就两千三了，流量还不错，用户的反响大部分也都很好，也收到了很多的建议内容，打算周更，频率适中~
