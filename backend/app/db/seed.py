from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.author_expansion import AUTHOR_EXPANSION_POEMS
from app.db import models
from app.utils.json_util import dump_json_list


POEMS = [
    {
        "title": "独坐敬亭山",
        "dynasty": "唐",
        "author": "李白",
        "content": "众鸟高飞尽，孤云独去闲。相看两不厌，只有敬亭山。",
        "recommend_sentence": "相看两不厌，只有敬亭山。",
        "tags": ["山水", "孤独", "唐诗", "李白"],
    },
    {
        "title": "春夜喜雨",
        "dynasty": "唐",
        "author": "杜甫",
        "content": "好雨知时节，当春乃发生。随风潜入夜，润物细无声。",
        "recommend_sentence": "随风潜入夜，润物细无声。",
        "tags": ["春天", "写景", "唐诗", "雨"],
    },
    {
        "title": "静夜思",
        "dynasty": "唐",
        "author": "李白",
        "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
        "recommend_sentence": "举头望明月，低头思故乡。",
        "tags": ["月", "思乡", "唐诗"],
    },
    {
        "title": "山居秋暝",
        "dynasty": "唐",
        "author": "王维",
        "content": "空山新雨后，天气晚来秋。明月松间照，清泉石上流。",
        "recommend_sentence": "明月松间照，清泉石上流。",
        "tags": ["山水", "秋天", "唐诗", "王维"],
    },
    {
        "title": "水调歌头",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "明月几时有，把酒问青天。但愿人长久，千里共婵娟。",
        "recommend_sentence": "但愿人长久，千里共婵娟。",
        "tags": ["宋词", "明月", "思乡", "中秋", "苏轼"],
    },
    {
        "title": "题西林壁",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。",
        "recommend_sentence": "不识庐山真面目，只缘身在此山中。",
        "tags": ["宋诗", "哲理", "山水", "苏轼"],
    },
    {
        "title": "饮湖上初晴后雨",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "水光潋滟晴方好，山色空蒙雨亦奇。欲把西湖比西子，淡妆浓抹总相宜。",
        "recommend_sentence": "欲把西湖比西子，淡妆浓抹总相宜。",
        "tags": ["宋诗", "西湖", "写景", "山水", "苏轼"],
    },
    {
        "title": "惠崇春江晚景",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "竹外桃花三两枝，春江水暖鸭先知。蒌蒿满地芦芽短，正是河豚欲上时。",
        "recommend_sentence": "竹外桃花三两枝，春江水暖鸭先知。",
        "tags": ["宋诗", "春天", "写景", "苏轼"],
    },
    {
        "title": "浣溪沙·游蕲水清泉寺",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "山下兰芽短浸溪，松间沙路净无泥，萧萧暮雨子规啼。谁道人生无再少？门前流水尚能西！休将白发唱黄鸡。",
        "recommend_sentence": "谁道人生无再少？门前流水尚能西！",
        "tags": ["宋词", "旷达", "春天", "苏轼"],
    },
    {
        "title": "蝶恋花·春景",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "花褪残红青杏小。燕子飞时，绿水人家绕。枝上柳绵吹又少，天涯何处无芳草。",
        "recommend_sentence": "枝上柳绵吹又少，天涯何处无芳草。",
        "tags": ["宋词", "春天", "婉约", "苏轼"],
    },
    {
        "title": "江城子·密州出猎",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "老夫聊发少年狂，左牵黄，右擎苍。会挽雕弓如满月，西北望，射天狼。",
        "recommend_sentence": "会挽雕弓如满月，西北望，射天狼。",
        "tags": ["宋词", "豪放", "报国", "苏轼"],
    },
    {
        "title": "卜算子·黄州定慧院寓居作",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "缺月挂疏桐，漏断人初静。谁见幽人独往来，缥缈孤鸿影。拣尽寒枝不肯栖，寂寞沙洲冷。",
        "recommend_sentence": "拣尽寒枝不肯栖，寂寞沙洲冷。",
        "tags": ["宋词", "孤独", "咏物", "苏轼"],
    },
    {
        "title": "六月二十七日望湖楼醉书",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "黑云翻墨未遮山，白雨跳珠乱入船。卷地风来忽吹散，望湖楼下水如天。",
        "recommend_sentence": "卷地风来忽吹散，望湖楼下水如天。",
        "tags": ["宋诗", "西湖", "写景", "雨", "苏轼"],
    },
    {
        "title": "和子由渑池怀旧",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "人生到处知何似，应似飞鸿踏雪泥。泥上偶然留指爪，鸿飞那复计东西。",
        "recommend_sentence": "人生到处知何似，应似飞鸿踏雪泥。",
        "tags": ["宋诗", "人生", "怀旧", "苏轼"],
    },
    {
        "title": "海棠",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "东风袅袅泛崇光，香雾空蒙月转廊。只恐夜深花睡去，故烧高烛照红妆。",
        "recommend_sentence": "只恐夜深花睡去，故烧高烛照红妆。",
        "tags": ["宋诗", "咏物", "春天", "海棠", "苏轼"],
    },
    {
        "title": "赠刘景文",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "荷尽已无擎雨盖，菊残犹有傲霜枝。一年好景君须记，最是橙黄橘绿时。",
        "recommend_sentence": "一年好景君须记，最是橙黄橘绿时。",
        "tags": ["宋诗", "秋天", "友情", "苏轼"],
    },
    {
        "title": "望江南·超然台作",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "春未老，风细柳斜斜。试上超然台上看，半壕春水一城花。烟雨暗千家。休对故人思故国，且将新火试新茶。诗酒趁年华。",
        "recommend_sentence": "休对故人思故国，且将新火试新茶。诗酒趁年华。",
        "tags": ["宋词", "春天", "旷达", "思乡", "苏轼"],
    },
    {
        "title": "临江仙·夜饮东坡醒复醉",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "夜饮东坡醒复醉，归来仿佛三更。家童鼻息已雷鸣，敲门都不应，倚杖听江声。小舟从此逝，江海寄余生。",
        "recommend_sentence": "小舟从此逝，江海寄余生。",
        "tags": ["宋词", "旷达", "江水", "苏轼"],
    },
    {
        "title": "西江月·世事一场大梦",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "世事一场大梦，人生几度秋凉。夜来风叶已鸣廊，看取眉头鬓上。中秋谁与共孤光，把盏凄然北望。",
        "recommend_sentence": "世事一场大梦，人生几度秋凉。",
        "tags": ["宋词", "中秋", "人生", "明月", "苏轼"],
    },
    {
        "title": "水龙吟·次韵章质夫杨花词",
        "dynasty": "宋",
        "author": "苏轼",
        "content": "似花还似非花，也无人惜从教坠。春色三分，二分尘土，一分流水。细看来，不是杨花，点点是离人泪。",
        "recommend_sentence": "细看来，不是杨花，点点是离人泪。",
        "tags": ["宋词", "咏物", "离别", "春天", "苏轼"],
    },
    {
        "title": "登鹳雀楼",
        "dynasty": "唐",
        "author": "王之涣",
        "content": "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。",
        "recommend_sentence": "欲穷千里目，更上一层楼。",
        "tags": ["登高", "励志", "唐诗"],
    },
]

