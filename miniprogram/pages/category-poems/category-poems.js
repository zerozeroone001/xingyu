const { getCategoryPoems } = require('../../services/category')
const { navigateTo } = require('../../utils/route')
const { showToast } = require('../../utils/toast')

Page({
  data: {
    loading: false,
    categoryId: '',
    categoryName: '',
    categoryType: '',
    keyword: '',
    poems: [],
    filteredPoems: []
  },

  onLoad(options) {
    const categoryId = decodeURIComponent(options.id || '')
    const categoryName = decodeURIComponent(options.name || '分类诗词')
    const categoryType = decodeURIComponent(options.type || '')

    this.setData({
      categoryId,
      categoryName,
      categoryType
    })

    wx.setNavigationBarTitle({
      title: categoryName
    })

    this.loadPoems()
  },

  onPullDownRefresh() {
    this.loadPoems().finally(() => {
      wx.stopPullDownRefresh()
    })
  },

  loadPoems() {
    const categoryId = this.data.categoryId

    if (!categoryId) {
      showToast('分类不存在')
      return Promise.resolve()
    }

    this.setData({ loading: true })

    return getCategoryPoems(categoryId, { page: 1, page_size: 50 })
      .then((data) => {
        const poems = (data.items || data || []).map((poem) => this.normalizePoem(poem))

        this.setData({ poems })
        this.applySearch()
      })
      .catch(() => {
        showToast('诗词列表暂不可用')
      })
      .finally(() => {
        this.setData({ loading: false })
      })
  },

  normalizePoem(poem) {
    return Object.assign({}, poem, {
      recommendLine: this.getRecommendLine(poem),
      likeCount: this.normalizeCount(poem.like_count),
      favoriteCount: this.normalizeCount(poem.favorite_count)
    })
  },

  getRecommendLine(poem) {
    const recommend = poem.recommend_sentence ||
      poem.recommended_sentence ||
      poem.recommend_line ||
      poem.recommended_line ||
      poem.quote ||
      poem.excerpt

    return recommend || this.getFirstTwoSentences(poem.content)
  },

  getFirstTwoSentences(content) {
    const text = String(content || '').trim()
    const sentences = text.match(/[^。！？；，,.!?;]+[。！？；，,.!?;]?/g) || []

    return sentences.slice(0, 2).join('')
  },

  normalizeCount(value) {
    const count = Number(value)

    return Number.isFinite(count) && count >= 0 ? count : 0
  },

  handleInput(event) {
    this.setData({
      keyword: event.detail.value
    })
    this.applySearch()
  },

  clearSearch() {
    this.setData({ keyword: '' })
    this.applySearch()
  },

  applySearch() {
    const keyword = String(this.data.keyword || '').trim()

    if (!keyword) {
      this.setData({
        filteredPoems: this.data.poems
      })
      return
    }

    const filteredPoems = this.data.poems.filter((poem) => {
      const tags = poem.tags || []
      const searchable = [
        poem.title,
        poem.author,
        poem.dynasty,
        poem.content,
        poem.recommendLine
      ].concat(tags).join(' ')

      return searchable.indexOf(keyword) >= 0
    })

    this.setData({ filteredPoems })
  },

  openPoem(event) {
    const poemId = event.currentTarget.dataset.id

    navigateTo(`/pages/poem-detail/poem-detail?id=${poemId}`)
  }
})
