"""生成 4 个车型的提车现场速查卡 + 车型选择页。

浏览器版与 APK 内嵌版共用同一套 HTML：
- JS 自动判断 window.AndroidStore（APK）或 localStorage（浏览器）
- 相对路径 img/ 与 cards/ 在两处结构一致
"""
from pathlib import Path
import re
import html

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
OUT = WORKSPACE / "车型速查卡"
APK_ASSETS = ROOT / "project" / "assets"
BASE_CARD = WORKSPACE / "小米澎程N90_Max_提车速查卡_A4_20261114.html"

# 复用现有速查卡的样式（含单页 A4 紧凑修正与手机视图）
_src = BASE_CARD.read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", _src, re.S).group(1)
EXTRA_CSS = """
  /* 车型矩阵版新增 */
  .back{display:inline-block;font-size:11px;color:#1d5fa8;text-decoration:none;padding:2px 0;margin-bottom:4px}
  .modelnote{font-size:9.5px;color:#5a6572;margin:0 0 5px;line-height:1.5}
  .tag{display:inline-block;font-size:8.6px;font-weight:700;padding:0 4px;border-radius:3px;margin-left:4px;vertical-align:1px}
  .tag.hi{background:#fdf0ef;color:#c8362f}
  .tag.mid{background:#fff7e8;color:#a86a12}
  .tag.info{background:#eef4fc;color:#1d5fa8}
  @media screen and (max-width:820px){
    .back{display:block;font-size:13px;padding:9px 11px;background:#eef4fc;border-radius:8px;margin-bottom:8px;color:#1d5fa8}
    .modelnote{font-size:11px;line-height:1.6;margin-bottom:8px}
    .tag{font-size:10px;padding:1px 5px;margin-left:5px}
    .bar-btns button:first-child{display:none}
  }
  @media print{.back{display:none!important}}
"""

