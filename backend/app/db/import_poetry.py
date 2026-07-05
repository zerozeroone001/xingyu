from __future__ import annotations

import json
import re
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

from opencc import OpenCC
from sqlalchemy import text

from app.core.cache import cache
from app.core.config import settings
from app.db import models
from app.db.models import Base
from app.db.session import SessionLocal, engine
from app.utils.json_util import dump_json_list


TANG_URL = "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E5%85%A8%E5%94%90%E8%AF%97/%E5%94%90%E8%AF%97%E4%B8%89%E7%99%BE%E9%A6%96.json"
SONG_CI_URL = "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E5%AE%8B%E8%AF%8D/%E5%AE%8B%E8%AF%8D%E4%B8%89%E7%99%BE%E9%A6%96.json"
YUAN_QU_URL = "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E5%85%83%E6%9B%B2/yuanqu.json"
NALAN_URL = "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/%E7%BA%B3%E5%85%B0%E6%80%A7%E5%BE%B7/%E7%BA%B3%E5%85%B0%E6%80%A7%E5%BE%B7%E8%AF%97%E9%9B%86.json"

SOURCE_DIR = settings.data_dir / "sources"
TANG_SOURCE = SOURCE_DIR / "tang_300.json"
SONG_CI_SOURCE = SOURCE_DIR / "song_ci_300.json"
YUAN_QU_SOURCE = SOURCE_DIR / "yuanqu.json"
NALAN_SOURCE = SOURCE_DIR / "nalan.json"

TARGET_POEMS = 300
TARGET_CI = 200
TARGET_YUAN = 200
TARGET_MING = 30
TARGET_QING = 200

OPENCC = OpenCC("t2s")

CONTENT_TABLES = [
    models.PoemCategory.__table__,
    models.Favorite.__table__,
    models.BrowseHistory.__table__,
    models.PoemName.__table__,
    models.Category.__table__,
    models.Poem.__table__,
]

CHAR_NORMALIZATION = str.maketrans(
    {
        "牀": "床",
        "臺": "台",
        "颱": "台",
        "嶽": "岳",
        "爲": "为",
        "為": "为",
        "靜": "静",
        "後": "后",
        "裏": "里",
        "裡": "里",
        "見": "见",
        "國": "国",
        "雲": "云",
        "舊": "旧",
        "無": "无",
        "鳥": "鸟",
        "飛": "飞",
        "風": "风",
        "聲": "声",
        "時": "时",
        "長": "长",
        "門": "门",
        "問": "问",
        "萬": "万",
        "開": "开",
        "關": "关",
        "東": "东",
        "爾": "尔",
        "來": "来",
        "對": "对",
        "獨": "独",
        "盡": "尽",
        "滄": "沧",
        "邊": "边",
        "夢": "梦",
        "歸": "归",
        "憶": "忆",
        "憐": "怜",
        "淚": "泪",
        "鄉": "乡",
        "應": "应",
        "憑": "凭",
        "樓": "楼",
        "滿": "满",
        "餘": "余",
        "塵": "尘",
        "曉": "晓",
        "隱": "隐",
        "龍": "龙",
        "黃": "黄",
        "綠": "绿",
        "紅": "红",
        "盧": "卢",
        "劉": "刘",
        "蘇": "苏",
        "陳": "陈",
        "駱": "骆",
        "錢": "钱",
        "張": "张",
        "楊": "杨",
        "鄭": "郑",
        "賈": "贾",
        "韓": "韩",
        "歐": "欧",
        "陽": "阳",
        "嘆": "叹",
        "處": "处",
        "書": "书",
        "劍": "剑",
        "亂": "乱",
        "斷": "断",
        "總": "总",
        "經": "经",
        "幾": "几",
        "數": "数",
        "難": "难",
        "猶": "犹",
        "蘭": "兰",
        "葉": "叶",
        "遙": "遥",
        "銷": "销",
        "將": "将",
        "齊": "齐",
        "離": "离",
        "懷": "怀",
        "親": "亲",
        "輕": "轻",
        "傳": "传",
        "畫": "画",
        "聽": "听",
        "絕": "绝",
        "驚": "惊",
        "讓": "让",
        "隨": "随",
        "帶": "带",
        "尋": "寻",
    }
)

