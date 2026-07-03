const { getProfileItems } = require('../../services/user')
const { navigateTo } = require('../../utils/route')
const { showToast } = require('../../utils/toast')

const pageConfig = {
  poems: {
    title: '我的诗作',
    intro: '发布过的诗词摘句与广场内容',
    emptyText: '还没有发布诗作'
  },
  likes: {
    title: '我的获赞',
    intro: '按点赞热度汇总的诗词与内容',
    emptyText: '暂时没有获赞内容'
  },
  favorites: {
    title: '我的收藏',
    intro: '收藏过的诗词与摘句',
    emptyText: '还没有收藏内容'
  },
  follows: {
    title: '我的关注',
    intro: '正在关注的诗友',
    emptyText: '还没有关注诗友'
  }
}

Page({
  data: {
    type: 'poems',
    title: pageConfig.poems.title,
    intro: pageConfig.poems.intro,
    emptyText: pageConfig.poems.emptyText,
    loading: false,
    items: []
  },

  onLoad(options) {
    const type = pageConfig[options.type] ? options.type : 'poems'
    const config = pageConfig[type]

    this.setData({
      type,
      title: config.title,
      intro: config.intro,
      emptyText: config.emptyText
    })

    wx.setNavigationBarTitle({
      title: config.title
    })

    this.loadItems()
  },

  onPullDownRefresh() {
    this.loadItems().finally(() => {
      wx.stopPullDownRefresh()
    })
  },

  loadItems() {
    this.setData({ loading: true })

    return getProfileItems(this.data.type, { page: 1, page_size: 50 })
      .then((data) => {
        this.setData({
          items: data.items || data || []
        })
      })
      .catch(() => {
        showToast('列表暂不可用')
      })
      .finally(() => {
        this.setData({ loading: false })
      })
  },

  openItem(event) {
    const url = event.currentTarget.dataset.url

    if (url) {
      navigateTo(url)
    }
  }
})
