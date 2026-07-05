const { getHomeData, likePoem, unlikePoem, sharePoem } = require('../../services/poem')
const { addFavorite, removeFavorite } = require('../../services/user')
const { navigateTo } = require('../../utils/route')
const { showToast } = require('../../utils/toast')

const fallbackPoem = {
  id: 1,
  title: '独坐敬亭山',
  dynasty: '唐',
  author: '李白',
  content: '众鸟高飞尽，孤云独去闲。相看两不厌，只有敬亭山。',
  recommend_sentence: '相看两不厌，只有敬亭山。',
  is_favorite: false,
  is_liked: false,
  like_count: 128,
  favorite_count: 36,
  share_count: 18
}

function toLineItems(lines) {
  return lines.map((text, index) => ({
    key: `${index}-${text}`,
    text
  }))
}

function getFallbackSentence(poem) {
  const sentence = String(poem && poem.recommend_sentence ? poem.recommend_sentence : '').trim()

  if (sentence) {
    return sentence
  }

  const matched = String((poem && poem.content) || fallbackPoem.content).match(/[^。！？]+[。！？]/)
  return matched ? matched[0] : fallbackPoem.recommend_sentence
}

function splitPoemSentences(source) {
  const lines = []

  source
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .split(/\n+/)
    .forEach((paragraph) => {
      const text = paragraph.replace(/\s+/g, '').trim()

      if (!text) {
        return
      }

      const matches = text.match(/[^，。！？；,.!?;]+[，。！？；,.!?;]?/g)
      lines.push(...(matches || [text]).map((item) => item.trim()).filter(Boolean))
    })

  return lines
}

function isFixedLengthPoemLine(line) {
  const text = line.replace(/[，。！？；,.!?;\s]/g, '')
  return text.length === 5 || text.length === 7
}

function getPoemContentLines(poem) {
  const source = String(
    (poem && poem.content) ||
    (poem && poem.recommend_sentence) ||
    fallbackPoem.content
  ).trim()

  if (!source) {
    return []
  }

  const sentenceLines = splitPoemSentences(source)

  if (sentenceLines.length >= 4 && sentenceLines.every(isFixedLengthPoemLine)) {
    return sentenceLines
  }

  return [source.replace(/\s+/g, '')]
}

function formatPoemLines(poem) {
  const poemLines = getPoemContentLines(poem)

  if (poemLines.length) {
    return toLineItems(poemLines)
  }

  return toLineItems([getFallbackSentence(poem)])
}