CLASSIC_RECOMMENDATIONS = {
    "登幽州台歌": "前不见古人，后不见来者。念天地之悠悠，独怆然而涕下。",
    "次北固山下": "海日生残夜，江春入旧年。乡书何处达？归雁洛阳边。",
    "春望": "感时花溅泪，恨别鸟惊心。烽火连三月，家书抵万金。",
    "月夜": "今夜鄜州月，闺中只独看。遥怜小儿女，未解忆长安。",
    "望岳": "会当凌绝顶，一览众山小。",
    "静夜思": "床前看月光，疑是地上霜。举头望山月，低头思故乡。",
    "黄鹤楼": "黄鹤一去不复返，白云千载空悠悠。晴川历历汉阳树，芳草萋萋鹦鹉洲。",
    "送杜少府之任蜀州": "海内存知己，天涯若比邻。无为在歧路，儿女共沾巾。",
    "登高": "无边落木萧萧下，不尽长江滚滚来。万里悲秋常作客，百年多病独登台。",
    "锦瑟": "此情可待成追忆，只是当时已惘然。",
    "无题": "身无彩凤双飞翼，心有灵犀一点通。",
    "夜雨寄北": "何当共剪西窗烛，却话巴山夜雨时。",
    "登鹳雀楼": "欲穷千里目，更上一层楼。",
    "相思": "愿君多采撷，此物最相思。",
    "竹里馆": "深林人不知，明月来相照。",
    "山居秋暝": "明月松间照，清泉石上流。竹喧归浣女，莲动下渔舟。",
    "终南别业": "行到水穷处，坐看云起时。",
    "送元二使安西": "劝君更尽一杯酒，西出阳关无故人。",
    "出塞": "秦时明月汉时关，万里长征人未还。",
    "凉州词": "羌笛何须怨杨柳，春风不度玉门关。",
    "早发白帝城": "两岸猿声啼不住，轻舟已过万重山。",
    "枫桥夜泊": "姑苏城外寒山寺，夜半钟声到客船。",
    "江雪": "孤舟蓑笠翁，独钓寒江雪。",
    "游子吟": "谁言寸草心，报得三春晖。",
    "赋得古原草送别": "野火烧不尽，春风吹又生。远芳侵古道，晴翠接荒城。",
    "虞美人": "问君能有几多愁？恰似一江春水向东流。",
    "水调歌头": "但愿人长久，千里共婵娟。",
    "念奴娇": "大江东去，浪淘尽，千古风流人物。",
    "声声慢": "梧桐更兼细雨，到黄昏、点点滴滴。",
    "一剪梅": "此情无计可消除，才下眉头，却上心头。",
    "青玉案": "众里寻他千百度。蓦然回首，那人却在，灯火阑珊处。",
    "雨霖铃": "多情自古伤离别，更那堪、冷落清秋节。",
    "鹊桥仙": "两情若是久长时，又岂在朝朝暮暮。",
    "永遇乐": "想当年，金戈铁马，气吞万里如虎。",
    "满江红": "莫等闲、白了少年头，空悲切。",
    "卜算子": "零落成泥碾作尘，只有香如故。",
}

