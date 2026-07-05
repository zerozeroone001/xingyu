const { getCategories } = require('../../services/category')
const { navigateTo } = require('../../utils/route')
const { showToast } = require('../../utils/toast')

const allType = '全部'

Page({
  data: {
    loading: false,
    activeType: allType,
    categories: [],
    typeTabs: [],
    categoryItems: []
  },

  onLoad() {
    this.loadCategories()
  },

  onPullDownRefresh() {
    this.loadCategories().finally(() => {
      wx.stopPullDownRefresh()
    })
  },

  loadCategories() {
    this.setData({ loading: true })

    return getCategories()
      .then((data) => {
        const categories = this.normalizeCategories(data.items || data || [])
        const typeTabs = this.buildTypeTabs(categories)
        const activeType = typeTabs[0] ? typeTabs[0].type : allType

        this.setData({
          categories,
          typeTabs,
          activeType
        })
        this.refreshCategoryItems()
      })
      .catch(() => {
        showToast('分类数据暂不可用')
      })
      .finally(() => {
        this.setData({ loading: false })
      })
  },

  normalizeCategories(categories) {
    return categories
      .slice()
      .sort((left, right) => (left.sort_order || 0) - (right.sort_order || 0))
      .map((item) => ({
        id: item.id,
        name: item.name,
        type: item.type || '其他',
        sort_order: item.sort_order || 0,
        poemCount: this.normalizeCount(item.poemCount || item.poem_count)
      }))
  },

  normalizeCount(value) {
    const count = Number(value)
    return Number.isFinite(count) && count >= 0 ? count : 0
  },

  buildTypeTabs(categories) {
    const types = [allType]

    categories.forEach((item) => {
      if (types.indexOf(item.type) < 0) {
        types.push(item.type)
      }
    })

    return types.map((type) => ({
      type,
      name: type,
      count: type === allType ? categories.length : categories.filter((item) => item.type === type).length
    }))
  },

  refreshCategoryItems() {
    const activeType = this.data.activeType
    const categoryItems = activeType === allType
      ? this.data.categories
      : this.data.categories.filter((item) => item.type === activeType)

    this.setData({ categoryItems })
  },

  changeType(event) {
    this.setData({
      activeType: event.currentTarget.dataset.type
    })
    this.refreshCategoryItems()
  },

  openCategory(event) {
    const { id, name, type } = event.currentTarget.dataset
    const query = [
      `id=${encodeURIComponent(id)}`,
      `name=${encodeURIComponent(name || '')}`,
      `type=${encodeURIComponent(type || '')}`
    ].join('&')

    navigateTo(`/pages/category-poems/category-poems?${query}`)
  }
})