Page({
  data: {
    loading: false,
    homeData: null,
    poemList: [fallbackPoem],
    currentPoemIndex: 0,
    currentPoem: fallbackPoem,
    recommendSentence: fallbackPoem.recommend_sentence,
    poemDisplayLines: formatPoemLines(fallbackPoem),
    isLiked: false,
    isFavorite: false,
    likeCount: fallbackPoem.like_count,
    favoriteCount: fallbackPoem.favorite_count,
    shareCount: fallbackPoem.share_count,
    statusBarHeight: 0,
    navHeight: 88,
    navTop: 24,
    navBarHeight: 32,
    navRightInset: 110,
    hasMultiplePoems: false,
    touchStartX: 0,
    touchStartY: 0,
    ignoreNextPoemTap: false,
    isSwitchingPoem: false,
    poemTransitionClass: ''
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

  onUnload() {
    clearTimeout(this.poemSwitchTimer)
    clearTimeout(this.poemEnterTimer)
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
        const poemList = this.normalizePoemList(data, poem)
        const currentPoemIndex = Math.max(0, poemList.findIndex((item) => String(item.id) === String(poem.id)))
        const currentPoem = poemList[currentPoemIndex] || poem
        this.setData({
          homeData: data,
          poemList,
          currentPoemIndex,
          hasMultiplePoems: poemList.length > 1
        })
        this.applyCurrentPoem(currentPoem)
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

  getRecommendSentence(poem) {
    return getFallbackSentence(poem)
  },

  normalizeCount(value, fallbackValue) {
    const count = Number(value)
    return Number.isFinite(count) && count >= 0 ? count : fallbackValue
  },

  normalizePoemList(data, currentPoem) {
    const source = []

    if (currentPoem) {
      source.push(currentPoem)
    }

    if (Array.isArray(data.recommend_poems)) {
      source.push(...data.recommend_poems)
    }

    const seen = {}
    const list = source.filter((poem) => {
      if (!poem || poem.id === undefined || poem.id === null) {
        return false
      }

      const key = String(poem.id)
      if (seen[key]) {
        return false
      }

      seen[key] = true
      return true
    })

    return list.length ? list : [fallbackPoem]
  },

  applyCurrentPoem(poem) {
    const currentPoem = poem || fallbackPoem
    this.setData({
      currentPoem,
      recommendSentence: this.getRecommendSentence(currentPoem),
      poemDisplayLines: formatPoemLines(currentPoem),
      isLiked: Boolean(currentPoem.is_liked),
      isFavorite: Boolean(currentPoem.is_favorite),
      likeCount: this.normalizeCount(currentPoem.like_count, fallbackPoem.like_count),
      favoriteCount: this.normalizeCount(currentPoem.favorite_count, fallbackPoem.favorite_count),
      shareCount: this.normalizeCount(currentPoem.share_count, fallbackPoem.share_count)
    })
  },

  updateCurrentPoem(patch) {
    const poemList = this.data.poemList.slice()
    const currentPoemIndex = this.data.currentPoemIndex
    const currentPoem = Object.assign({}, poemList[currentPoemIndex] || this.data.currentPoem, patch)

    poemList[currentPoemIndex] = currentPoem
    this.setData({
      poemList,
      currentPoem
    })
  },

  applyPoemActionResult(result = {}, fallbackPatch = {}) {
    const patch = Object.assign({}, fallbackPatch)

    if (result.is_liked !== undefined) {
      patch.is_liked = Boolean(result.is_liked)
    }

    if (result.is_favorite !== undefined) {
      patch.is_favorite = Boolean(result.is_favorite)
    }

    if (result.like_count !== undefined) {
      patch.like_count = this.normalizeCount(result.like_count, this.data.likeCount)
    }

    if (result.favorite_count !== undefined) {
      patch.favorite_count = this.normalizeCount(result.favorite_count, this.data.favoriteCount)
    }

    if (result.share_count !== undefined) {
      patch.share_count = this.normalizeCount(result.share_count, this.data.shareCount)
    }

    this.updateCurrentPoem(patch)
    this.setData({
      isLiked: Boolean(patch.is_liked !== undefined ? patch.is_liked : this.data.isLiked),
      isFavorite: Boolean(patch.is_favorite !== undefined ? patch.is_favorite : this.data.isFavorite),
      likeCount: this.normalizeCount(patch.like_count, this.data.likeCount),
      favoriteCount: this.normalizeCount(patch.favorite_count, this.data.favoriteCount),
      shareCount: this.normalizeCount(patch.share_count, this.data.shareCount)
    })
  },

  switchPoem(offset) {
    const poemList = this.data.poemList

    if (!Array.isArray(poemList) || poemList.length <= 1 || this.data.isSwitchingPoem) {
      return false
    }

    const nextIndex = (this.data.currentPoemIndex + offset + poemList.length) % poemList.length
    const exitClass = offset > 0 ? 'poem-content--exit-left' : 'poem-content--exit-right'
    const enterClass = offset > 0 ? 'poem-content--enter-right' : 'poem-content--enter-left'

    clearTimeout(this.poemSwitchTimer)
    clearTimeout(this.poemEnterTimer)

    this.setData({
      isSwitchingPoem: true,
      poemTransitionClass: exitClass
    })

    this.poemSwitchTimer = setTimeout(() => {
      this.setData({
        currentPoemIndex: nextIndex,
        poemTransitionClass: enterClass
      })
      this.applyCurrentPoem(poemList[nextIndex])

      this.poemEnterTimer = setTimeout(() => {
        this.setData({
          isSwitchingPoem: false,
          poemTransitionClass: ''
        })
      }, 40)
    }, 170)

    return true
  },

  handlePoemTouchStart(event) {
    const touch = event.touches && event.touches[0]

    if (!touch) {
      return
    }

    this.setData({
      touchStartX: touch.clientX,
      touchStartY: touch.clientY
    })
  },

  handlePoemTouchEnd(event) {
    const touch = event.changedTouches && event.changedTouches[0]

    if (!touch) {
      return
    }

    const deltaX = touch.clientX - this.data.touchStartX
    const deltaY = touch.clientY - this.data.touchStartY

    if (Math.abs(deltaX) < 48 || Math.abs(deltaX) < Math.abs(deltaY) * 1.2) {
      return
    }

    if (this.switchPoem(deltaX > 0 ? -1 : 1)) {
      this.setData({ ignoreNextPoemTap: true })
    }
  },

  openMenu() {
    showToast('菜单开发中')
  },

  toggleLike() {
    const nextLiked = !this.data.isLiked
    const likeCount = Math.max(0, this.data.likeCount + (nextLiked ? 1 : -1))
    const rollback = {
      is_liked: this.data.isLiked,
      like_count: this.data.likeCount
    }
    const action = nextLiked ? likePoem : unlikePoem

    this.setData({
      isLiked: nextLiked,
      likeCount
    })
    this.updateCurrentPoem({
      is_liked: nextLiked,
      like_count: likeCount
    })

    action(this.data.currentPoem.id)
      .then((result) => {
        this.applyPoemActionResult(result, {
          is_liked: nextLiked,
          like_count: likeCount
        })
      })
      .catch(() => {
        this.applyPoemActionResult({}, rollback)
        showToast('点赞接口暂不可用')
      })
  },

  toggleFavorite() {
    const nextFavorite = !this.data.isFavorite
    const favoriteCount = Math.max(0, this.data.favoriteCount + (nextFavorite ? 1 : -1))
    const action = nextFavorite ? addFavorite : removeFavorite

    this.setData({
      isFavorite: nextFavorite,
      favoriteCount
    })
    this.updateCurrentPoem({
      is_favorite: nextFavorite,
      favorite_count: favoriteCount
    })

    action(this.data.currentPoem.id)
      .then((result) => {
        this.applyPoemActionResult(result, {
          is_favorite: nextFavorite,
          favorite_count: favoriteCount
        })
        showToast(nextFavorite ? '已收藏' : '已取消', 'success')
      })
      .catch(() => {
        const rollbackFavorite = !nextFavorite
        const rollbackCount = Math.max(0, favoriteCount + (rollbackFavorite ? 1 : -1))
        this.setData({
          isFavorite: rollbackFavorite,
          favoriteCount: rollbackCount
        })
        this.updateCurrentPoem({
          is_favorite: rollbackFavorite,
          favorite_count: rollbackCount
        })
        showToast('收藏接口暂不可用')
      })
  },

  handleShareTap() {
    const shareCount = this.data.shareCount + 1
    const rollbackCount = this.data.shareCount
    this.setData({
      shareCount
    })
    this.updateCurrentPoem({
      share_count: shareCount
    })

    sharePoem(this.data.currentPoem.id)
      .then((result) => {
        this.applyPoemActionResult(result, {
          share_count: shareCount
        })
      })
      .catch(() => {
        this.setData({
          shareCount: rollbackCount
        })
        this.updateCurrentPoem({
          share_count: rollbackCount
        })
        showToast('分享计数暂不可用')
      })
  },

  goPoemDetail() {
    if (this.data.ignoreNextPoemTap) {
      this.setData({ ignoreNextPoemTap: false })
      return
    }

    navigateTo(`/pages/poem-detail/poem-detail?id=${this.data.currentPoem.id}`)
  }
})
