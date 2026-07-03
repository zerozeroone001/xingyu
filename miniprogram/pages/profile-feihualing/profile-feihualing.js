const { getMyRooms } = require('../../services/feihualing')
const { navigateTo } = require('../../utils/route')
const { showToast } = require('../../utils/toast')

Page({
  data: {
    loading: false,
    rooms: []
  },

  onLoad() {
    this.loadRooms()
  },

  onPullDownRefresh() {
    this.loadRooms().finally(() => {
      wx.stopPullDownRefresh()
    })
  },

  loadRooms() {
    this.setData({ loading: true })

    return getMyRooms({ page: 1, page_size: 50 })
      .then((data) => {
        this.setData({
          rooms: data.items || data || []
        })
      })
      .catch(() => {
        showToast('飞花令对局暂不可用')
      })
      .finally(() => {
        this.setData({ loading: false })
      })
  },

  openRoom(event) {
    const roomId = event.currentTarget.dataset.id

    navigateTo(`/pages/feihualing/feihualing?roomId=${roomId}`)
  }
})