MODELS = [
    {
        "id": "n70_pro", "name": "N70 Pro", "full": "小米澎程 N70 Pro",
        "price": "20.99 万", "tax": "约 9300 元", "img": "n70_pro.jpg",
        "tagline": "入门大五座 · 前驱高性价比",
        "specs": ["2+3 大五座", "前驱 210kW", "纯电 351km"],
        "cond": ["N70 Pro（大五座）", "20.99 万", "前驱 210kW · 52kWh 磷酸铁锂", "未选装按订单核对"],
        "ev": "351km", "total": "1351km", "battery": "52kWh 磷酸铁锂",
        "drive": "前置前驱 210kW / 0-100km/h 7.9s",
        "seats": "2+3 大五座 / 5 条安全带", "airbag": "9 个安全气囊",
        "wheels": "按订单轮毂款式与规格核对（勿套用 N90 的 21 寸鸳鸯胎）",
        "option": "选装件（轮毂／车漆／舒适包等）",
        "wade": "600mm 涉水能力",
        "modelnote": "本卡按 N70 Pro 标准配置编写。网上对 Pro 是否标配空气悬架口径不一，现场一律以订单配置页和实车为准。",
    },
    {
        "id": "n70_max", "name": "N70 Max", "full": "小米澎程 N70 Max",
        "price": "23.99 万", "tax": "约 10600 元", "img": "n70_max.jpg",
        "tagline": "长续航性能五座 · 四驱 + 空悬",
        "specs": ["2+3 大五座", "四驱 310kW", "纯电 505km"],
        "cond": ["N70 Max（大五座）", "23.99 万", "双电机四驱 310kW · 76kWh", "5 挡空悬 + CDC"],
        "ev": "505km", "total": "1461km", "battery": "76kWh 三元锂",
        "drive": "双电机四驱 310kW / 0-100km/h 5.5s",
        "seats": "2+3 大五座 / 5 条安全带", "airbag": "9 个安全气囊",
        "wheels": "按订单轮毂款式与规格核对",
        "option": "选装件（轮毂／车漆／舒适包等）",
        "wade": "650mm 涉水能力",
        "modelnote": "本卡按 N70 Max 标准配置编写；相比 Pro 主要多四驱、大电池、5 挡空悬+CDC、激光雷达、HUD、25 扬声器与冰箱，逐项确认没被错装成 Pro。",
    },
    {
        "id": "n90_max", "name": "N90 Max", "full": "小米澎程 N90 Max",
        "price": "26.99 万", "tax": "约 11900 元", "img": "n90_max.jpg",
        "tagline": "旗舰大七座 · 2+2+3 真七座",
        "specs": ["2+2+3 大七座", "四驱 310kW", "纯电 464km"],
        "cond": ["N90 Max（大七座）", "26.99 万", "双电机四驱 · 76kWh", "2 万豪华套装：已选才查"],
        "ev": "464km", "total": "1705km", "battery": "76kWh 三元锂",
        "drive": "双电机四驱 310kW / 0-100km/h 5.9s",
        "seats": "2+2+3 大七座 / 7 条安全带", "airbag": "12 个安全气囊",
        "wheels": "21 寸轮毂、前 255 / 后 265 鸳鸯胎",
        "option": "2 万豪华套装（智能电动门／21.4 寸后排屏／电动迎宾踏板／9L 冰箱／麂皮顶／主驾外后视镜防眩目）",
        "wade": "750mm 涉水能力",
        "modelnote": "本卡按 N90 Max 七座版通用配置编写；07 区「2 万豪华套装」为选装件，未选可跳过。第三排安全带固定在 D 柱属设计特性，现场确认家人能否接受。",
    },
    {
        "id": "n90_explorer", "name": "N90 Max 探索版", "full": "小米澎程 N90 Max 探索版",
        "price": "29.99 万", "tax": "约 13300 元", "img": "n90_explorer.jpg",
        "tagline": "原厂升降顶舱 · 5 座露营 LOFT",
        "specs": ["2+3 大五座", "电动升降顶舱", "纯电 462km"],
        "cond": ["N90 Max 探索版（大五座）", "29.99 万", "双电机四驱 · 76kWh", "无第三排 · 顶舱为原厂标配"],
        "ev": "462km", "total": "1688km", "battery": "76kWh 三元锂",
        "drive": "双电机四驱 310kW / 0-100km/h 5.9s",
        "seats": "2+3 大五座 / 5 条安全带", "airbag": "12 个安全气囊",
        "wheels": "21 寸轮毂、前 255 / 后 265 鸳鸯胎",
        "option": "探索版专属配置（升降顶舱／地暖／冰箱／电动吸合门，30 寸投影为选装）",
        "wade": "750mm 涉水能力",
        "modelnote": "本卡按 N90 Max 探索版编写：5 座布局、无第三排，原厂电动升降顶舱是核心，密封与升降机构必须反复试。11/4 官方宣布珍珠白探索版开启交付，白色属较新批次。",
    },
]


def it(text, ok, tag=""):
    return (text, ok, tag)


