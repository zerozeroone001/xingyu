const mockPoems = [
  {
    id: 1,
    title: '独坐敬亭山',
    dynasty: '唐',
    author: '李白',
    content: '众鸟高飞尽，孤云独去闲。相看两不厌，只有敬亭山。',
    translation: '群鸟高飞远去，孤云也独自悠闲飘走。彼此久久相看不觉厌倦，眼前只有敬亭山。',
    annotation: '敬亭山：在今安徽宣城北。闲：悠闲，安静。',
    appreciation: '诗人以山为知己，把孤独写得清远沉静，形成物我相看、心境相通的画面。',
    recommend_sentence: '相看两不厌，只有敬亭山。',
    tags: ['山水', '孤独', '唐诗'],
    is_favorite: false,
    is_liked: false,
    like_count: 128,
    favorite_count: 36,
    share_count: 18
  },
  {
    id: 2,
    title: '春夜喜雨',
    dynasty: '唐',
    author: '杜甫',
    content: '好雨知时节，当春乃发生。随风潜入夜，润物细无声。野径云俱黑，江船火独明。晓看红湿处，花重锦官城。',
    translation: '好雨似乎懂得时节，在春天万物萌发时降临。它随风潜入夜里，悄悄滋润万物。天明再看雨后花朵，锦官城里一片湿润繁盛。',
    annotation: '乃：就。潜：暗暗地，悄悄地。锦官城：成都的别称。',
    appreciation: '全诗由听觉、视觉写春雨，从夜雨无声到晓看花重，含蓄表现诗人对生机的喜悦。',
    recommend_sentence: '随风潜入夜，润物细无声。',
    tags: ['春天', '写景', '唐诗', '雨'],
    is_favorite: false,
    is_liked: false,
    like_count: 96,
    favorite_count: 24,
    share_count: 12
  },
  {
    id: 3,
    title: '静夜思',
    dynasty: '唐',
    author: '李白',
    content: '床前明月光，疑是地上霜。举头望明月，低头思故乡。',
    translation: '明亮月光洒在床前，好像地上泛起一层白霜。抬头望见天上明月，低头便思念远方故乡。',
    annotation: '疑：好像。举头：抬头。',
    appreciation: '全诗语言浅近，却把月夜思乡写得真切动人。',
    recommend_sentence: '举头望明月，低头思故乡。',
    tags: ['月', '思乡', '唐诗'],
    is_favorite: true,
    is_liked: true,
    like_count: 156,
    favorite_count: 52,
    share_count: 21
  },
  {
    id: 4,
    title: '山居秋暝',
    dynasty: '唐',
    author: '王维',
    content: '空山新雨后，天气晚来秋。明月松间照，清泉石上流。竹喧归浣女，莲动下渔舟。随意春芳歇，王孙自可留。',
    translation: '空旷山中刚下过雨，傍晚天气带着秋意。明月照在松林间，清泉流过石上。竹林喧响是浣衣女子归来，莲叶摇动是渔舟顺流而下。',
    annotation: '暝：日落时分，天色将晚。浣女：洗衣的女子。春芳歇：春草芳华消歇。',
    appreciation: '诗中有画，写出雨后山林的清朗与幽静，也寄寓诗人愿留山居的心境。',
    recommend_sentence: '明月松间照，清泉石上流。',
    tags: ['山水', '秋天', '唐诗', '王维'],
    is_favorite: false,
    is_liked: false,
    like_count: 142,
    favorite_count: 44,
    share_count: 16
  },
  {
    id: 5,
    title: '念奴娇·赤壁怀古',
    dynasty: '宋',
    author: '苏轼',
    content: '大江东去，浪淘尽，千古风流人物。故垒西边，人道是，三国周郎赤壁。乱石穿空，惊涛拍岸，卷起千堆雪。江山如画，一时多少豪杰。遥想公瑾当年，小乔初嫁了，雄姿英发。羽扇纶巾，谈笑间，樯橹灰飞烟灭。故国神游，多情应笑我，早生华发。人生如梦，一尊还酹江月。',
    translation: '长江滚滚东流，淘尽千古英雄人物。赤壁江山壮阔如画，引出对周瑜风采和历史兴亡的追怀，最终转为人生如梦的旷达感叹。',
    annotation: '念奴娇：词牌名。周郎：周瑜。樯橹：代指曹军战船。酹：以酒洒地祭奠。',
    appreciation: '全词气势开阔，把怀古、写景与人生感叹融为一体，是豪放词的代表作。',
    recommend_sentence: '大江东去，浪淘尽，千古风流人物。',
    tags: ['宋词', '豪放', '怀古', '江水'],
    is_favorite: false,
    is_liked: true,
    like_count: 238,
    favorite_count: 91,
    share_count: 35
  },
  {
    id: 6,
    title: '水调歌头',
    dynasty: '宋',
    author: '苏轼',
    content: '明月几时有，把酒问青天。不知天上宫阙，今夕是何年。我欲乘风归去，又恐琼楼玉宇，高处不胜寒。起舞弄清影，何似在人间。转朱阁，低绮户，照无眠。不应有恨，何事长向别时圆。人有悲欢离合，月有阴晴圆缺，此事古难全。但愿人长久，千里共婵娟。',
    translation: '词人对月饮酒，由天上人间写到兄弟离别，最终以“但愿人长久”化解离愁，表达豁达而深厚的祝愿。',
    annotation: '水调歌头：词牌名。琼楼玉宇：美玉砌成的楼宇，指月中宫殿。婵娟：美好的月色。',
    appreciation: '由望月起兴，写亲情、离合与旷达胸襟，情感层层转折而归于开阔。',
    recommend_sentence: '但愿人长久，千里共婵娟。',
    tags: ['宋词', '明月', '思乡', '中秋'],
    is_favorite: true,
    is_liked: true,
    like_count: 312,
    favorite_count: 126,
    share_count: 48
  },
  {
    id: 7,
    title: '如梦令',
    dynasty: '宋',
    author: '李清照',
    content: '昨夜雨疏风骤，浓睡不消残酒。试问卷帘人，却道海棠依旧。知否，知否？应是绿肥红瘦。',
    translation: '昨夜风急雨疏，沉睡醒来酒意未消。问卷帘人海棠如何，对方说依旧；词人却知道花已凋零、绿叶更盛。',
    annotation: '如梦令：词牌名。绿肥红瘦：绿叶繁茂，红花稀少。',
    appreciation: '短小篇幅写出惜花情思，语言清丽含蓄，结尾一问一答尤其传神。',
    recommend_sentence: '知否，知否？应是绿肥红瘦。',
    tags: ['宋词', '婉约', '写景', '海棠'],
    is_favorite: false,
    is_liked: false,
    like_count: 186,
    favorite_count: 73,
    share_count: 27
  },
  {
    id: 8,
    title: '声声慢',
    dynasty: '宋',
    author: '李清照',
    content: '寻寻觅觅，冷冷清清，凄凄惨惨戚戚。乍暖还寒时候，最难将息。三杯两盏淡酒，怎敌他、晚来风急。雁过也，正伤心，却是旧时相识。满地黄花堆积，憔悴损，如今有谁堪摘。守着窗儿，独自怎生得黑。梧桐更兼细雨，到黄昏、点点滴滴。这次第，怎一个愁字了得。',
    translation: '词人从寻觅无着写到冷清凄苦，淡酒、急风、过雁、黄花、细雨层层叠加，最后凝成难以言尽的愁绪。',
    annotation: '声声慢：词牌名。将息：调养休息。次第：情形，光景。',
    appreciation: '叠字开篇，层层写出孤寂与愁绪，是婉约词中极具感染力的名篇。',
    recommend_sentence: '寻寻觅觅，冷冷清清，凄凄惨惨戚戚。',
    tags: ['宋词', '婉约', '愁绪'],
    is_favorite: false,
    is_liked: true,
    like_count: 221,
    favorite_count: 82,
    share_count: 29
  },
  {
    id: 9,
    title: '登鹳雀楼',
    dynasty: '唐',
    author: '王之涣',
    content: '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。',
    translation: '夕阳依傍群山落下，黄河奔流入海。若想望尽更远风景，就要再登上一层楼。',
    annotation: '鹳雀楼：旧址在今山西永济。穷：尽，使达到极点。',
    appreciation: '短短二十字将壮阔景象与进取精神融为一体。',
    recommend_sentence: '欲穷千里目，更上一层楼。',
    tags: ['登高', '励志', '唐诗'],
    is_favorite: false,
    is_liked: false,
    like_count: 168,
    favorite_count: 61,
    share_count: 20
  },
  {
    id: 10,
    title: '望庐山瀑布',
    dynasty: '唐',
    author: '李白',
    content: '日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。',
    translation: '阳光照在香炉峰上升起紫色烟霞，远望瀑布像挂在山前。水流飞泻而下，好像银河从九天落下。',
    annotation: '香炉：庐山香炉峰。九天：极高的天空。',
    appreciation: '诗中夸张奇崛，写出庐山瀑布的壮丽与飞动感。',
    recommend_sentence: '飞流直下三千尺，疑是银河落九天。',
    tags: ['山水', '瀑布', '唐诗', '李白'],
    is_favorite: false,
    is_liked: true,
    like_count: 203,
    favorite_count: 80,
    share_count: 31
  },
  {
    id: 11,
    title: '早发白帝城',
    dynasty: '唐',
    author: '李白',
    content: '朝辞白帝彩云间，千里江陵一日还。两岸猿声啼不住，轻舟已过万重山。',
    translation: '清晨辞别彩云间的白帝城，一天便回到千里外的江陵。两岸猿声仍不断啼叫，轻快的小舟已穿过万重青山。',
    annotation: '白帝城：在今重庆奉节。江陵：今湖北荆州一带。',
    appreciation: '全诗节奏轻快，写出舟行三峡的速度与诗人心境的舒展。',
    recommend_sentence: '两岸猿声啼不住，轻舟已过万重山。',
    tags: ['行旅', '山水', '唐诗', '李白'],
    is_favorite: false,
    is_liked: false,
    like_count: 174,
    favorite_count: 58,
    share_count: 19
  },
  {
    id: 12,
    title: '黄鹤楼',
    dynasty: '唐',
    author: '崔颢',
    content: '昔人已乘黄鹤去，此地空余黄鹤楼。黄鹤一去不复返，白云千载空悠悠。晴川历历汉阳树，芳草萋萋鹦鹉洲。日暮乡关何处是，烟波江上使人愁。',
    translation: '昔人乘黄鹤离去，只留下黄鹤楼。晴日江对岸树木清晰，鹦鹉洲芳草茂盛；暮色中望不见故乡，江上烟波令人惆怅。',
    annotation: '晴川：晴朗的江面。历历：分明可数。乡关：故乡。',
    appreciation: '前半写传说与时间空茫，后半转入登楼所见和思乡之愁，气象高远。',
    recommend_sentence: '日暮乡关何处是，烟波江上使人愁。',
    tags: ['登楼', '思乡', '唐诗'],
    is_favorite: true,
    is_liked: false,
    like_count: 246,
    favorite_count: 104,
    share_count: 38
  },
  {
    id: 13,
    title: '锦瑟',
    dynasty: '唐',
    author: '李商隐',
    content: '锦瑟无端五十弦，一弦一柱思华年。庄生晓梦迷蝴蝶，望帝春心托杜鹃。沧海月明珠有泪，蓝田日暖玉生烟。此情可待成追忆，只是当时已惘然。',
    translation: '锦瑟的一弦一柱牵起对年华的追忆。梦蝶、杜鹃、沧海明月、蓝田暖玉交织成迷离意象，写出难以明言的怅惘。',
    annotation: '无端：没有来由。华年：美好的年华。惘然：怅然若失。',
    appreciation: '诗以繁复意象写追忆与怅惘，含蓄朦胧，余味悠长。',
    recommend_sentence: '此情可待成追忆，只是当时已惘然。',
    tags: ['爱情', '追忆', '唐诗', '李商隐'],
    is_favorite: false,
    is_liked: true,
    like_count: 275,
    favorite_count: 118,
    share_count: 43
  },
  {
    id: 14,
    title: '泊船瓜洲',
    dynasty: '宋',
    author: '王安石',
    content: '京口瓜洲一水间，钟山只隔数重山。春风又绿江南岸，明月何时照我还。',
    translation: '京口与瓜洲只隔一条江，钟山也只隔几重山。春风又吹绿江南岸，明月什么时候照着我回家。',
    annotation: '瓜洲：在今江苏扬州南。钟山：今南京紫金山。',
    appreciation: '“绿”字写活春风，也牵出诗人对故园的深切思念。',
    recommend_sentence: '春风又绿江南岸，明月何时照我还。',
    tags: ['宋诗', '思乡', '春天'],
    is_favorite: false,
    is_liked: false,
    like_count: 151,
    favorite_count: 47,
    share_count: 18
  },
  {
    id: 15,
    title: '定风波',
    dynasty: '宋',
    author: '苏轼',
    content: '莫听穿林打叶声，何妨吟啸且徐行。竹杖芒鞋轻胜马，谁怕。一蓑烟雨任平生。料峭春风吹酒醒，微冷，山头斜照却相迎。回首向来萧瑟处，归去，也无风雨也无晴。',
    translation: '途中遇雨，词人不为风雨所动，拄竹杖、穿芒鞋从容前行。回望风雨来处，最终化为“也无风雨也无晴”的豁达。',
    annotation: '定风波：词牌名。吟啸：吟咏长啸。料峭：形容微寒。',
    appreciation: '小序般的途中遭雨，被写成面对人生风雨的从容姿态。',
    recommend_sentence: '一蓑烟雨任平生。',
    tags: ['宋词', '豪放', '旷达', '风雨'],
    is_favorite: true,
    is_liked: true,
    like_count: 294,
    favorite_count: 132,
    share_count: 52
  },
  {
    id: 16,
    title: '卜算子·咏梅',
    dynasty: '宋',
    author: '陆游',
    content: '驿外断桥边，寂寞开无主。已是黄昏独自愁，更著风和雨。无意苦争春，一任群芳妒。零落成泥碾作尘，只有香如故。',
    translation: '梅花开在驿外断桥边，黄昏风雨中独自承受寂寞。它无意与百花争春，即便零落成泥，香气依旧。',
    annotation: '卜算子：词牌名。更著：又遭受。一任：任凭。',
    appreciation: '借梅花写高洁孤贞，末句“香如故”格外有力量。',
    recommend_sentence: '零落成泥碾作尘，只有香如故。',
    tags: ['宋词', '咏物', '梅花', '品格'],
    is_favorite: false,
    is_liked: true,
    like_count: 233,
    favorite_count: 97,
    share_count: 36
  },
  {
    id: 17,
    title: '江城子·乙卯正月二十日夜记梦',
    dynasty: '宋',
    author: '苏轼',
    content: '十年生死两茫茫，不思量，自难忘。千里孤坟，无处话凄凉。纵使相逢应不识，尘满面，鬓如霜。夜来幽梦忽还乡，小轩窗，正梳妆。相顾无言，惟有泪千行。料得年年肠断处，明月夜，短松冈。',
    translation: '词人梦见亡妻，十年生死相隔，纵不刻意思量也难以忘怀。梦中相见无言，醒后只余明月孤坟的深痛。',
    annotation: '江城子：词牌名。乙卯：宋神宗熙宁八年。短松冈：长着矮松的坟冈。',
    appreciation: '全词以白描写深情，哀而不饰，是悼亡词名篇。',
    recommend_sentence: '十年生死两茫茫，不思量，自难忘。',
    tags: ['宋词', '悼亡', '深情', '苏轼'],
    is_favorite: false,
    is_liked: false,
    like_count: 321,
    favorite_count: 149,
    share_count: 61
  },
  {
    id: 18,
    title: '青玉案·元夕',
    dynasty: '宋',
    author: '辛弃疾',
    content: '东风夜放花千树，更吹落，星如雨。宝马雕车香满路。凤箫声动，玉壶光转，一夜鱼龙舞。蛾儿雪柳黄金缕，笑语盈盈暗香去。众里寻他千百度，蓦然回首，那人却在，灯火阑珊处。',
    translation: '元宵夜灯火如花、车马香尘、歌舞喧腾。词人在人群中千百次寻找，回首却在灯火稀疏处见到那人。',
    annotation: '青玉案：词牌名。元夕：元宵夜。阑珊：零落稀疏。',
    appreciation: '上片写繁华热闹，下片以“灯火阑珊处”反衬清醒孤高的精神追寻。',
    recommend_sentence: '众里寻他千百度，蓦然回首，那人却在，灯火阑珊处。',
    tags: ['宋词', '元宵', '辛弃疾', '婉约'],
    is_favorite: true,
    is_liked: true,
    like_count: 356,
    favorite_count: 171,
    share_count: 66
  },
  {
    id: 19,
    title: '破阵子·为陈同甫赋壮词以寄之',
    dynasty: '宋',
    author: '辛弃疾',
    content: '醉里挑灯看剑，梦回吹角连营。八百里分麾下炙，五十弦翻塞外声。沙场秋点兵。马作的卢飞快，弓如霹雳弦惊。了却君王天下事，赢得生前身后名。可怜白发生。',
    translation: '词人醉中看剑，梦回军营，想象沙场点兵、战马飞驰、弓弦如雷，最终却以白发生的现实收束。',
    annotation: '陈同甫：陈亮。八百里：牛名，泛指牛肉。的卢：良马名。',
    appreciation: '壮怀激烈与现实失意形成强烈对照，末句沉痛有力。',
    recommend_sentence: '醉里挑灯看剑，梦回吹角连营。',
    tags: ['宋词', '豪放', '报国', '辛弃疾'],
    is_favorite: false,
    is_liked: true,
    like_count: 302,
    favorite_count: 136,
    share_count: 49
  },
  {
    id: 20,
    title: '天净沙·秋思',
    dynasty: '元',
    author: '马致远',
    content: '枯藤老树昏鸦，小桥流水人家，古道西风瘦马。夕阳西下，断肠人在天涯。',
    translation: '枯藤老树、黄昏乌鸦、小桥流水、古道西风与瘦马共同构成秋日旅途的萧瑟画面，夕阳下游子漂泊天涯。',
    annotation: '天净沙：曲牌名。断肠人：极度忧伤的人。',
    appreciation: '寥寥数语铺排意象，被称为秋思小令中的经典。',
    recommend_sentence: '夕阳西下，断肠人在天涯。',
    tags: ['元曲', '秋天', '羁旅', '思乡'],
    is_favorite: false,
    is_liked: false,
    like_count: 214,
    favorite_count: 88,
    share_count: 32
  }
]