HOT_TITLE_RANKS = {
    "静夜思": 1000,
    "登鹳雀楼": 990,
    "春晓": 980,
    "悯农": 970,
    "望庐山瀑布": 960,
    "早发白帝城": 950,
    "赠汪伦": 940,
    "黄鹤楼": 930,
    "望岳": 920,
    "春望": 910,
    "登高": 900,
    "将进酒": 890,
    "蜀道难": 880,
    "锦瑟": 870,
    "无题": 860,
    "夜雨寄北": 850,
    "相思": 840,
    "送元二使安西": 830,
    "山居秋暝": 820,
    "枫桥夜泊": 810,
    "江雪": 800,
    "游子吟": 790,
    "赋得古原草送别": 780,
    "出塞": 770,
    "凉州词": 760,
    "竹里馆": 750,
    "登幽州台歌": 740,
    "次北固山下": 730,
    "水调歌头": 1000,
    "念奴娇": 990,
    "虞美人": 980,
    "青玉案": 970,
    "声声慢": 960,
    "雨霖铃": 950,
    "鹊桥仙": 940,
    "一剪梅": 930,
    "满江红": 920,
    "永遇乐": 910,
    "卜算子": 900,
    "如梦令": 890,
    "武陵春": 880,
    "浣溪沙": 870,
    "蝶恋花": 860,
    "定风波": 850,
    "江城子": 840,
    "破阵子": 830,
    "渔家傲": 820,
    "天净沙": 810,
    "山坡羊": 800,
    "水仙子": 790,
    "折桂令": 780,
    "卖花声": 770,
    "长相思": 760,
    "浣溪沙": 750,
    "木兰花令": 740,
    "采桑子": 730,
    "桃花庵歌": 950,
    "石灰吟": 940,
    "临江仙": 930,
    "一剪梅": 920,
    "明日歌": 910,
    "今日歌": 900,
    "画鸡": 890,
    "别云间": 880,
    "马上作": 870,
    "京师得家书": 860,
}

HOT_AUTHOR_RANKS = {
    "李白": 100,
    "杜甫": 98,
    "苏轼": 96,
    "王维": 94,
    "白居易": 92,
    "李商隐": 90,
    "李清照": 88,
    "辛弃疾": 86,
    "柳永": 84,
    "陆游": 82,
    "孟浩然": 80,
    "王昌龄": 78,
    "杜牧": 76,
    "李煜": 74,
    "秦观": 72,
    "欧阳修": 70,
    "岳飞": 68,
    "王之涣": 66,
    "张若虚": 64,
    "关汉卿": 92,
    "马致远": 90,
    "白朴": 86,
    "张养浩": 84,
    "张可久": 82,
    "乔吉": 80,
    "王实甫": 78,
    "贯云石": 76,
    "纳兰性德": 96,
    "于谦": 86,
    "唐寅": 84,
    "杨慎": 82,
    "高启": 80,
    "夏完淳": 78,
    "戚继光": 76,
    "王守仁": 74,
    "刘基": 72,
    "袁凯": 70,
    "文征明": 68,
    "钱福": 66,
    "文嘉": 64,
}

GENERIC_HOT_TITLES = {
    "长相思",
    "浣溪沙",
    "一剪梅",
    "临江仙",
    "念奴娇",
    "青玉案",
    "天净沙",
    "山坡羊",
    "水仙子",
    "折桂令",
    "卖花声",
    "蝶恋花",
    "采桑子",
    "卜算子",
    "如梦令",
}