def common_sections(m):
    """6 个通用前置分区（01–06）"""
    return [
        {"no": "01", "title": "开场 3 分钟", "note": "身份与订单", "items": [
            it("三码合一：前挡／B柱／机舱／地毯 VIN 对合格证、发票", "17 位逐字符完全一致，差一位即拒提"),
            it("副驾 B 柱铭牌出厂日期", "≤3 个月；>6 个月要书面说明＋换油液"),
            it("表显里程＋胎毛／座椅保护膜", "≤50km 正常；>100km 书面说明"),
            it(f"对照订单：{m['full']}、车漆、轮毂、{m['option']}", "与订单／发票／配置页一致，少一项写进交付单"),
            it("确认是排产新车，非展车／试驾车／准新车", "交付单书面写明车辆来源"),
        ]},
        {"no": "02", "title": "外观漆面", "note": "室外自然光＋手电 45° 斜照", "items": [
            it("车顶、前后杠四角、翼子板、门边、门槛（运损高发）", "无划痕／凹陷／掉漆／色差"),
            it("漆膜仪逐面测（先取原厂基准）", "90–160μm、相邻差 ≤30μm；局部 >200μm 疑补漆"),
            it("四门／机盖／尾门／大灯接缝左右对比", "缝差 ≤1mm、面差 ≤0.5mm"),
            it("各开闭件、密封胶条、半隐藏门把手开关 2 次", "顺畅、无翘边脱胶"),
            it("全车玻璃／灯罩／雨刮胶条", "无裂纹水雾、胶条不开裂（车主踩过坑）"),
        ]},
        {"no": "03", "title": "轮胎与玻璃日期", "note": "", "items": [
            it("四胎 DOT 四位码＋全车玻璃批号", "早于整车出厂；四胎互差 ≤3 个月"),
            it(f"胎毛、鼓包、轮毂、胎压：{m['wheels']}", "无伤、规格与订单一致；冷车胎压按 B 柱标签"),
        ]},
        {"no": "04", "title": "机舱 · 三电 · 增程器", "note": "别只当电车验", "items": [
            it("冷却液／刹车油／机油尺＋管路接头、12V 接线", "MAX–MIN、F–L，琥珀透明、无渗漏"),
            it("冷启动增程器（交代别提前热车）怠速 3–5 分钟", "无敲击啸叫、方向盘无明显抖动"),
            it(f"读 SOH／循环次数、表显纯电续航（标定 CLTC {m['ev']}，{m['battery']}）", "SOH ≥95%、循环 <50 次、表显偏差 ≤10%"),
            it("快慢充枪插拔 2 次＋试充 3 分钟、油箱盖", "无啸叫松动、能握手、密封正常"),
        ]},
        {"no": "05", "title": "举升看底盘", "note": "11/3 澎程系列共性提醒", "items": [
            it("左右后悬架全铝 H 臂对比拍照（车质网 1817363 打磨痕迹投诉）", "纹理一致、无打磨；有则书面说明／换件"),
            it("电池包护板、底盘护板、减振器", "无托底变形渗漏；不给举升就在交付单写「未举升」"),
        ]},
        {"no": "06", "title": "内饰装配", "note": "", "items": [
            it(f"{m['seats']}：座椅表面与缝线、保护膜", "无污渍跳线断线（车主踩过坑）"),
            it("全部安全带拉到底回卷＋锁止", "回卷顺、锁止可靠"),
            it("6 根滑轨槽内异物、盖板、中控门板缝隙", "干净无金属屑、按压无异响"),
        ]},
    ]