const mockCategories = [
  { id: 1, name: '唐诗', type: '朝代', sort_order: 1 },
  { id: 2, name: '宋词', type: '体裁', sort_order: 2 },
  { id: 3, name: '写景', type: '主题', sort_order: 3 },
  { id: 4, name: '思乡', type: '主题', sort_order: 4 },
  { id: 5, name: '飞花令常用', type: '玩法', sort_order: 5 }
]

const squareImages = [
  '/assets/images/square-01.svg',
  '/assets/images/square-02.svg',
  '/assets/images/square-03.svg',
  '/assets/images/square-04.svg',
  '/assets/images/square-05.svg',
  '/assets/images/square-06.svg',
  '/assets/images/square-07.svg',
  '/assets/images/square-08.svg',
  '/assets/images/square-09.svg'
]

const mockSquareFeed = [
  {
    id: 1,
    title: '雨后山色：把一句诗走成一段路',
    content: '清晨沿溪上山，雾气还贴着松针。\n读到“空山新雨后，天气晚来秋”时，才觉得这不是景色，是王维替我们留住的一次呼吸。',
    badge: '山水',
    tags: ['山水', '行旅', '王维'],
    time: '12 分钟前',
    author: {
      nickname: '林深不知处',
      avatarText: '林',
      avatarTone: 'sage'
    },
    images: squareImages.slice(0, 9),
    likeCount: 128,
    favoriteCount: 45,
    shareCount: 18,
    isLiked: true,
    isFavorited: false,
    comments: [
      {
        id: 101,
        nickname: '云影青松',
        avatarText: '云',
        avatarTone: 'green',
        content: '九宫格很有层次，第一张山影最贴诗意。',
        time: '刚刚',
        likeCount: 12,
        favoriteCount: 3
      },
      {
        id: 102,
        nickname: '采菊东篱',
        avatarText: '采',
        avatarTone: 'warm',
        content: '“留住一次呼吸”这句配文真好。',
        time: '5 分钟前',
        likeCount: 8,
        favoriteCount: 2,
        isLiked: true
      },
      {
        id: 103,
        nickname: '墨客小张',
        avatarText: '墨',
        avatarTone: 'ink',
        content: '像一篇小游记，收藏了。',
        time: '9 分钟前',
        likeCount: 6,
        favoriteCount: 4,
        isFavorited: true
      },
      {
        id: 104,
        nickname: '夜读诗人',
        avatarText: '夜',
        avatarTone: 'rose',
        content: '下次也想按诗句去走一条路线。',
        time: '10 分钟前',
        likeCount: 4,
        favoriteCount: 1
      }
    ]
  },
  {
    id: 2,
    title: '今日摘句：心远地自偏',
    content: '午休翻到陶渊明，忽然觉得真正难的不是离开喧闹，而是在喧闹里给心留一块安静的地方。',
    badge: '摘句',
    tags: ['摘句', '田园', '陶渊明'],
    time: '38 分钟前',
    author: {
      nickname: '采菊东篱',
      avatarText: '采',
      avatarTone: 'warm'
    },
    images: squareImages.slice(1, 5),
    likeCount: 96,
    favoriteCount: 31,
    shareCount: 12,
    isLiked: false,
    isFavorited: true,
    comments: [
      {
        id: 201,
        nickname: '溪上月',
        avatarText: '溪',
        avatarTone: 'sage',
        content: '配图有纸页和竹影，读起来很静。',
        time: '12 分钟前',
        likeCount: 5,
        favoriteCount: 1
      },
      {
        id: 202,
        nickname: '半窗灯火',
        avatarText: '灯',
        avatarTone: 'ink',
        content: '这句适合放在书桌旁。',
        time: '18 分钟前',
        likeCount: 9,
        favoriteCount: 3,
        isLiked: true
      }
    ]
  },
  {
    id: 3,
    title: '飞花令热词：月',
    content: '整理了一组带“月”的句子，从李白到苏轼都能接上。今晚练习的时候，先从“床前明月光”热身。',
    badge: '飞花令',
    tags: ['飞花令', '月色', '练习'],
    time: '1 小时前',
    author: {
      nickname: '夜读诗人',
      avatarText: '夜',
      avatarTone: 'ink'
    },
    images: squareImages.slice(2, 5),
    likeCount: 156,
    favoriteCount: 64,
    shareCount: 27,
    isLiked: false,
    isFavorited: false,
    comments: [
      {
        id: 301,
        nickname: '清辉',
        avatarText: '清',
        avatarTone: 'rose',
        content: '建议下一期整理“风”，太常用了。',
        time: '26 分钟前',
        likeCount: 14,
        favoriteCount: 5
      },
      {
        id: 302,
        nickname: '松间照',
        avatarText: '松',
        avatarTone: 'green',
        content: '月主题真的很适合入门。',
        time: '31 分钟前',
        likeCount: 7,
        favoriteCount: 2
      },
      {
        id: 303,
        nickname: '一卷书',
        avatarText: '书',
        avatarTone: 'warm',
        content: '分享给同学了，晚上一起练。',
        time: '45 分钟前',
        likeCount: 11,
        favoriteCount: 2,
        isFavorited: true
      }
    ]
  }
]

const mockUser = {
  id: 1,
  nickname: '诗词访客',
  avatar_url: '',
  favorite_count: 2,
  history_count: 3,
  feihualing_count: 8
}

/**
 * 统一模拟分页结构。
 * @param {Array} items 原始列表
 * @param {number} page 当前页码
 * @param {number} pageSize 每页数量
 */
function pageResult(items, page = 1, pageSize = 10) {
  const start = (page - 1) * pageSize
  const list = items.slice(start, start + pageSize)

  return {
    items: list,
    page,
    page_size: pageSize,
    total: items.length,
    has_more: start + pageSize < items.length
  }
}

function findPoem(poemId) {
  return mockPoems.find((item) => String(item.id) === String(poemId)) || mockPoems[0]
}

module.exports = {
  mockPoems,
  mockCategories,
  mockSquareFeed,
  mockUser,
  pageResult,
  findPoem
}
