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

### 9.22

feat：
/timer 抽智能魔方 shared 组件
/timer 优化复盘区布局 ui/ux 以及移动端下的复盘窗口表现
/timer 优化陀螺仪跟随表现 更跟手
/desktop 完善蓝牙桥接层（moyu32 qiyi）

fix：
/timer 虚拟魔方动作挂载导致的动画缺失

---

### 9.26

feat：
/timer 复盘分享链接改为短链（登录态 + 分享时服务端保存 后端改动 需待线上验收）
/timer 智能魔方联机功能验收完成
/timer 智能魔方联机 pk 结算反馈与 uiux 优化
/timer 继续抽 shared 统一智能魔方链路与部分timer ui
/scramble Redi 打乱生成切换为 Moyu 风格（参考 cstimer）

---

### 9.27

feat：
/timer 共享层基本抽出 Windows / Android timer 基本完善
/desktop 调整布局和 Web 桌面端统一
/release Google Play 与 ios 上架发布准备（进行中）
/friends 好友间聊天交流（待测试）
/notifications ios 补齐通道和设备能力（待测试）

fix：
/timer Windows 队列拥挤问题导致的智能魔方假连接

---

### 9.29

feat：
/ai-assistant 切为 ds / uiux 改进
/release ios / Android 提审推进（表单填完  ios 等付款协议审核；Google play  差传图和支付接入）
/timer 剩余共享收口
/timer 微信小程序端蓝牙计时器/Stactmat 适配

---

### 10.4（13%）

feat:
/release google play 信息填写推进 支付开发接入

fix:
/timer 布局高度过长以及打乱区滚动条
/timer 内存占用异常
/timer 合并的“？”说明文字补充
/timer 全屏下顶部摄像头安全间距
/tool 搜索框的自动聚焦移除——不再自动拉起输入法
/miniprogram 首页跳转逻辑切回小程序原生页面 —— 保留导航栏
/contact ui 换行优化 —— 防止遮挡
/timer 计时结束时触发打乱跳转
/timer 双人模式布局优化 —— 防止遮挡
/miniprogram 主题颜色继承


---

### 10.5（35%）

feat：
/macos 智能魔方 BLE 适配补齐
/mobile & /desktop 统一：智能计时器以及 stackmat 接入；补齐智能魔方重置回写和更多型号；联机记录复盘；本地多人 状态机；联机房间控制逻辑 + 记录可靠性

fix：
/app webview cookie 回传 —— 正常通过验证码
/timer 空格交互优化 —— 不再干预选项开关
/timer 多人计时页面布局优化 —— 字号 遮挡 图标等
/account 中国城市补齐中文
/miniprogram 语言同步持久保存
/miniprogram “我的”横向溢出
/support 补齐英文姓名翻译
/tools 搜索框➕号样式优化

---
### 10.6(200刀 30 %)

feat:
/release 内购测试完成送审
/timer 统一：本地多人；历史成绩统计；回放；联机视频；多人联机完整页面；普通随机生成链路
/timer 专项训练分离；智能魔方适配(ZBLL)

fix:
/recon 复盘图标布局
/pet 桌宠开关
/appearance 外观面板再次点击关闭
/ui 开关统一样式
/pet 微信小程序桌宠边界设定
/ui 图论页面分割线
/timer 合并提示样式优化 ；移到设置
/timer 联机数据统计维度扩充
/ui 移动端加号卡片层级提高
/math 图论内外环对应关系

---
### 10.7 （200刀32%）

feat:
/timer 智能魔方专项阶段判断；按训练朝向判断；AUF 容许范围；专项训练扩展
/timer 统一基本完成：专项生成完整调度；WCA 真题池完整编排；解法面板外层交互；更多下单工具入口；单人页面总编排
/BLE 工具中蓝牙接入原生宿主
/miniprogram 小程序设备校准——重置回写
/file 文件导出原生适配
/macos 打印原生适配
/timer 计时保亮兜底
 
fix:
/timer 加入返回按钮
/pet 桌宠开关加入另一个入口在桌宠设置
/appearance 外观设置面板滚动影响全站滚动 & 删除诊断按钮
/account 账号管理首页改为返回
/contact 返回首页按钮工作
/miniprogram timer 页面跳转到其他页面的返回问题
/pet 返回按钮
/feedback 分类筛选
/site 改名为“网站导航”
/achievements 字体统一
/miniprogram 页面缓存防止反复重新加载
/timer 选择器统一为一个 & 选择器拖动影响全屏滚动
/recon 操作控件居中 & 链接区优化
/pet 关闭显示继承点击到统计页面