SPECIAL = {
    "n70_pro": [
        {"no": "07", "title": "Pro 版配置核对", "note": "别按 Max 宣传稿验", "star": True, "items": [
            it("前驱单电机 210kW / 0-100km/h 7.9s", "车机驱动状态为两驱、无后电机，与订单一致"),
            it("52kWh 磷酸铁锂、CLTC 351km / 综合 1351km", "铭牌／车机参数与订单一致"),
            it("空气悬架与 CDC 是否配备：网上口径不一", "以订单配置页＋实车为准；有则按 08 区测升降，无则跳过"),
            it("基础音响（非 25 扬声器）、HUD／冰箱若未选装", "逐项核对，缺件或与宣传不符写进交付单"),
            it("9 气囊、14 处 2200MPa 超强钢、龙甲电池 500J / 55℃", "仪表无气囊故障灯、配置单一致"),
            it("600mm 涉水、最小转弯半径 5.67m", "涉水模式可开启；窄路掉头试一次"),
            it("若选装轮毂／车漆／舒适包", "逐项对照订单，未装写进交付单"),
        ]},
        {"no": "08", "title": "N70 特色机构", "note": "只验漆面等于没验", "items": [
            it("6 根 1938mm 纯平地板滑轨＋18 种场景模式", "全行程顺滑、锁止无松旷、槽内无异物"),
            it("前排座椅一键放平成床、5 座布局与后备厢扩展", "动作到位、复位无报警、容积符合标定"),
            it("空调出风、音响、全车灯光、车窗防夹 ≥4 次", "制冷制热有效、全部点亮、防夹回弹"),
            it("门把手三重冗余、充电口盖、随车工具", "应急开启可演示、无卡滞"),
            it("车机账号、小爱语音、记录仪 U 盘、ETC", "权益绑定本人账号、U 盘已插、ETC 可激活"),
        ]},
    ],
    "n70_max": [
        {"no": "07", "title": "Max 相对 Pro 的增配验收", "note": "这 3 万买的东西", "star": True, "items": [
            it("双电机四驱 310kW / 0-100km/h 5.5s", "车机可查四驱状态，与订单一致"),
            it("76kWh 三元锂、CLTC 505km / 综合 1461km", "表显与标定偏差 ≤10%"),
            it("5 挡空气弹簧＋CDC、前后 4 个液压衬套", "升降 3 次：10 秒内、四角同步、熄火 10 分钟不下沉"),
            it("车顶激光雷达＋HAD 满配辅助驾驶", "硬件无磕碰、权益已绑定本人账号"),
            it("HUD、25 扬声器星弦音响、独立压缩机冰箱", "逐项试：显示／各声道／制冷制热"),
            it("385mm 加宽后门槛、650mm 涉水", "外观与车机涉水模式确认"),
            it("若选装轮毂／车漆／舒适包", "逐项对照订单，未装写进交付单"),
        ]},
        {"no": "08", "title": "N70 特色机构", "note": "只验漆面等于没验", "items": [
            it("6 根 1938mm 纯平地板滑轨＋18 种场景模式", "全行程顺滑、锁止无松旷、槽内无异物"),
            it("前排座椅一键放平成床、5 座布局与后备厢扩展", "动作到位、复位无报警、容积符合标定"),
            it("空调出风、音响、全车灯光、车窗防夹 ≥4 次", "制冷制热有效、全部点亮、防夹回弹"),
            it("门把手三重冗余、充电口盖、随车工具", "应急开启可演示、无卡滞"),
            it("车机账号、小爱语音、记录仪 U 盘、ETC", "权益绑定本人账号、U 盘已插、ETC 可激活"),
        ]},
    ],
    "n90_max": [
        {"no": "07", "title": "2 万豪华套装验收", "note": "已选才查 · 未选可跳过", "star": True, "items": [
            it("智能电动门 6 种开闭方式各 2 次＋防夹＋应急手动释放", "每次都能开闭（10/27 有偶发打不开）"),
            it("21.4 寸后排娱乐屏黑白红纯色＋翻转机构", "无坏点、无磕碰划痕（车主反馈过磕碰）"),
            it("电动迎宾踏板随门伸缩 3 次", "到位、无卡顿异响、无松旷"),
            it("9L 压缩机冰箱制冷／制热＋放水瓶", "都工作；SOC<20% 自动关闭属已知逻辑"),
            it("麂皮绒车顶＋顶棚", "无污渍压痕塌陷；拾音口冲孔是设计非故障"),
            it("主驾外后视镜防眩目", "功能可开、镜面无划痕"),
            it("若另购香氛机／闻献套装：装上通电、开关 3 次", "不掉线（11/5–11/6 投诉为供电触点不良，避免新车拆内饰）"),
        ]},
        {"no": "08", "title": "N90 特色机构", "note": "只验漆面等于没验", "items": [
            it("前排 180° 电动旋转（按键＋小爱各一次）、二排零重力／16 点按摩／通风加热", "全行程无卡滞、复位无报警"),
            it("一键成床／对坐模式至少各 1 次＋完整复位", "床面平顺、行车前座椅可复位"),
            it("二三排超长滑轨推满全程＋滑动中岛来回 3 次", "无卡顿、无「嗒嗒」共振、锁止无松旷"),
            it("空气弹簧＋CDC 5 挡来回 3 次", "10 秒内升降、四角同步、熄火 10 分钟不下沉"),
            it("17 出风口制冷制热各 3 分钟、25 扬声器、全车灯光", "温差 ≥8℃、无破音、全部点亮"),
            it("四门车窗升降 ≥4 次＋防夹、天窗遮阳帘、雨刮喷淋", "无卡顿异响、防夹回弹、关严不漏光"),
            it("第三排座椅前后调节＋D 柱安全带够取", "各位置都能扣上；够不到属设计特性，现场确认能接受"),
        ]},
    ],
    "n90_explorer": [
        {"no": "07", "title": "升降顶舱专项验收", "note": "探索版核心 · 反复试", "star": True, "items": [
            it("驻车状态连续升／降 2–3 次（官方约 26 秒完成）", "左右电机同步、无卡顿歪斜异响"),
            it("四角密封条、篷布涂层、手电照一圈接缝", "无压伤脱胶破损；关闭后车高仅 +100mm、无漏风"),
            it("应急中断（车顶阅读灯区危险警告灯开关）、手动应急关闭", "现场演示可用；问清雨天／锁车降雨提醒"),
            it("二层配置：五面纱窗、照明、双空调出风口、18W Type-C、磁吸点位", "齐全可用；承重 200kg 标识清楚"),
            it("地暖三挡、木纹铝合金地板、二排一键成床 1.87m×1.24m", "发热正常、成床平顺、行车前可复位"),
            it("确认 5 座布局（无第三排）、冰箱／电动吸合门为标配", "与订单一致；30 寸投影若选装需装上验"),
            it("UWB 生物体检测、上方超声波雷达、激光雷达限高预警", "让专员逐项演示；确认顶舱仅非公共道路＋驻车可用"),
        ]},
        {"no": "08", "title": "N90 特色机构", "note": "只验漆面等于没验", "items": [
            it("前排 180° 电动旋转、二排零重力／按摩／通风加热", "全行程无卡滞、复位无报警"),
            it("6 根超长滑轨推满全程＋滑动中岛来回 3 次", "无卡顿、无「嗒嗒」共振、锁止无松旷"),
            it("空气弹簧＋CDC 5 挡来回 3 次", "10 秒内升降、四角同步、熄火 10 分钟不下沉"),
            it("9L 冰箱制冷制热、25 扬声器、17 出风口", "都工作、无破音、温差 ≥8℃"),
            it("全车灯光、四门车窗 ≥4 次＋防夹、天窗遮阳帘、雨刮", "全部点亮、防夹回弹、胶条不开裂"),
            it("顶舱关闭状态下低速掉头、地库限高预警", "车高 1925mm，影像与预警正常、无刮顶风险"),
        ]},
    ],
}


