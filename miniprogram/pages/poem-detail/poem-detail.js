const { getPoemDetail } = require('../../services/poem')
const { addFavorite, removeFavorite } = require('../../services/user')
const { showToast } = require('../../utils/toast')
const { navigateBack } = require('../../utils/route')

const fallbackPoem = {
  id: 1,
  title: '饮酒·其五',
  dynasty: '东晋',
  author: '陶渊明',
  content: '结庐在人境，而无车马喧。问君何能尔？心远地自偏。采菊东篱下，悠然见南山。山气日夕佳，飞鸟相与还。此中有真意，欲辨已忘言。',
  tags: ['田园', '隐逸', '东晋'],
  is_favorite: false,
  is_liked: false,
  like_count: 128,
  favorite_count: 64,
  share_count: 32
}

Page({
  data: {
    poemId: '',
    poem: fallbackPoem,
    poemLines: [],
    isFavorite: false,
    isLiked: false,
    isVertical: false,
    likeCount: 0,
    favoriteCount: 0,
    shareCount: 0,
    contentTop: 112,
    comments: [
      {
        short: '墨',
        name: '墨客潇湘',
        time: '2小时前',
        content: '此诗意境深远，每次读来都有新感悟。特别是“采菊东篱下”一句，那种浑然天成的悠然，非大智慧不能为之。'
      },
      {
        short: '南',
        name: '南山悠悠',
        time: '5小时前',
        content: '陶公的淡泊名利令人向往，在这喧嚣尘世中，唯有守住内心的安宁，方能心远地自偏。'
      }
    ]
  },

  onLoad(options) {
    const poemId = options.id || '1'
    this.setPoemState(fallbackPoem, { poemId })
    this.loadPoemDetail(poemId)
  },

  onShareAppMessage() {
    return {
      title: `${this.data.poem.title} · ${this.data.poem.author}`,
      path: `/pages/poem-detail/poem-detail?id=${this.data.poemId}`
    }
  },

  /**
   * 加载诗词详情。
   * mock 模式下会直接返回本地诗词；后端接入后保持同一数据结构即可。
   */
  loadPoemDetail(poemId) {
    return getPoemDetail(poemId)
      .then((data) => {
        this.setPoemState(data || fallbackPoem)
      })
      .catch(() => {
        this.setPoemState(fallbackPoem)
      })
  },

  setPoemState(poem, extra = {}) {
    this.setData(Object.assign({
      poem,
      poemLines: this.splitPoemLines(poem.content),
      isFavorite: Boolean(poem.is_favorite),
      isLiked: Boolean(poem.is_liked),
      likeCount: poem.like_count || 0,
      favoriteCount: poem.favorite_count || 0,
      shareCount: poem.share_count || 0
    }, extra))
  },

  toggleLike() {
    const nextLiked = !this.data.isLiked
    const nextCount = this.data.likeCount + (nextLiked ? 1 : -1)

    this.setData({
      isLiked: nextLiked,
      likeCount: Math.max(0, nextCount)
    })
  },

  toggleFavorite() {
    const action = this.data.isFavorite ? removeFavorite : addFavorite
    const nextFavorite = !this.data.isFavorite

    action(this.data.poemId)
      .then(() => {
        this.setData({
          isFavorite: nextFavorite,
          favoriteCount: Math.max(0, this.data.favoriteCount + (nextFavorite ? 1 : -1))
        })
        showToast(nextFavorite ? '已收藏' : '已取消', 'success')
      })
      .catch(() => {
        showToast('收藏接口暂不可用')
      })
  },

  /**
   * 按句号、问号、叹号拆分诗句，保持一行一句的阅读节奏。
   */
  splitPoemLines(content) {
    return String(content || '').match(/[^。！？]+[。！？]/g) || []
  },

  goBack() {
    navigateBack()
  },

  handleNavReady(event) {
    const navHeight = event.detail.navHeight || 96

    this.setData({
      contentTop: navHeight + 8
    })
  },

  toggleLayout() {
    this.setData({
      isVertical: !this.data.isVertical
    })
  },

  writeNote() {
    showToast('写笔记开发中')
  }
})