POEMS.extend(AUTHOR_EXPANSION_POEMS)

CATEGORIES = [
    ("唐诗", "体裁", 1),
    ("宋词", "体裁", 2),
    ("山水", "主题", 3),
    ("思乡", "主题", 4),
    ("月", "飞花令", 5),
    ("春天", "主题", 6),
    ("苏轼", "作者", 7),
    ("宋诗", "体裁", 8),
    ("豪放", "风格", 9),
    ("旷达", "主题", 10),
    ("李白", "作者", 11),
    ("杜甫", "作者", 12),
    ("白居易", "作者", 13),
    ("王维", "作者", 14),
    ("李清照", "作者", 15),
    ("辛弃疾", "作者", 16),
    ("陆游", "作者", 17),
    ("李商隐", "作者", 18),
    ("杜牧", "作者", 19),
    ("王昌龄", "作者", 20),
]


def sync_poem_names(db: Session) -> None:
    poem_titles = set(db.scalars(select(models.Poem.title)).all())
    existing_names = {item.name: item for item in db.scalars(select(models.PoemName)).all()}
    changed = False
    for title in poem_titles:
        if title not in existing_names:
            db.add(models.PoemName(name=title))
            changed = True
    for name, item in existing_names.items():
        if name not in poem_titles:
            db.delete(item)
            changed = True
    if changed:
        db.commit()


def seed_data(db: Session) -> None:
    existing = db.scalar(select(models.Poem.id).limit(1))
    if existing is not None:
        sync_poem_names(db)
        return

    users = [
        models.User(openid="mock:guest", nickname="诗词访客", avatar_text="诗", title="翰林学士", level=12, city="杭州"),
        models.User(openid="mock:lin", nickname="林深不知处", avatar_text="林", title="青衫诗客", level=8),
        models.User(openid="mock:cai", nickname="采菊东篱", avatar_text="采", title="田园诗友", level=7),
    ]
    db.add_all(users)
    db.flush()

    poems = []
    for item in POEMS:
        poem = models.Poem(**{key: value for key, value in item.items() if key != "tags"}, tags=dump_json_list(item["tags"]))
        poems.append(poem)
    db.add_all(poems)
    db.flush()
    db.add_all([models.PoemName(name=poem.title) for poem in poems])

    categories = [models.Category(name=name, type=type_, sort_order=sort_order) for name, type_, sort_order in CATEGORIES]
    db.add_all(categories)
    db.flush()

    for poem in poems:
        tags = set(item["tags"] for item in [])
        poem_tags = set()
        for source in POEMS:
            if source["title"] == poem.title:
                poem_tags = set(source["tags"])
                break
        for category in categories:
            if category.name in poem_tags or category.name == poem.dynasty:
                db.add(models.PoemCategory(poem_id=poem.id, category_id=category.id))

    topic = models.SquareTopic(
        user_id=users[1].id,
        title="雨后山色：把一句诗走成一段路",
        content="清晨沿溪上山，雾气还贴着松针。读到“空山新雨后，天气晚来秋”时，才觉得这不只是景色。",
        badge="山水",
        tags=dump_json_list(["山水", "行旅", "王维"]),
        images=dump_json_list(["/assets/images/square-01.svg", "/assets/images/square-02.svg"]),
        like_count=12,
        favorite_count=3,
    )
    db.add(topic)
    db.flush()
    db.add(models.SquareComment(topic_id=topic.id, user_id=users[2].id, content="这句配山路很合适。", like_count=2))

    room = models.FeihualingRoom(
        creator_id=users[1].id,
        title="月下雅集",
        keyword="月",
        can_watch=True,
        player_count=3,
        max_players=6,
        round_text="第 3 轮",
    )
    db.add(room)
    db.flush()
    db.add(
        models.FeihualingRoomMessage(
            room_id=room.id,
            user_id=users[1].id,
            role="opponent",
            content="床前明月光，疑是地上霜。",
            source_title="静夜思",
            source_author="李白",
            source_dynasty="唐",
        )
    )

    db.add(models.UserFollow(user_id=users[0].id, target_user_id=users[1].id))
    db.commit()
