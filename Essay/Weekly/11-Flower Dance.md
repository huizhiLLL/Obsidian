---
date: 2026/07/19
image: /assets/26-11/bg.jpg
description: 藏在轻快旋律里的浪漫
---
> [Flower Dance](https://music.163.com/song?id=22676167&uct2=U2FsdGVkX1+jTOHIvmUzGQhWSN++RDFNsoS/Xm0SCYY=) 「花之舞」，轻盈流畅的钢琴旋律，明亮而富有活力

在音乐开头有一段对白，它取自 1960 年意大利科幻电影《Assignment: Outer Space》

电影中，男女主角正在讨论太空站里的一种植物：

Lucy: They serve the purpose of changing hydrogen into breathable oxygen, and they're as necessary here as the air is on Earth
（就是说这些植物能够提供维持生命所必需的氧气）

Ray: But I still say… they're flowers.

Lucy: If you like.

Ray: Do you sell them?

Lucy: I'm afraid not.

Ray: But maybe we could make a deal.

音乐里的对白到这里便结束了，但电影中的对话其实还没有结束：

女方好奇他所说的交易是什么意思，男方解释：他愿意出钱买下这些花，却不打算将它们带走，而是把它们留在原地，送给她。原来，他是借此向她表达好感。

这就让整段对话有了一种很巧妙的浪漫感：在女方眼里，那是维持生命的植物；在男方眼里，它们还可以是一份礼物。

---

## 分享

### GPT-5.6-Luna（Max）

根据实测体验以及社区评价，GPT-5.6-Luna，配上 Max ，实际的开发体验很不错
建议配合 Sol 分析+写计划/实施方案，Luna 执行
Luna 的执行成本低，耐用，日常开发完全够用~
至于 Sol，社区认为高推理强度的效果并不满意 —— 想太多了
所以一般使用 Medium 即可

> 推荐模型也是好物分享（）

## 随便讲讲

### 开发（RubiKey）

起因是看到一个“用智能魔方玩地铁跑酷”的短视频，结果发现是录屏的......

和 GPT 简单讨论，得到了真正实现的方案，花费约 1h 完成了 POC —— 使用无障碍服务自动化操作
技术栈： Kotlin + Jetpack Compose Material 3 + Java core（协议核心层复用 DCTimer-BLE ）
在后来的 ui/ux 优化以及多品牌兼容的基础上，发布了第一个 0.2.0 的正式版

UI 很切合我的口味，颜值很高（主题选择黑白）
具体可以去 [huizhiLLL/RubiKey-Android: 智能魔方控制安卓设备](https://github.com/huizhiLLL/RubiKey-Android) 看到截图~

### 关于 RubiKey

这个名字最早在 3月底使用，即[用智能魔方玩 MC 中的魔方](https://www.bilibili.com/video/BV1ZaQmB4EsG) 过程中开发的软件，[面向 Windows 的智能魔方自动化操作客户端](https://github.com/huizhiLLL/RubiKey)

当时认为它没什么介绍和发布价值，仅在复刻教程中提及使用，且使用门槛不低（Win 11 + Mac 获取）
原 RubiKey 所使用的技术栈相当糟糕 —— Electron 会受浏览器沙盒限制，不仅蓝牙连接，实现自动化操作更是麻烦。所以现在看来，也的确没什么介绍和发布价值💦

而 RubiKey-Android，整体更加满意，门槛低，体积小，易用，多品牌，简洁，高颜值 .....
功能不多，本质的核心需求仍然是娱乐整活向，因此会简单介绍，不作过多笔墨

事实上，出于个人在智能魔方上的应用层花费太多时间和尝试，已逐渐感觉枯燥与乏味，觉得一直在整烂活 —— 技术上并没什么创新，只是应用层的缝合，而外人看来仍然存在一定的新鲜感。

### 吐槽 —— dy

辛辛苦苦剪完 RubiKey 的教程视频，正准备发布在 dy 和 b 站时，却收到了以下的提示：

<img src="./assets/26-11/rubikey.jpg" />

当尝试把简介的链接相关内容删除后重新发布，仍然提示违规 —— 应该是视频内容中含有外链的原因
那就需要重新修改视频 会麻烦很多 —— 干脆放弃发布，选择发一条简介贴 b 站视频引导的图文 ......

首次被 dy 制裁，本身对 dy 的印象就很差（评论区），这下更差
虽然理解引导外链影响软件本身的流量，但切的太死，对分享性质的内容严重打击，我反感遍地的“求”，“私发”，浪费时间 ......