MING_ITEMS = [
    {
        "title": "石灰吟",
        "author": "于谦",
        "paragraphs": ["千锤万凿出深山，烈火焚烧若等闲。", "粉骨碎身浑不怕，要留清白在人间。"],
        "tags": ["明诗", "咏物", "励志"],
    },
    {
        "title": "咏煤炭",
        "author": "于谦",
        "paragraphs": [
            "凿开混沌得乌金，藏蓄阳和意最深。",
            "爝火燃回春浩浩，洪炉照破夜沉沉。",
            "鼎彝元赖生成力，铁石犹存死后心。",
            "但愿苍生俱饱暖，不辞辛苦出山林。",
        ],
        "tags": ["明诗", "咏物"],
    },
    {
        "title": "桃花庵歌",
        "author": "唐寅",
        "paragraphs": [
            "桃花坞里桃花庵，桃花庵下桃花仙。",
            "桃花仙人种桃树，又摘桃花换酒钱。",
            "酒醒只在花前坐，酒醉还来花下眠。",
            "半醒半醉日复日，花落花开年复年。",
            "但愿老死花酒间，不愿鞠躬车马前。",
            "车尘马足富者趣，酒盏花枝贫者缘。",
            "若将富贵比贫贱，一在平地一在天。",
            "若将贫贱比车马，他得驱驰我得闲。",
            "别人笑我太疯癫，我笑他人看不穿。",
            "不见五陵豪杰墓，无花无酒锄作田。",
        ],
        "tags": ["明诗", "桃花", "闲适"],
    },
    {
        "title": "一剪梅",
        "author": "唐寅",
        "paragraphs": [
            "雨打梨花深闭门，忘了青春，误了青春。",
            "赏心乐事共谁论？花下销魂，月下销魂。",
            "愁聚眉峰尽日颦，千点啼痕，万点啼痕。",
            "晓看天色暮看云，行也思君，坐也思君。",
        ],
        "tags": ["明词", "爱情", "相思"],
    },
    {
        "title": "画鸡",
        "author": "唐寅",
        "paragraphs": ["头上红冠不用裁，满身雪白走将来。", "平生不敢轻言语，一叫千门万户开。"],
        "tags": ["明诗", "咏物"],
    },
    {
        "title": "言志",
        "author": "唐寅",
        "paragraphs": ["不炼金丹不坐禅，不为商贾不耕田。", "闲来写就青山卖，不使人间造孽钱。"],
        "tags": ["明诗", "言志"],
    },
    {
        "title": "临江仙",
        "author": "杨慎",
        "paragraphs": [
            "滚滚长江东逝水，浪花淘尽英雄。",
            "是非成败转头空。",
            "青山依旧在，几度夕阳红。",
            "白发渔樵江渚上，惯看秋月春风。",
            "一壶浊酒喜相逢。",
            "古今多少事，都付笑谈中。",
        ],
        "tags": ["明词", "怀古", "豪放"],
    },
    {
        "title": "出郊",
        "author": "杨慎",
        "paragraphs": ["高田如楼梯，平田如棋局。", "白鹭忽飞来，点破秧针绿。"],
        "tags": ["明诗", "田园", "写景"],
    },
    {
        "title": "梅花九首其一",
        "author": "高启",
        "paragraphs": [
            "琼姿只合在瑶台，谁向江南处处栽。",
            "雪满山中高士卧，月明林下美人来。",
            "寒依疏影萧萧竹，春掩残香漠漠苔。",
            "自去何郎无好咏，东风愁寂几回开。",
        ],
        "tags": ["明诗", "咏物", "梅花"],
    },
    {
        "title": "寻胡隐君",
        "author": "高启",
        "paragraphs": ["渡水复渡水，看花还看花。", "春风江上路，不觉到君家。"],
        "tags": ["明诗", "春天", "访友"],
    },
    {
        "title": "送陈秀才还沙上省墓",
        "author": "高启",
        "paragraphs": ["满衣血泪与尘埃，乱后还乡亦可哀。", "风雨梨花寒食过，几家坟上子孙来？"],
        "tags": ["明诗", "伤怀"],
    },
    {
        "title": "别云间",
        "author": "夏完淳",
        "paragraphs": [
            "三年羁旅客，今日又南冠。",
            "无限山河泪，谁言天地宽。",
            "已知泉路近，欲别故乡难。",
            "毅魄归来日，灵旗空际看。",
        ],
        "tags": ["明诗", "爱国", "伤怀"],
    },
    {
        "title": "马上作",
        "author": "戚继光",
        "paragraphs": ["南北驱驰报主情，江花边草笑平生。", "一年三百六十日，多是横戈马上行。"],
        "tags": ["明诗", "边塞", "爱国"],
    },
    {
        "title": "望阙台",
        "author": "戚继光",
        "paragraphs": ["十年驱驰海色寒，孤臣于此望宸銮。", "繁霜尽是心头血，洒向千峰秋叶丹。"],
        "tags": ["明诗", "爱国"],
    },
    {
        "title": "拜年",
        "author": "文征明",
        "paragraphs": ["不求见面惟通谒，名纸朝来满敝庐。", "我亦随人投数纸，世情嫌简不嫌虚。"],
        "tags": ["明诗", "风俗"],
    },
    {
        "title": "泛海",
        "author": "王守仁",
        "paragraphs": ["险夷原不滞胸中，何异浮云过太空。", "夜静海涛三万里，月明飞锡下天风。"],
        "tags": ["明诗", "言志"],
    },
    {
        "title": "蔽月山房",
        "author": "王守仁",
        "paragraphs": ["山近月远觉月小，便道此山大于月。", "若人有眼大如天，当见山高月更阔。"],
        "tags": ["明诗", "哲理", "月"],
    },
    {
        "title": "秋望",
        "author": "李梦阳",
        "paragraphs": [
            "黄河水绕汉宫墙，河上秋风雁几行。",
            "客子过壕追野马，将军韬箭射天狼。",
            "黄尘古渡迷飞挽，白月横空冷战场。",
            "闻道朔方多勇略，只今谁是郭汾阳。",
        ],
        "tags": ["明诗", "边塞", "秋天"],
    },
    {
        "title": "五月十九日大雨",
        "author": "刘基",
        "paragraphs": ["风驱急雨洒高城，云压轻雷殷地声。", "雨过不知龙去处，一池草色万蛙鸣。"],
        "tags": ["明诗", "写景", "雨"],
    },
    {
        "title": "京师得家书",
        "author": "袁凯",
        "paragraphs": ["江水三千里，家书十五行。", "行行无别语，只道早还乡。"],
        "tags": ["明诗", "思乡"],
    },
    {
        "title": "春草",
        "author": "杨基",
        "paragraphs": [
            "嫩绿柔香远更浓，春来无处不茸茸。",
            "六朝旧恨斜阳里，南浦新愁细雨中。",
            "近水欲迷歌扇绿，隔花偏衬舞裙红。",
            "平川十里人归晚，无数牛羊一笛风。",
        ],
        "tags": ["明诗", "春天", "咏物"],
    },
    {
        "title": "秋日杂感",
        "author": "陈子龙",
        "paragraphs": [
            "行吟坐啸独悲秋，海雾江云引暮愁。",
            "不信有天常似醉，最怜无地可埋忧。",
            "荒荒葵井多新鬼，寂寂瓜田识故侯。",
            "见说五湖供饮马，沧浪何处着渔舟。",
        ],
        "tags": ["明诗", "秋天", "伤怀"],
    },
    {
        "title": "甲辰八月辞故里",
        "author": "张煌言",
        "paragraphs": [
            "国亡家破欲何之，西子湖头有我师。",
            "日月双悬于氏墓，乾坤半壁岳家祠。",
            "惭将赤手分三席，敢为丹心借一枝。",
            "他日素车东浙路，怒涛岂必属鸱夷。",
        ],
        "tags": ["明诗", "爱国"],
    },
    {
        "title": "竹枝词",
        "author": "何景明",
        "paragraphs": ["十二峰头秋草荒，冷烟寒月过瞿塘。", "青枫江上孤舟客，不听猿啼亦断肠。"],
        "tags": ["明诗", "羁旅", "秋天"],
    },
    {
        "title": "塞上曲送元美",
        "author": "李攀龙",
        "paragraphs": ["白羽如霜出塞寒，胡烽不断接长安。", "城头一片西山月，多少征人马上看。"],
        "tags": ["明诗", "边塞", "送别"],
    },
    {
        "title": "出师讨满夷自瓜州至金陵",
        "author": "郑成功",
        "paragraphs": ["缟素临江誓灭胡，雄师十万气吞吴。", "试看天堑投鞭渡，不信中原不姓朱。"],
        "tags": ["明诗", "爱国"],
    },
    {
        "title": "明日歌",
        "author": "钱福",
        "paragraphs": [
            "明日复明日，明日何其多。",
            "我生待明日，万事成蹉跎。",
            "世人若被明日累，春去秋来老将至。",
            "朝看水东流，暮看日西坠。",
            "百年明日能几何？请君听我明日歌。",
        ],
        "tags": ["明诗", "劝学", "哲理"],
    },
    {
        "title": "今日歌",
        "author": "文嘉",
        "paragraphs": [
            "今日复今日，今日何其少！",
            "今日又不为，此事何时了？",
            "人生百年几今日，今日不为真可惜！",
            "若言姑待明朝至，明朝又有明朝事。",
            "为君聊赋今日诗，努力请从今日始。",
        ],
        "tags": ["明诗", "劝学", "哲理"],
    },
    {
        "title": "绝句",
        "author": "刘基",
        "paragraphs": ["人生无百岁，百岁复如何？", "古来英雄士，各已归山河。"],
        "tags": ["明诗", "哲理"],
    },
    {
        "title": "岳忠武王祠",
        "author": "于谦",
        "paragraphs": ["匹马南来渡浙河，汴城宫阙远嵯峨。", "中兴诸将谁降敌，负国奸臣主议和。", "黄叶古祠寒雨积，清山荒冢白云多。", "如何一别朱仙镇，不见将军奏凯歌。"],
        "tags": ["明诗", "怀古", "爱国"],
    },
]

