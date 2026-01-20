```mermaid
graph TD
    subgraph "UI Presentation Layer Main Thread"
        Window["FluentWindow 主窗口"]
        Nav["NavigationInterface 侧边栏"]
        Pages["StackedWidget 多页面容器"]

        subgraph "Views 页面"
            Page_Home["HomeInterface 3D魔方预览"]
            Page_Config["SettingInterface 按键映射"]
            Page_Log["LogInterface 控制台日志"]
        end
    end

    subgraph "Event Loop Integration"
        QAsync["QAsync / qasync 核心桥梁"]
        QtLoop["Qt Event Loop 负责UI响应"]
        AsyncLoop["Asyncio Loop 负责蓝牙通信"]
    end

    subgraph "Business Logic Layer"
        Service_BT["BluetoothService 蓝牙管理"]
        Service_Map["KeyMapper 映射引擎"]
        State_Cube["CubeState 当前姿态_四元数"]
    end

    subgraph "Hardware Abstraction Layer HAL"
        Driver_GAN["GAN Driver AES解密"]
        Driver_MoYu["MoYu Driver"]
    end

    %% Data Flow
    Window --"用户操作"--> Service_BT
    Service_BT --"connect"--> AsyncLoop
    AsyncLoop --"bleak"--> Driver_GAN

    Driver_GAN --"notify"--> Service_BT
    Service_BT --"Signal pose_changed"--> State_Cube
    Service_BT --"Signal move_detected"--> Service_Map

    State_Cube --"Signal update_3d"--> Page_Home
    Service_Map --"pydirectinput"--> OS_Input["Windows Input API"]

    %% Loop Bridge
    QAsync === QtLoop
    QAsync === AsyncLoop
```
### 表现层
PyQt6 + PyQt-Fluent-Widgets



RubiKey/
├── app/
│   ├── common/              # 通用工具 (Config, SignalBus)
│   │   ├── config.py        # 基于 qfluentwidgets.Config 的配置管理
│   │   └── signal_bus.py    # 全局信号总线
│   ├── components/          # 自定义 UI 组件 (3D View)
│   │   └── cube_gl_view.py  # OpenGL 魔方渲染控件
│   ├── resource/            # 图片、图标、QSS样式
│   ├── view/                # 具体的页面界面
│   │   ├── home_interface.py
│   │   └── setting_interface.py
│   └── main_window.py       # 主窗口组装
├── core/                    # 核心业务 (无 UI)
│   ├── bluetooth_service.py # 封装 Bleak，发射 Qt 信号
│   └── key_mapper.py        # 映射逻辑
├── firmware/                # 硬件协议 (从原项目重构)
│   ├── gan_cube.py
│   └── aes_crypto.py
├── main.py                  # 启动入口 (配置 qasync)
└── requirements.txt