def tail_sections(m):
    return [
        {"no": "09", "title": "车机 · 账号 · 权益", "note": "", "items": [
            it("登录本人小米账号、小爱控导航／空调、OTA 最新、HAD 权益绑定", "权益在账号内可见、无展车遗留账号"),
            it("行车记录仪 U 盘插好并回放、内置 ETC 激活、USB／Type-C／V2L", "都能用（U 盘最易漏）"),
            it("雷达与影像：倒车影像、360 环视、真人站车后测倒车雷达", "无黑屏畸变；激光雷达／涉水雷达按配置核对"),
            it(f"仪表与车机：{m['airbag']}、制动、三电", "无故障灯报警"),
        ]},
        {"no": "10", "title": "动态试驾 10–15km", "note": "保险生效＋临牌到手再开", "items": [
            it("关音乐走粗糙路面＋减速带、触发增程器介入", "中岛无「嗒嗒」共振（异响当场录音录像）"),
            it(f"{m['drive']}：直线加速、刹车直／中踩、松手不跑偏", "动力平顺、不软塌不跑偏、无虚位抖动"),
            it("动能回收最低档、自动泊车 1 次、窄路掉头、风噪胎噪", "拖拽感能接受、无异常漏风"),
            it("空悬／底盘（若配备）两模式过坎", "滤震整、无松散异响"),
        ]},
        {"no": "11", "title": "手续 · 费用 · 签字", "note": "", "items": [
            it("发票三联／合格证原件／一致性证书／PDI 原件／三包／手册／三电质保", "全齐；合格证不接受「抵押在银行」"),
            it("钥匙清点（车主反馈标配仅卡片钥匙）、三角牌／反光背心／拖车钩／补胎工具", "当场清点登记"),
            it(f"费用核：{m['price']}、购置税（2026 减半 5%，{m['tax']}）、险约 7000–8200、上牌自办 120–200（店内约 390）", "与合同一致、无附加费"),
            it("保险精确到分钟当日生效、临牌办妥、赠品与充电桩线缆写进合同盖章、一对一讲解讲完", "全部满足再签字"),
        ]},
    ]


INTEL_COMMON = (
    "11/3 车质网 1817363：N90 Max 右后悬架全铝 H 臂打磨痕迹，交车未告知 → 必举升对比。"
    "11/5 车质网 1818917、11/6 汽车投诉网 QT347904：香氛机断联／供电触点不良，拆修后引发中岛震动 → 提车前发现。"
    "10/21、10/27 社区：中岛共振异响、电动门偶发打不开，官方暂无批次整改说明。"
    "11/9 澎程单月交付 27,132 台（N90 12,587 台），首批车装配一致性建议多查。截至 11/10 未见官方召回公告。"
)

