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
    content: '好雨知时节，当春乃发生。随风潜入夜，润物细无声。',
    translation: '好雨似乎会挑选时节，降临在万物萌生的春天。',
    annotation: '乃：就。潜：暗暗地，悄悄地。',
    appreciation: '诗句以细腻笔触写春雨，含蓄表现诗人对生机的喜悦。',
    tags: ['春天', '写景', '唐诗'],
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
    translation: '明亮月光洒在床前，好像地上泛起一层白霜。',
    annotation: '疑：好像。举头：抬头。',
    appreciation: '全诗语言浅近，却把月夜思乡写得真切动人。',
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
    content: '空山新雨后，天气晚来秋。明月松间照，清泉石上流。',
    translation: '空旷山中刚下过一场雨，傍晚天气显出秋意。',
    annotation: '暝：日落时分，天色将晚。',
    appreciation: '诗中有画，写出雨后山林的清朗与幽静。',
    tags: ['山水', '秋天', '唐诗'],
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
    content: '大江东去，浪淘尽，千古风流人物。故垒西边，人道是，三国周郎赤壁。',
    translation: '长江滚滚东流，淘尽千古英雄人物。',
    annotation: '念奴娇：词牌名。赤壁：黄州赤壁。',
    appreciation: '全词气势开阔，把怀古、写景与人生感叹融为一体。',
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
    title: '水调歌头·明月几时有',
    dynasty: '宋',
    author: '苏轼',
    content: '明月几时有，把酒问青天。不知天上宫阙，今夕是何年。',
    translation: '明月从什么时候出现？端起酒杯遥问青天。',
    annotation: '水调歌头：词牌名。',
    appreciation: '由望月起兴，写亲情、离合与旷达胸襟。',
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
    title: '如梦令·昨夜雨疏风骤',
    dynasty: '宋',
    author: '李清照',
    content: '昨夜雨疏风骤，浓睡不消残酒。试问卷帘人，却道海棠依旧。',
    translation: '昨夜雨点稀疏而风急，沉睡醒来酒意未消。',
    annotation: '如梦令：词牌名。',
    appreciation: '短小篇幅写出惜花情思，语言清丽含蓄。',
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
    title: '声声慢·寻寻觅觅',
    dynasty: '宋',
    author: '李清照',
    content: '寻寻觅觅，冷冷清清，凄凄惨惨戚戚。乍暖还寒时候，最难将息。',
    translation: '四处寻觅，只有冷清凄凉萦绕心头。',
    annotation: '声声慢：词牌名。将息：调养休息。',
    appreciation: '叠字开篇，层层写出孤寂与愁绪。',
    recommend_sentence: '寻寻觅觅，冷冷清清，凄凄惨惨戚戚。',
    tags: ['宋词', '婉约', '愁绪'],
    is_favorite: false,
    is_liked: true,
    like_count: 221,
    favorite_count: 82,
    share_count: 29
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
