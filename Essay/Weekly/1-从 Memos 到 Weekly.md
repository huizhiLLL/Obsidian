---
date: 2026/05/10
tags:
  - 迁移
  - Kami
  - 魔方
  - 开发
  - AI
---
> 首篇周刊，包括背景，分享和记录

## 背景

偶然逛到 tw93 老师的 [潮流周刊](https://weekly.tw93.fun/) ，觉得不错，很有价值，（即便只是每周分享）
（然后就 clone 下来二改自用了）

> 顺便一提，原仓库开发文档 404 + post/assets 太多，clone 时需要排除部分资源来加快速度

### 定位思考

**周刊**和**博客**是两种定位
**周刊**：更碎 周期性总结
**博客**：沉淀性分享和总结

### 先前的编排

此前是博客 + 自托管 Memos（多端同步）
博客记沉淀性内容，Memos 偏碎碎念，没事写两笔或当做备忘录/清单，很杂
博客基于 Wordpress，所在服务器快到期，太重，正在迁至 Astro 并复刻原主题。

> 二编：现在更偏好 简洁精炼 优雅风格
> 而非传统的 归档 Tag 友链 关于...... 以及各种卡片/封图的那一套
> 首页无封图的文章列表即可 加之简单的导航栏和页脚 文章 md 渲染 + 无后端的评论区 足够

Memos 太碎 可沉淀价值太低
此类周记，碎片化的总结，刚刚好，介于 Memos 和博客之间，自由而易沉淀
也方便碎碎念（之前博客也发了很多生活的，转在 Weekly 写刚刚好，而不至于污染）

>希望能坚持每周一篇

## 好物分享

- [Kami](https://github.com/tw93/Kami)：强约束的 AI 文档交付，优雅耐看，即便是前端答辩的 GPT 也能交付稳定风格的文档
- [Kaku](https://github.com/tw93/Kaku)：Agent 开发的 skills 技能包，完整实用
- 仓耳今楷：Tw93 常用，比 LXGW 稍正式，更耐看（LXGW 已看腻）

<img src="./assets/26-01/wakatime.png" alt="wakatime" />

(用 Kami 生成的 WakaTime 分析报告)

## 魔方相关开发

最近在写魔方相关的软件：
- [SharpTimer](https://github.com/huizhiLLL/SharpTimer)：Win UI 3 原生计时器，支持智能魔方
- [Cugent](https://github.com/huizhiLLL/Cugent)：初期开发中，偏向定制底层工具的 AI agent，强调魔方领域的交互革新
  Demo 图([演示视频](https://www.bilibili.com/video/BV1wNRZBqEf6/))：

<img src="./assets/26-01/cubeagent.png" alt="cubeagent" />

### 魔方与 AI

基于复原视角下的解法重建很重要， AI 结合前要先完善
实际发现，很玄乎，难保证高准确度（所以 Acubemy 算法很厉害）
Codex 用太多，现在对 Agent loop 和 Toolcall 的已经欲罢不能，所以想起来搓个魔方 Agent，从底层的工具链来革新

至于技术选型，也考虑良久：
- cstimer 浏览器插件：发挥空间不够，只能做轻量化统计
- 原生计时器集成，cstimer 不太可能 pr（AI 堆史山），DCTimer 底子太老，不适合塞 AI

考虑大众使用门槛，选择了 web 的 AI chatbox，花了十几个小时才把 Agent loop 的 demo 做出来
开发过程有些痛苦，搓一个  Agent loop 挺麻烦，对于底层工具的设计上，不够清晰，算法也不会💦

### LCX 逆向

用 GPT-5.4 low 尝试逆向 LCX 的接口：
 一路波折，开始用 mitm，发现手机代理不上（校园网限制？）然后 PCAPdroid 分析流量，HTTPS 抓不到接口，最后暴力反编译 apk，抓到了需要的公开接口（性质的确不好，但客观来说没什么恶劣影响💦）

最后扔到 AstrBot 上集成查询时，发现那台 US 的服务器连 LC 的上游极其不稳定（那老外怎么用的？）
并且周赛接口暂时调不通，参数猜不对，只能调 userId -> 昵称和周赛总榜的接口。

最后在凌晨突发奇思，用我的第二台服务器测试接口的网络连通性，效果非常好。于是果断中转，并且排查出了之前总榜调不通的原因：GPT 把 competition_id 搞成 competitionId 了。
唯一遗憾是选手主页的 PB 成绩没法完善查询，因为只能通过 userId 来查，而昵称 -> userId 的接口并不存在。

## 依然焦虑

大量时间冲浪，AI Fomo。
课程学习忽略了很多 重蹈覆辙 依旧纯摆烂
也无所谓，没什么意义，我不追求绩点和保研
硬技术的提升最重要（srds 机械/电子相关的也一点还没学）

> neruo-sama 可爱捏😊（来自 Codex-Pet）

<img src="./assets/26-01/neuro1.png"  />
<img src="./assets/26-01/neuro2.png"  />