TAG_HTML = {"hi": '<span class="tag hi">重点</span>',
            "mid": '<span class="tag mid">易漏</span>',
            "info": '<span class="tag info">设计确认</span>'}


def render_items(items):
    out = []
    for text, ok, tag in items:
        t = TAG_HTML.get(tag, "")
        out.append(
            '<label class="li"><input type="checkbox"><span>'
            + text + t + ' <span class="s">→ ' + ok + '</span></span></label>'
        )
    return "\n".join(out)


def render_sections(sections):
    out = []
    for s in sections:
        star = ' star' if s.get("star") else ''
        note = f'<em>{s["note"]}</em>' if s.get("note") else ''
        out.append(
            f'<div class="blk{star}"><h2>{s["no"]}　{s["title"]}{note}</h2>\n'
            + render_items(s["items"]) + '\n</div>'
        )
    return "\n".join(out)


def render_card(m):
    sections = (common_sections(m)[:6] + SPECIAL[m["id"]]
                + tail_sections(m))
    left = sections[:6]
    right = sections[6:]
    cond = "".join(
        f'<i>{html.escape(c)}</i>' for c in m["cond"]
    )
    chips = [s["no"] + " " + s["title"].split(" ")[0][:6] for s in sections]
    intel = (f'<b>本周情报（决定上面几个「重点」）</b><br>{INTEL_COMMON}<br>'
             f'{html.escape(m["modelnote"])} 以上车主反馈为个案、非批次质量结论；'
             '里程／SOH／漆膜等数值为通用或媒体经验值，最终以小米官方 PDI 报告与随车文件为准。')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{m['full']} 提车现场速查卡 · 2026-11-14</title>
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="bar no-print">
  <div class="bar-top">
    <span class="tip">现场速查卡 · 勾选自动保存在本机<span class="tip-extra"> · 电脑可打印一张 A4</span></span>
    <b class="prog" id="prog">已确认 0 / 0</b>
    <div class="bar-btns">
      <button onclick="window.print()">打印 / 存 PDF</button>
      <button id="hideDone">隐藏已勾</button>
      <button id="reset">重置</button>
    </div>
  </div>
  <div class="pbar"><i id="fill"></i></div>
  <nav class="jump" id="jump" aria-label="分区快捷跳转"></nav>
</div>

<div class="page">
  <a class="back" href="../index.html">← 切换车型</a>
  <div class="hd">
    <h1>{m['full']} 提车现场速查卡</h1>
    <div class="date">2026-11-14（周六）<br>预留 60–90 分钟 · 带 1 位同伴</div>
  </div>

  <div class="cond"><b>适用</b>{cond}<i>排产新车（非现车／非准新车）</i><i>已剔除不适用车型项</i></div>
  <p class="modelnote">{html.escape(m['modelnote'])}</p>

  <div class="redline">
    先验后签 · 不签空白 PDI／交车单 · 不先付尾款再看车 · 坚持室外自然光验漆 · 全程录像 · 问题写进交付单，不接受「回去 OTA 升级就好」· VIN 不符／补漆未告知／里程异常／底盘打磨托底／证件不齐 → 可拒绝签收谈换车
  </div>

  <div class="cols">
    <div class="col">
{render_sections(left)}
    </div>
    <div class="col">
{render_sections(right)}
      <div class="intel">{intel}</div>
    </div>
  </div>

  <div class="ft">
    <span>图片与数据来自小米汽车官网及公开车主反馈，仅作识别与验车参考 · 详细版 55 项清单见工作区</span>
    <span>编制 2026-11-10 · 问题记录：______________________________</span>
  </div>
</div>

