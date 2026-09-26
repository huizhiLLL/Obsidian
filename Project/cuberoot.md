### 9.15

feat：
/scramble 页面各板块布局重构；
/timer gan qiyi moyu32 重置操作加入设备回写；
/timer 设置 ui 优化
/timer 页面布局优化 —— 打乱与时间调换；
/timer 智能魔方相关文案精简优化

fix：
/timer gan v4 qiyi 智能魔方延迟（一包多发）；
/timer moyu32 连接 —— mac 地址获取流程修复以及轴向问题；
/recon 页面 id 不同导致项目重复；
/wca 统计页面子页面主题色未跟随主题；
devOrigin 白名单配置打通开发环境内网穿透；

---

### 9.19

feat：
/timer 陀螺仪加入开关；
/timer 虚拟魔方视角可拖动；

fix：
/account 微信小程序 wca 绑定修复 —— 采用短期绑定票据+浏览器引导；（待线上测试）
/timer 智能魔方重置回写偏差；
/timer 智能魔方结束时自动打开解法开关 & ready 时自动收起解法和复盘；
/timer 复盘区回放速度与实际偏差；
/timer 移动端下智能魔方复盘挤占元素问题优化；
/timer 智能魔方复盘步序与分段分析解法未统一消费；同时优化文案

---

### 9.20

feat：
/site 网站导航页面翻新，组件/主题统一；
/miniprogram 小程序 moyu32 / qiyi 智能魔方跑通；
/mobile 安卓端 ble 适配完成 —— moyu32 / gan v2 v3 / qiyi；
/timer 多人计时联机智能魔方适配；（后端更新 待线上测试）
/timer 智能魔方解法/复盘页加载优化；
/timer 部分窗口遮罩 + 透明玻璃叠加样式优化；

fix：
/recon 页面项目选择器 icon 缺失；
/scramble 统一打乱页面背景图文字样式；
/timer 移动端页面打乱显示空间不足 / 滑动触摸问题；

---

9.22

feat：
/timer 抽智能魔方 shared 组件
/timer 优化复盘区布局 ui/ux 以及移动端下的复盘窗口表现
/timer 优化陀螺仪跟随表现 更跟手
/desktop 完善蓝牙桥接层（moyu32 qiyi）

fix：
/timer 虚拟魔方动作挂载导致的动画缺失

---

9.26

feat：
/timer 复盘分享链接改为短链（登录态 + 分享时服务端保存 后端改动 需待线上验收）
/timer 智能魔方联机功能验收完成
/timer 智能魔方联机 pk 结算反馈与 uiux 优化
/timer 继续抽 shared 统一智能魔方链路与部分timer ui
/scramble Redi 打乱生成切换为 Moyu 风格（参考 cstimer）