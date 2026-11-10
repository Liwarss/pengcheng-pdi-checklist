# 小米澎程提车现场速查卡

N70 / N90 全系 4 个车型的提车验车清单，提供**浏览器版 HTML** 与**离线 Android APK** 两种用法。每项都写清「检查什么 → 怎么检查 → 合格标准」，现场可逐项打勾。

## 快速开始

| 方式 | 用法 |
| --- | --- |
| Android APK | 下载根目录 `小米澎程提车速查卡_全车型.apk` 安装。自签名应用，首次安装需在系统里允许「安装未知应用」；**零权限、完全离线** |
| 浏览器版 | 打开 `车型速查卡/index.html` → 选择车型 → 逐项勾选。进度存在浏览器 localStorage，按车型分别保存 |
| 打印 A4 | 电脑浏览器打开 `车型速查卡/cards/<车型>.html` → 「打印 / 存 PDF」，每张清单为单页 A4 |

APK 启动后先进入车型选择页，4 张卡片配官方渲染图；点进去是各自独立的清单，切换车型不会串进度，并记住「上次使用」的车型。

## 车型与清单

| 车型 | 指导价 | 清单项数 | 主要专项 |
| --- | --- | --- | --- |
| N70 Pro | 20.99 万 | 45 | 前驱 210kW / 52kWh 磷酸铁锂 / CLTC 351km；空悬是否标配以订单配置页为准 |
| N70 Max | 23.99 万 | 45 | 四驱 310kW / 505km / 5 挡空悬 + CDC / 激光雷达 / HUD / 25 扬声器 / 车载冰箱 |
| N90 Max | 26.99 万 | 47 | 2+2+3 七座 / 464km / 21 寸鸳鸯胎 / 2 万豪华套装 6 件逐项验收 / 滑动中岛 / HAD 权益 |
| N90 Max 探索版 | 29.99 万 | 46 | 电动升降顶舱反复升降、四角密封、应急中断与手动关闭、地暖、限高预警 |

## 目录结构

```
.
├── README.md
├── .gitignore
├── 小米澎程N90_Max_提车验车清单_20261114.html   # 55 项详细版（含怎么检查/合格标准）
├── 小米澎程N90_Max_提车速查卡_A4_20261114.html  # 原始单车型 A4 速查卡（样式源）
├── 小米澎程提车速查卡_全车型.apk                 # 可直接安装的成品
├── 车型速查卡/                                   # 浏览器版（选择页 + 4 卡 + 4 图）
│   ├── index.html
│   ├── cards/*.html
│   └── img/*.jpg
└── android/                                      # 可复现构建（不含 1.1GB 工具链）
    ├── make_cards.py                             # 生成 4 张清单 + 选择页并同步到 assets
    ├── build.sh                                  # javac → d8 → aapt2 → zipalign → apksigner
    └── project/
        ├── AndroidManifest.xml
        ├── java/com/liwar/n90check/MainActivity.java
        ├── res/mipmap-hdpi/ic_launcher.png
        └── assets/                               # 内嵌页面（与 车型速查卡/ 内容一致）
```

## APK 实现说明

- 包名 `com.liwar.n90check`，minSdk 23 / targetSdk 34，**不申请任何权限**（页面无外部 URL）。
- `MainActivity` 是一个最小 WebView 壳，加载 `file:///android_asset/index.html`。
- 勾选状态通过 `AndroidStore` JS Bridge 写入 `SharedPreferences`，按 `check_<车型>_v1` 独立存储；浏览器版自动回退到 `localStorage`。
- 签名采用 v1/v2/v3 自签名证书。**私钥 `n90.keystore` 不入库**，`build.sh` 会在本地自动生成；正式分发请替换为自己的密钥，并通过 `KS_PASS` 环境变量设置口令（脚本里的默认值只是本地演示口令，不是凭据）。
- 沿用同一份 keystore 重新构建时，APK 可直接覆盖安装；在没有该证书的机器上构建会生成新证书，**签名不同的 APK 需先卸载旧版再安装**。

## 修改清单 / 复现构建

改内容请编辑 `android/make_cards.py` 中的 `MODELS`、`common_sections()`、`SPECIAL`，然后：

```bash
python3 android/make_cards.py     # 重新生成 车型速查卡/ 并同步到 android/project/assets/
```

构建 APK 需要 **JDK 17 + Android SDK platform 34 + build-tools 34.0.0**：

```bash
export JAVA_HOME=/path/to/jdk-17
export ANDROID_SDK_DIR=/path/to/android-sdk   # 其下有 platforms/android-34 与 build-tools/34.0.0
bash android/build.sh                          # 输出覆盖到仓库根目录的 APK
```

若不设环境变量，脚本会回退到 `android/jdk`、`android/sdk` 便携目录（这两个目录不在仓库里）。

## 数据来源与免责声明

- 配置与价格整理自 2026 年 9 月上市公开信息及车主提车反馈；网上对个别配置（如 N70 Pro 是否标配空悬）口径不一，一律以订单配置页与实车为准。
- 清单中引用的车主投诉（车质网、汽车投诉网、社区提车作业等）属**个案反馈，不代表批次性质量结论**。
- 里程 ≤50km、SOH ≥95%、漆膜 90–160μm 等数值为行业通用／媒体经验值，**最终以小米官方 PDI 报告与随车文件为准**。
- 4 张车型图片取自小米汽车官网公开渲染图，仅作车型识别示意，**版权归原权利人所有**；如有异议请提 issue 移除。
- 本项目为个人整理的验车辅助工具，与小米公司无关联，非官方资料；据此作出的提车决定由使用者自行判断。

## 许可

仓库未附带 LICENSE，默认保留所有权利。如需开源复用，请先自行补充许可文件。