<script>
(function(){{
  var MODEL='{m["id"]}', KEY='check_'+MODEL+'_v1';
  var S = window.AndroidStore ? {{
    load:function(k){{return window.AndroidStore.load(k)||'';}},
    save:function(k,v){{window.AndroidStore.save(k,v);}},
    last:function(){{return window.AndroidStore.last()||'';}},
    setLast:function(id){{window.AndroidStore.setLast(id);}}
  }} : {{
    load:function(k){{return localStorage.getItem(k)||'';}},
    save:function(k,v){{localStorage.setItem(k,v);}},
    last:function(){{return localStorage.getItem('last_model')||'';}},
    setLast:function(id){{localStorage.setItem('last_model',id);}}
  }};
  try{{S.setLast(MODEL);}}catch(e){{}}

  var boxes=Array.prototype.slice.call(document.querySelectorAll('.li input'));
  var blks=Array.prototype.slice.call(document.querySelectorAll('.blk'));
  var prog=document.getElementById('prog'), fill=document.getElementById('fill');
  var hideBtn=document.getElementById('hideDone'), jump=document.getElementById('jump');
  var st={{}}; try{{st=JSON.parse(S.load(KEY)||'{{}}');}}catch(e){{st={{}};}}

  function paint(){{
    var n=0;
    boxes.forEach(function(b){{b.closest('.li').classList.toggle('done',b.checked);if(b.checked)n++;}});
    prog.textContent='已确认 '+n+' / '+boxes.length;
    fill.style.width=(boxes.length?(n/boxes.length*100):0)+'%';
  }}
  function save(){{
    var o={{}}; boxes.forEach(function(b,i){{o[i]=b.checked;}});
    o.hide=document.body.classList.contains('hidecompleted');
    try{{S.save(KEY,JSON.stringify(o));}}catch(e){{}}
  }}
  function setHide(on){{
    document.body.classList.toggle('hidecompleted',on);
    hideBtn.textContent=on?'显示已勾':'隐藏已勾';
  }}
  boxes.forEach(function(b,i){{
    if(st[i])b.checked=true;
    b.addEventListener('change',function(){{paint();save();}});
  }});
  setHide(!!st.hide);

  var names={chips!r};
  blks.forEach(function(el,i){{
    el.id='blk'+i;
    var a=document.createElement('a');
    a.href='#blk'+i; a.textContent=names[i]||String(i+1);
    a.addEventListener('click',function(e){{
      e.preventDefault();
      el.scrollIntoView({{behavior:'smooth',block:'start'}});
      Array.prototype.forEach.call(jump.children,function(x){{x.classList.remove('on');}});
      a.classList.add('on');
    }});
    jump.appendChild(a);
  }});
  hideBtn.addEventListener('click',function(){{
    setHide(!document.body.classList.contains('hidecompleted')); save();
  }});
  document.getElementById('reset').addEventListener('click',function(){{
    if(!confirm('清空本车型全部勾选？'))return;
    boxes.forEach(function(b){{b.checked=false;}});
    setHide(false);
    try{{S.save(KEY,'{{}}');}}catch(e){{}}
    paint();
  }});
  paint();
}})();
</script>
</body>
</html>
"""


def render_index(models):
    cards = []
    for m in models:
        specs = "".join(f'<span>{html.escape(s)}</span>' for s in m["specs"])
        cards.append(f"""  <a class="model" href="cards/{m['id']}.html" data-id="{m['id']}">
    <div class="pic"><img src="img/{m['img']}" alt="{m['full']}"></div>
    <div class="info">
      <div class="row1"><b>{m['full']}</b><i>{m['price']}</i></div>
      <p>{m['tagline']}</p>
      <div class="specs">{specs}</div>
      <div class="go">进入验车清单 <span>→</span></div>
    </div>
  </a>""")
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>小米澎程提车速查卡 · 选车型</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#f2f5f8;color:#1c2128;font:15px/1.6 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:18px 14px 40px}
header{background:#fff;border:1px solid #e3e8ee;border-radius:14px;padding:18px 20px;margin-bottom:14px}
h1{margin:0 0 6px;font-size:22px}
.sub{color:#5a6572;font-size:13px;margin:0}
.warn{margin-top:12px;background:#fdf0ef;border-left:3px solid #c8362f;color:#8d2520;padding:9px 12px;border-radius:6px;font-size:13px;font-weight:700}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.model{display:block;background:#fff;border:1px solid #e3e8ee;border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;transition:.15s}
.model:hover{border-color:#9fb4cc;transform:translateY(-2px);box-shadow:0 6px 18px rgba(28,33,40,.08)}
.model.last{border-color:#1f7a52;box-shadow:0 0 0 2px rgba(31,122,82,.12)}
.pic{aspect-ratio:16/9;background:#eef1f4;overflow:hidden}
.pic img{width:100%;height:100%;object-fit:cover;display:block}
.info{padding:12px 14px 14px}
.row1{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.row1 b{font-size:16px}
.row1 i{font-style:normal;color:#c8362f;font-weight:700;font-size:14px;white-space:nowrap}
.info p{margin:3px 0 9px;color:#5a6572;font-size:13px}
.specs{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:11px}
.specs span{font-size:11px;background:#eef2f7;color:#44505e;border-radius:4px;padding:3px 7px}
.go{background:#1c2128;color:#fff;border-radius:8px;padding:9px 12px;font-size:13px;font-weight:600;display:flex;justify-content:space-between}
.model.last .go{background:#1f7a52}
.tag-last{display:inline-block;margin-left:7px;font-size:10px;background:#e7f4ec;color:#1f7a52;border-radius:4px;padding:1px 6px;vertical-align:2px}
footer{margin-top:16px;padding:13px 16px;background:#fff;border:1px solid #e3e8ee;border-radius:12px;font-size:12px;color:#5a6572;line-height:1.8}
footer b{color:#1c2128}
@media(max-width:680px){.wrap{padding:12px 10px 30px}.grid{grid-template-columns:1fr}h1{font-size:19px}header{padding:14px}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>小米澎程 · 提车现场速查卡</h1>
  <p class="sub">先选车型，再逐项打勾 · 2026-11-14（周六）提车现场用 · 完全离线可用</p>
  <div class="warn">先验后签：不签空白 PDI 单、不先付尾款再看车、坚持室外自然光验漆、全程录像。</div>
</header>

<div class="grid">
""" + "\n".join(cards) + """
</div>

<footer>
  <b>4 个车型 · 4 张独立清单</b>，每张约 35–45 项，按车型配置差异编写；勾选进度按车型分别保存，切换车型不会串。<br>
  <b>图片来源：</b>小米汽车官网（xiaomiev.com）车型页面公开渲染图，仅作车型识别示意，版权归原作者所有；N70 Pro 与 N70 Max 外观相同，用官方不同角度／配色图区分。<br>
  <b>数据口径：</b>配置与价格来自 2026 年 9 月上市公开信息及车主提车反馈；车主投诉属个案，非批次质量结论；数值标准以小米官方 PDI 报告与随车文件为准。<br>
  <b>打印：</b>在电脑浏览器打开任一车型清单，点「打印 / 存 PDF」可输出单页 A4；本选择页无需打印。
</footer>
</div>
<script>
(function(){
  var S = window.AndroidStore ? {
    last:function(){return window.AndroidStore.last()||'';},
    setLast:function(id){window.AndroidStore.setLast(id);}
  } : {
    last:function(){return localStorage.getItem('last_model')||'';},
    setLast:function(id){localStorage.setItem('last_model',id);}
  };
  var last=''; try{last=S.last();}catch(e){}
  var links=document.querySelectorAll('.model');
  Array.prototype.forEach.call(links,function(a){
    if(a.getAttribute('data-id')===last){
      a.classList.add('last');
      var t=document.createElement('span');t.className='tag-last';t.textContent='上次使用';
      a.querySelector('.row1 b').appendChild(t);
    }
    a.addEventListener('click',function(){
      try{S.setLast(a.getAttribute('data-id'));}catch(e){}
    });
  });
})();
</script>
</body>
</html>
"""


def main():
    (OUT / "cards").mkdir(parents=True, exist_ok=True)
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(render_index(MODELS), encoding="utf-8")
    for m in MODELS:
        p = OUT / "cards" / (m["id"] + ".html")
        p.write_text(render_card(m), encoding="utf-8")
        n = render_card(m).count('type="checkbox"')
        print(f"{m['name']:16s} {n:2d} 项  {p.name}")

    # 同步到 APK assets
    import shutil
    if APK_ASSETS.exists():
        shutil.rmtree(APK_ASSETS)
    shutil.copytree(OUT, APK_ASSETS)
    print("已同步到 APK assets")
    for p in sorted(APK_ASSETS.rglob("*")):
        if p.is_file():
            print("  ", p.relative_to(APK_ASSETS), p.stat().st_size)


if __name__ == "__main__":
    main()
