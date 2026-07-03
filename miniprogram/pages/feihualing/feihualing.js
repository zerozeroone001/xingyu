const { getRooms } = require('../../services/feihualing')
const { showToast } = require('../../utils/toast')

Page({
  data: {
    loading: false,
    rooms: [],
    roomCount: 0,
    watchableCount: 0,
    onlineCount: 0
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

    return getRooms()
      .then((data) => {
        const rooms = data.items || []

        this.setData({
          rooms,
          roomCount: rooms.length,
          watchableCount: rooms.filter((item) => item.canWatch).length,
          onlineCount: data.online_count || 0
        })
      })
      .catch(() => {
        showToast('对局列表暂不可用')
      })
      .finally(() => {
        this.setData({ loading: false })
      })
  },

  createRoom() {
    showToast('发起对局开发中')
  },

  enterRoom(event) {
    const roomId = event.currentTarget.dataset.id
    const room = this.data.rooms.find((item) => String(item.id) === String(roomId))

    showToast(room ? `进入「${room.title}」` : '进入对局')
  }
})
