from __future__ import annotations

import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path

from opencc import OpenCC


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "backend" / "data" / "sources"
DB_PATH = ROOT / "backend" / "data" / "app.db"
MOCK_PATH = ROOT / "miniprogram" / "services" / "mock.js"
MINIPROGRAM_OUT = ROOT / "miniprogram" / "services" / "mock_author_expansions.js"
BACKEND_OUT = ROOT / "backend" / "app" / "db" / "author_expansion.py"

TARGET_AUTHORS = [
    "李白",
    "杜甫",
    "白居易",
    "王维",
    "李清照",
    "辛弃疾",
    "陆游",
    "李商隐",
    "杜牧",
    "王昌龄",
]

ALIASES = {
    "王维": {"王维", "王維"},
    "李商隐": {"李商隐", "李商隱"},
    "辛弃疾": {"辛弃疾", "辛棄疾"},
    "陆游": {"陆游", "陸游"},
    "王昌龄": {"王昌龄", "王昌齡"},
}

PRIORITY_TITLES = {
    "李白": ["将进酒", "蜀道难", "月下独酌四首 一", "赠汪伦", "黄鹤楼送孟浩然之广陵", "行路难三首 一", "宣州谢朓楼饯别校书叔云", "渡荆门送别", "送友人", "客中行", "关山月", "峨眉山月歌", "子夜吴歌 秋歌", "闻王昌龄左迁龙标遥有此寄", "独坐敬亭山", "望天门山", "秋浦歌十七首 十五", "南陵别儿童入京", "金陵酒肆留别", "长干行二首 一"],
    "杜甫": ["望岳", "春望", "登高", "蜀相", "月夜", "春夜喜雨", "闻官军收河南河北", "旅夜书怀", "登岳阳楼", "江南逢李龟年", "绝句二首 一", "绝句二首 二", "八阵图", "江畔独步寻花七绝句 六", "赠花卿", "客至", "阁夜", "登楼", "兵车行", "佳人"],
    "白居易": ["赋得古原草送别", "钱塘湖春行", "问刘十九", "暮江吟", "大林寺桃花", "花非花", "池上二绝 一", "忆江南 三", "浪淘沙", "邯郸冬至夜思家", "观刈麦", "夜雨", "村夜", "南浦别", "放言五首 三", "遗爱寺", "卖炭翁"],
    "王维": ["鹿柴", "竹里馆", "鸟鸣涧", "相思", "送元二使安西", "使至塞上", "终南别业", "九月九日忆山东兄弟", "杂诗三首 二", "山中", "辛夷坞", "渭川田家", "过香积寺", "汉江临泛", "少年行四首 一"],
    "李清照": ["如梦令", "声声慢", "一剪梅", "醉花阴", "武陵春", "夏日绝句", "渔家傲", "凤凰台上忆吹箫", "点绛唇", "蝶恋花", "临江仙", "菩萨蛮", "减字木兰花", "清平乐", "浣溪沙"],
    "辛弃疾": ["青玉案", "破阵子", "永遇乐", "西江月", "南乡子", "丑奴儿", "清平乐", "菩萨蛮", "摸鱼儿", "水龙吟", "鹧鸪天", "贺新郎", "太常引", "生查子", "满江红"],
    "陆游": ["卜算子", "钗头凤", "诉衷情", "鹧鸪天", "夜游宫", "秋波媚", "谢池春", "好事近", "鹊桥仙", "朝中措", "浪淘沙", "浣溪沙", "渔家傲", "蝶恋花", "南乡子"],
    "李商隐": ["无题", "夜雨寄北", "嫦娥", "乐游原", "贾生", "霜月", "隋宫", "马嵬二首 二", "北青萝", "寄令狐郎中", "端居", "瑶池", "落花", "风雨", "蝉"],
    "杜牧": ["清明", "山行", "赤壁", "泊秦淮", "江南春", "秋夕", "赠别二首 一", "赠别二首 二", "遣怀", "寄扬州韩绰判官", "过华清宫绝句三首 一", "金谷园", "题乌江亭", "九日齐山登高", "旅宿"],
    "王昌龄": ["出塞二首 一", "芙蓉楼送辛渐二首 一", "从军行七首 四", "从军行七首 五", "采莲曲二首 二", "闺怨", "长信怨", "塞下曲四首 一", "送柴侍御", "同从弟南斋玩月忆山阴崔少府", "送魏二", "西宫春怨"],
}

