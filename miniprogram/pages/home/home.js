const { getHomeData } = require('../../services/poem')
const { navigateTo } = require('../../utils/route')
const { showToast } = require('../../utils/toast')

const fallbackPoem = {
  id: 1,
  title: '独坐敬亭山',
  dynasty: '唐',
  author: '李白',
  content: '众鸟高飞尽，孤云独去闲。相看两不厌，只有敬亭山。',
  is_favorite: false,
  is_liked: false,
  like_count: 128,
  favorite_count: 36,
  share_count: 18
}

Page({
  data: {
    loading: false,
    homeData: null,
    currentPoem: fallbackPoem,
    poemLines: ['众鸟高飞尽，', '孤云独去闲。', '相看两不厌，', '只有敬亭山。'],
    isLiked: false,
    isFavorite: false,
    likeCount: fallbackPoem.like_count,
    favoriteCount: fallbackPoem.favorite_count,
    shareCount: fallbackPoem.share_count,
    statusBarHeight: 0,
    navHeight: 88,
    navTop: 24,
    navBarHeight: 32,
    navRightInset: 110
  },

  onLoad() {
    this.initLayout()
    this.loadHomeData()
  },

  onShareAppMessage() {
    return {
      title: '山水诗境 · 今日一诗',
      path: '/pages/home/home'
    }
  },

  onPullDownRefresh() {
    this.loadHomeData().finally(() => {
      wx.stopPullDownRefresh()
    })
  },

  /**
   * 加载首页聚合数据。
   * 当前页面先显示模板复刻基线，接口接入后再把数据映射到真实组件。
   */
  loadHomeData() {
    this.setData({ loading: true })

    return getHomeData()
      .then((data) => {
        const poem = data.today_poem || fallbackPoem
        this.setData({
          homeData: data,
          currentPoem: poem,
          poemLines: this.splitPoemLines(poem.content),
          isLiked: Boolean(poem.is_liked),
          isFavorite: Boolean(poem.is_favorite),
          likeCount: this.normalizeCount(poem.like_count, fallbackPoem.like_count),
          favoriteCount: this.normalizeCount(poem.favorite_count, fallbackPoem.favorite_count),
          shareCount: this.normalizeCount(poem.share_count, fallbackPoem.share_count)
        })
      })
      .catch(() => {
        // 初始化阶段后端未启动属于正常情况，页面继续保留模板图展示。
      })
      .finally(() => {
        this.setData({ loading: false })
      })
  },

  /**
   * 初始化自定义导航需要的尺寸。
   * 胶囊按钮会因刘海屏、全面屏而变化，用它的实际位置对齐导航行并预留右侧空间。
   */
  initLayout() {
    const info = wx.getWindowInfo ? wx.getWindowInfo() : wx.getSystemInfoSync()
    const capsule = wx.getMenuButtonBoundingClientRect ? wx.getMenuButtonBoundingClientRect() : null
    const statusBarHeight = info.statusBarHeight || 0

    if (capsule && capsule.top && capsule.height) {
      const windowWidth = info.windowWidth || capsule.right || 0
      this.setData({
        statusBarHeight,
        navHeight: capsule.bottom + 8,
        navTop: capsule.top,
        navBarHeight: capsule.height,
        navRightInset: Math.max(96, windowWidth - capsule.left + 8)
      })
      return
    }

    this.setData({
      statusBarHeight,
      navHeight: statusBarHeight + 64,
      navTop: statusBarHeight + 8,
      navBarHeight: 36,
      navRightInset: 110
    })
  },

  /**
   * 将诗词正文按标点拆成四行，页面层只负责展示，不直接写死诗句内容。
   */
  splitPoemLines(content) {
    const matched = String(content || fallbackPoem.content).match(/[^，。！？]+[，。！？]/g)
    return matched || ['众鸟高飞尽，', '孤云独去闲。', '相看两不厌，', '只有敬亭山。']
  },

  normalizeCount(value, fallbackValue) {
    const count = Number(value)
    return Number.isFinite(count) && count >= 0 ? count : fallbackValue
  },

  openMenu() {
    showToast('菜单开发中')
  },

  toggleLike() {
    const nextLiked = !this.data.isLiked
    this.setData({
      isLiked: nextLiked,
      likeCount: Math.max(0, this.data.likeCount + (nextLiked ? 1 : -1))
    })
  },

  toggleFavorite() {
    const nextFavorite = !this.data.isFavorite
    this.setData({
      isFavorite: nextFavorite,
      favoriteCount: Math.max(0, this.data.favoriteCount + (nextFavorite ? 1 : -1))
    })
    showToast(this.data.isFavorite ? '已收藏' : '已取消', 'success')
  },

  handleShareTap() {
    this.setData({
      shareCount: this.data.shareCount + 1
    })
  },

  goPoemDetail() {
    navigateTo(`/pages/poem-detail/poem-detail?id=${this.data.currentPoem.id}`)
  }
})