THEME_KEYWORDS = {
    "思乡": ["乡", "故园", "故人", "归", "家书", "客"],
    "山水": ["山", "水", "江", "河", "溪", "泉", "峰"],
    "月": ["月", "婵娟"],
    "春天": ["春", "花", "柳", "莺"],
    "秋天": ["秋", "霜", "落木"],
    "送别": ["送", "别", "离", "阳关"],
    "边塞": ["塞", "关", "胡", "羌", "沙场"],
    "怀古": ["古", "故国", "兴亡", "英雄"],
    "爱情": ["相思", "情", "郎", "红豆"],
    "咏物": ["蝉", "草", "梅", "竹", "菊", "莲"],
    "豪放": ["大江", "金戈", "万里", "英雄"],
}


def normalize_text(value: str) -> str:
    value = OPENCC.convert(value).translate(CHAR_NORMALIZATION)
    value = value.replace("，", "，").replace("。", "。")
    return re.sub(r"\s+", "", value)


def ensure_source(path: Path, url: str) -> None:
    if path.exists() and path.stat().st_size > 0 and "�" not in path.read_text(encoding="utf-8", errors="replace"):
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=45) as response:
        path.write_bytes(response.read())


def load_json(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def item_title(item: dict[str, Any], kind: str) -> str:
    title = item.get("rhythmic") if kind == "ci" and item.get("rhythmic") else item.get("title")
    return normalize_text(str(title or "").strip())


def item_content(item: dict[str, Any]) -> str:
    paragraphs = item.get("paragraphs") or item.get("para") or []
    normalized = [normalize_text(str(line).strip()) for line in paragraphs if str(line).strip()]
    return "\n".join(line for line in normalized if line)


def split_sentences(content: str) -> list[str]:
    normalized = content.replace("\n", "")
    parts = re.findall(r"[^。！？!?；;]+[。！？!?；;]?", normalized)
    return [part for part in parts if part]


def classic_recommendation(title: str, content: str) -> str | None:
    recommendation = CLASSIC_RECOMMENDATIONS.get(title)
    if recommendation is None:
        for classic_title, classic_sentence in CLASSIC_RECOMMENDATIONS.items():
            if classic_title in title:
                recommendation = classic_sentence
                break
    if recommendation and recommendation.replace("\n", "") in content.replace("\n", ""):
        return recommendation
    if recommendation and all(part in content for part in split_sentences(recommendation)[:1]):
        return recommendation
    return None


def sentence_score(sentence: str) -> int:
    score = 0
    for keyword in ["月", "春", "秋", "江", "山", "水", "花", "风", "雨", "云", "乡", "情", "梦", "酒"]:
        if keyword in sentence:
            score += 2
    if 10 <= len(sentence) <= 28:
        score += 4
    elif 6 <= len(sentence) <= 42:
        score += 2
    return score


def fallback_recommendation(content: str) -> str:
    sentences = split_sentences(content)
    if not sentences:
        return content[:80]

    best_index = max(range(len(sentences)), key=lambda index: sentence_score(sentences[index]))
    selected = [sentences[best_index]]

    if best_index + 1 < len(sentences) and len("".join(selected)) < 34:
        selected.append(sentences[best_index + 1])
    if best_index > 0 and len("".join(selected)) < 18:
        selected.insert(0, sentences[best_index - 1])

    result = "".join(selected)
    if len(result) > 90:
        result = "".join(sentences[: min(4, len(sentences))])
    return result[:100]


def recommend_sentence(title: str, content: str) -> str:
    return classic_recommendation(title, content) or fallback_recommendation(content)


def popularity_score(row: dict[str, Any], original_index: int) -> int:
    title = row["title"]
    score = 0
    title_score = 0
    for hot_title, rank in HOT_TITLE_RANKS.items():
        if hot_title == title:
            title_score = max(title_score, rank + 120)
        elif hot_title in title:
            title_score = max(title_score, rank // 5 if hot_title in GENERIC_HOT_TITLES else rank // 2)
    score += title_score
    score += HOT_AUTHOR_RANKS.get(row["author"], 0)
    score += 60 if "唐诗三百首" in row["tags"] or "宋词三百首" in row["tags"] else 0
    score += min(40, len(split_sentences(row["content"])))
    return score * 1000 - original_index


def apply_popularity_counts(row: dict[str, Any], position: int) -> None:
    score = max(1, int(row["heat_score"] / 1000))
    row["like_count"] = max(12, score + 500 - position)
    row["favorite_count"] = max(4, int(row["like_count"] * 0.42))
    row["share_count"] = max(1, int(row["like_count"] * 0.16))


def infer_tags(title: str, author: str, dynasty: str, kind_name: str, source_tags: list[str], content: str) -> list[str]:
    tags = [kind_name, dynasty, author]
    tags.extend(normalize_text(str(tag)) for tag in source_tags if str(tag).strip())
    searchable = f"{title}{content}"
    for tag, keywords in THEME_KEYWORDS.items():
        if any(keyword in searchable for keyword in keywords):
            tags.append(tag)

    result = []
    for tag in tags:
        if tag and tag not in result:
            result.append(tag)
    return result[:12]


def build_poetry_rows(
    raw_items: list[dict[str, Any]],
    count: int,
    dynasty: str,
    kind: str,
    collection_tag: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(raw_items):
        title = item_title(item, kind)
        author = normalize_text(str(item.get("author") or "").strip())
        content = item_content(item)
        if not title or not author or not content:
            continue
        source_tags = [normalize_text(str(tag)) for tag in item.get("tags") or [] if str(tag).strip()]
        if kind == "mixed":
            kind_name = "词" if any("词" in tag for tag in source_tags) else "诗"
            active_collection_tag = "明词" if kind_name == "词" else "明诗"
        else:
            kind_name = {"poem": "诗", "ci": "词", "qu": "曲"}.get(kind, "诗词")
            active_collection_tag = collection_tag
        tags = infer_tags(title, author, dynasty, active_collection_tag, source_tags, content)
        row = {
            "title": title,
            "dynasty": dynasty,
            "author": author,
            "content": content,
            "recommend_sentence": recommend_sentence(title, content),
            "tags": tags + [kind_name] if kind_name not in tags else tags,
        }
        row["heat_score"] = popularity_score(row, index)
        rows.append(row)
    if len(rows) < count:
        raise RuntimeError(f"Only found {len(rows)} valid {kind} rows, expected {count}.")
    rows.sort(key=lambda row: row["heat_score"], reverse=True)
    return rows[:count]


def reset_content_schema() -> None:
    with engine.begin() as connection:
        if engine.dialect.name == "sqlite":
            connection.execute(text("PRAGMA foreign_keys=OFF"))
        for table in CONTENT_TABLES:
            table.drop(bind=connection, checkfirst=True)
        if engine.dialect.name == "sqlite":
            connection.execute(text("PRAGMA foreign_keys=ON"))
    Base.metadata.create_all(bind=engine)


def category_specs(rows: list[dict[str, Any]]) -> list[tuple[str, str, int]]:
    specs: list[tuple[str, str, int]] = [
        ("诗", "体裁", 1),
        ("词", "体裁", 2),
        ("曲", "体裁", 3),
        ("唐诗", "体裁", 4),
        ("宋词", "体裁", 5),
        ("元曲", "体裁", 6),
        ("明诗", "体裁", 7),
        ("明词", "体裁", 8),
        ("清词", "体裁", 9),
    ]
    order = 10
    for dynasty, _ in Counter(row["dynasty"] for row in rows).most_common():
        specs.append((dynasty, "朝代", order))
        order += 1
    for author, _ in Counter(row["author"] for row in rows).most_common(24):
        specs.append((author, "作者", order))
        order += 1
    theme_counter = Counter(tag for row in rows for tag in row["tags"] if tag in THEME_KEYWORDS)
    for tag, _ in theme_counter.most_common(16):
        specs.append((tag, "主题", order))
        order += 1
    return specs


def import_rows(rows: list[dict[str, Any]]) -> None:
    with SessionLocal() as db:
        poems: list[models.Poem] = []
        for row in rows:
            poem = models.Poem(
                title=row["title"],
                dynasty=row["dynasty"],
                author=row["author"],
                content=row["content"],
                recommend_sentence=row["recommend_sentence"],
                tags=dump_json_list(row["tags"]),
                like_count=row["like_count"],
                favorite_count=row["favorite_count"],
                share_count=row["share_count"],
            )
            poems.append(poem)
            db.add(poem)
        db.flush()

        db.add_all([models.PoemName(name=poem.title) for poem in poems])

        categories = [
            models.Category(name=name, type=type_, sort_order=sort_order)
            for name, type_, sort_order in category_specs(rows)
        ]
        db.add_all(categories)
        db.flush()

        categories_by_name = {category.name: category for category in categories}
        for poem, row in zip(poems, rows, strict=True):
            linked = set(row["tags"])
            linked.add(row["dynasty"])
            linked.add(row["author"])
            for name in linked:
                category = categories_by_name.get(name)
                if category is not None:
                    db.add(models.PoemCategory(poem_id=poem.id, category_id=category.id))

        db.commit()


def main() -> None:
    ensure_source(TANG_SOURCE, TANG_URL)
    ensure_source(SONG_CI_SOURCE, SONG_CI_URL)
    ensure_source(YUAN_QU_SOURCE, YUAN_QU_URL)
    ensure_source(NALAN_SOURCE, NALAN_URL)

    poem_rows = build_poetry_rows(load_json(TANG_SOURCE), TARGET_POEMS, dynasty="唐", kind="poem", collection_tag="唐诗")
    ci_rows = build_poetry_rows(load_json(SONG_CI_SOURCE), TARGET_CI, dynasty="宋", kind="ci", collection_tag="宋词")
    yuan_rows = build_poetry_rows(load_json(YUAN_QU_SOURCE), TARGET_YUAN, dynasty="元", kind="qu", collection_tag="元曲")
    ming_rows = build_poetry_rows(MING_ITEMS, TARGET_MING, dynasty="明", kind="mixed", collection_tag="明诗")
    qing_rows = build_poetry_rows(load_json(NALAN_SOURCE), TARGET_QING, dynasty="清", kind="ci", collection_tag="清词")
    rows = poem_rows + ci_rows + yuan_rows + ming_rows + qing_rows
    rows.sort(key=lambda row: row["heat_score"], reverse=True)
    for index, row in enumerate(rows):
        apply_popularity_counts(row, index)

    reset_content_schema()
    import_rows(rows)
    for prefix in ["home:data:", "poem:detail:", "category:list", "feihualing:keywords"]:
        cache.clear_prefix(prefix)

    print(
        "Imported "
        f"{len(poem_rows)} Tang poems, {len(ci_rows)} Song ci, {len(yuan_rows)} Yuan qu, "
        f"{len(ming_rows)} Ming entries and {len(qing_rows)} Qing entries into {settings.database_url}."
    )
    print(f"Poem names inserted: {len(rows)}.")


if __name__ == "__main__":
    main()