cc = OpenCC("t2s")


def simplify(value: str) -> str:
    return cc.convert(value or "").strip()


def normalize_key(value: str) -> str:
    return re.sub(r"\s+", "", simplify(value))


def load_json(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def content_from_paragraphs(paragraphs: list[str]) -> str:
    return "".join(simplify(item).strip() for item in paragraphs if str(item).strip())


def first_sentence(content: str) -> str:
    match = re.search(r"[^。！？]+[。！？]", content)
    return match.group(0) if match else content[:28]


def infer_dynasty(author: str, kind: str) -> str:
    if kind == "ci" or author in {"李清照", "辛弃疾", "陆游"}:
        return "宋"
    return "唐"


def infer_tags(author: str, title: str, dynasty: str, kind: str, content: str) -> list[str]:
    tags = ["宋词" if kind == "ci" else f"{dynasty}诗", dynasty, author]
    searchable = f"{title}{content}"
    tag_rules = [
        ("山水", ["山", "水", "江", "溪", "湖"]),
        ("明月", ["月", "蟾", "桂魄"]),
        ("思乡", ["乡", "家", "归", "客"]),
        ("春天", ["春", "花", "柳", "莺"]),
        ("秋天", ["秋", "霜", "雁"]),
        ("送别", ["送", "别", "离"]),
        ("边塞", ["塞", "关", "军", "胡", "楼兰"]),
        ("豪放", ["剑", "弓", "沙场", "金戈", "铁马"]),
        ("婉约", ["愁", "泪", "相思", "帘"]),
        ("咏物", ["梅", "花", "柳", "荷", "蝉"]),
    ]
    for tag, words in tag_rules:
        if any(word in searchable for word in words):
            tags.append(tag)
    result = []
    for tag in tags:
        if tag not in result:
            result.append(tag)
    return result[:5]


def source_rows() -> list[dict]:
    rows: list[dict] = []
    for pattern, kind in [("poet.tang.*.json", "poem"), ("ci.song.*.json", "ci")]:
        for path in sorted(SOURCE_DIR.glob(pattern)):
            for item in load_json(path):
                author = simplify(item.get("author", ""))
                title = simplify(item.get("rhythmic") if kind == "ci" else item.get("title", ""))
                paragraphs = item.get("paragraphs") or []
                content = content_from_paragraphs(paragraphs)
                if author and title and content:
                    rows.append({"title": title, "author": author, "content": content, "kind": kind})
    return rows


def db_rows() -> list[dict]:
    rows: list[dict] = []
    con = sqlite3.connect(DB_PATH)
    try:
        for title, dynasty, author, content, recommend, tags in con.execute(
            "select title, dynasty, author, content, recommend_sentence, tags from poems"
        ):
            rows.append(
                {
                    "title": simplify(title),
                    "author": simplify(author),
                    "content": simplify(content),
                    "kind": "ci" if "词" in (tags or "") else "poem",
                    "dynasty": dynasty,
                    "recommend_sentence": recommend,
                    "tags": json.loads(tags or "[]"),
                }
            )
    finally:
        con.close()
    return rows


def existing_mock_keys() -> set[tuple[str, str]]:
    text = MOCK_PATH.read_text(encoding="utf-8")
    pattern = re.compile(r"title:\s*'([^']+)'.*?author:\s*'([^']+)'", re.S)
    return {(normalize_key(author), normalize_key(title)) for title, author in pattern.findall(text)}


def score_row(row: dict, author: str) -> tuple[int, int, str]:
    title = row["title"]
    priorities = PRIORITY_TITLES.get(author, [])
    score = 0
    for idx, hot_title in enumerate(priorities):
        if title == hot_title:
            score += 2000 - idx
        elif hot_title in title:
            score += 1200 - idx
    length = len(row["content"])
    if 20 <= length <= 220:
        score += 500
    elif length <= 360:
        score += 250
    if re.search(r"\s|□|�|\[|\]", title + row["content"]):
        score -= 800
    if re.search(r"[一二三四五六七八九十]$", title):
        score -= 20
    return (-score, length, title)


def select_rows() -> list[dict]:
    all_rows = db_rows() + source_rows()
    by_author: dict[str, list[dict]] = defaultdict(list)
    alias_to_author = {name: name for name in TARGET_AUTHORS}
    for author, aliases in ALIASES.items():
        for alias in aliases:
            alias_to_author[alias] = author

    for row in all_rows:
        author = alias_to_author.get(row["author"])
        if author:
            normalized = {**row, "author": author}
            by_author[author].append(normalized)

    existing = existing_mock_keys()
    selected: list[dict] = []
    selected_keys = set(existing)
    for author in TARGET_AUTHORS:
        candidates = sorted(by_author[author], key=lambda row: score_row(row, author))
        added = 0
        for row in candidates:
            key = (normalize_key(author), normalize_key(row["title"]))
            if key in selected_keys:
                continue
            if len(row["content"]) < 12 or len(row["content"]) > 360:
                continue
            selected_keys.add(key)
            dynasty = row.get("dynasty") or infer_dynasty(author, row["kind"])
            tags = row.get("tags") or infer_tags(author, row["title"], dynasty, row["kind"], row["content"])
            if author not in tags:
                tags.append(author)
            selected.append(
                {
                    "title": row["title"],
                    "dynasty": dynasty,
                    "author": author,
                    "content": row["content"],
                    "recommend_sentence": row.get("recommend_sentence") or first_sentence(row["content"]),
                    "tags": tags[:6],
                }
            )
            added += 1
            if added == 25:
                break
        if added < 20:
            raise RuntimeError(f"{author} only selected {added} poems")
        print(author, added)
    return selected


def js_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def write_frontend(rows: list[dict]) -> None:
    lines = ["const mockAuthorExpansionPoems = ["]
    for index, row in enumerate(rows, start=36):
        lines.extend(
            [
                "  {",
                f"    id: {index},",
                f"    title: {js_string(row['title'])},",
                f"    dynasty: {js_string(row['dynasty'])},",
                f"    author: {js_string(row['author'])},",
                f"    content: {js_string(row['content'])},",
                f"    recommend_sentence: {js_string(row['recommend_sentence'])},",
                f"    tags: {json.dumps(row['tags'], ensure_ascii=False)},",
                "    is_favorite: false,",
                "    is_liked: false,",
                f"    like_count: {80 + (index * 13) % 260},",
                f"    favorite_count: {20 + (index * 7) % 140},",
                f"    share_count: {8 + (index * 5) % 58}",
                "  },",
            ]
        )
    if rows:
        lines[-1] = "  }"
    lines.extend(["]", "", "module.exports = mockAuthorExpansionPoems", ""])
    MINIPROGRAM_OUT.write_text("\n".join(lines), encoding="utf-8")


def write_backend(rows: list[dict]) -> None:
    lines = ["from __future__ import annotations", "", "AUTHOR_EXPANSION_POEMS = ["]
    for row in rows:
        lines.extend(
            [
                "    {",
                f"        \"title\": {json.dumps(row['title'], ensure_ascii=False)},",
                f"        \"dynasty\": {json.dumps(row['dynasty'], ensure_ascii=False)},",
                f"        \"author\": {json.dumps(row['author'], ensure_ascii=False)},",
                f"        \"content\": {json.dumps(row['content'], ensure_ascii=False)},",
                f"        \"recommend_sentence\": {json.dumps(row['recommend_sentence'], ensure_ascii=False)},",
                f"        \"tags\": {json.dumps(row['tags'], ensure_ascii=False)},",
                "    },",
            ]
        )
    lines.extend(["]", ""])
    BACKEND_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = select_rows()
    write_frontend(rows)
    write_backend(rows)
    print("total", len(rows))


if __name__ == "__main__":
    main()
