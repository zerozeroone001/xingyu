const {
  getSquareFeed,
  toggleSquareLike,
  toggleSquareFavorite,
  increaseSquareShare,
  toggleSquareCommentLike,
  toggleSquareCommentFavorite
} = require('../../services/square')
const { getKeywords, getRooms } = require('../../services/feihualing')
const { showToast } = require('../../utils/toast')
const { navigateTo } = require('../../utils/route')

function normalizeComment(comment) {
  return {
    ...comment,
    nickname: comment.nickname || comment.user_nickname || '诗友',
    avatarText: comment.avatarText || comment.avatar_text || '诗',
    avatarTone: comment.avatarTone || comment.avatar_tone || 'sage',
    content: comment.content || '',
    time: comment.time || comment.created_at || '',
    isLiked: Boolean(comment.isLiked || comment.is_liked),
    isFavorited: Boolean(comment.isFavorited || comment.is_favorited),
    likeCount: comment.likeCount || comment.like_count || 0,
    favoriteCount: comment.favoriteCount || comment.favorite_count || 0
  }
}

function normalizeTags(topic) {
  if (Array.isArray(topic.tags) && topic.tags.length) {
    return topic.tags
  }

  const tag = topic.badge || topic.tag
  return tag ? [tag] : ['话题']
}

function getTopicShareTitle(topic) {
  const content = topic && topic.content ? topic.content.replace(/\s+/g, ' ').trim() : ''
  return content ? content.slice(0, 24) : '星语诗词广场'
}

function normalizeTopic(topic) {
  const author = topic.author || {}
  const images = (topic.images || topic.image_urls || []).slice(0, 9)
  const comments = (topic.comments || []).map(normalizeComment)

  return {
    ...topic,
    content: topic.content || topic.summary || '',
    tags: normalizeTags(topic),
    time: topic.time || topic.created_at || '',
    author: {
      nickname: author.nickname || topic.author_name || '诗友',
      avatarText: author.avatarText || author.avatar_text || topic.author_avatar_text || '诗',
      avatarTone: author.avatarTone || author.avatar_tone || topic.author_avatar_tone || 'sage'
    },
    images,
    imageGridClass: `image-grid--count-${images.length}`,
    comments,
    previewComments: comments.slice(0, 3),
    isLiked: Boolean(topic.isLiked || topic.is_liked),
    isFavorited: Boolean(topic.isFavorited || topic.is_favorited),
    likeCount: topic.likeCount || topic.like_count || 0,
    favoriteCount: topic.favoriteCount || topic.favorite_count || 0,
    shareCount: topic.shareCount || topic.share_count || 0
  }
}

function normalizeRoom(room) {
  const playerCount = Number(room.playerCount || room.player_count || 0)
  const maxPlayers = Number(room.maxPlayers || room.max_players || 0)
  const creator = room.creator || {}
  const canWatch = Boolean(room.canWatch || room.can_watch)
  const isFull = maxPlayers > 0 && playerCount >= maxPlayers
  const roundText = room.roundText || room.round_text || ''
  const progress = maxPlayers > 0 ? Math.min(100, Math.round((playerCount / maxPlayers) * 100)) : 0

  return {
    ...room,
    playerCount,
    maxPlayers,
    roundText,
    canWatch,
    isFull,
    progress,
    statusText: isFull ? '已满员' : roundText.indexOf('等待') >= 0 || roundText.indexOf('招募') >= 0 ? '招募中' : '进行中',
    creator: {
      avatarText: creator.avatarText || creator.avatar_text || '诗',
      avatarTone: creator.avatarTone || creator.avatar_tone || 'sage',
      nickname: creator.nickname || room.creator_name || '诗友',
      level: creator.level || room.creator_level || 1,
      title: creator.title || room.creator_title || '飞花令玩家'
    }
  }
}

Page({
  data: {
    activeChannel: 'square',
    page: 1,
    list: [],
    hasMore: true,
    loading: false,
    roomLoading: false,
    rooms: [],
    filteredRooms: [],
    keywordOptions: [],
    roomKeyword: '',
    roomStatus: 'all',
    roomSearchValue: '',
    featuredRoom: null,
    roomCount: 0,
    watchableCount: 0,
    recruitingCount: 0,
    onlineCount: 0
  },

  onLoad() {
    this.loadFeed(true)
    this.loadRooms()
  },

  onShow() {
    if (this.hasShown && this.data.activeChannel === 'square') {
      this.loadFeed(true)
    }

    this.hasShown = true
  },

  onPullDownRefresh() {
    const task = this.data.activeChannel === 'square' ? this.loadFeed(true) : this.loadRooms()

    task.finally(() => {
      wx.stopPullDownRefresh()
    })
  },

  onReachBottom() {
    if (this.data.activeChannel === 'square' && !this.data.loading && this.data.hasMore) {
      this.loadFeed(false)
    }
  },

  onScrollToLower() {
    this.onReachBottom()
  },

  /**
   * 加载广场内容流。
   * refresh 为 true 时重置分页，适用于首次进入和下拉刷新。
   */
  loadFeed(refresh) {
    const nextPage = refresh ? 1 : this.data.page + 1
    this.setData({ loading: true })

    return getSquareFeed({ page: nextPage })
      .then((data) => {
        const items = (data.items || []).map(normalizeTopic)

        this.setData({
          page: nextPage,
          list: refresh ? items : this.data.list.concat(items),
          hasMore: Boolean(data.has_more)
        })
      })
      .catch(() => {
        showToast('广场内容暂时不可用')
      })
      .finally(() => {
        this.setData({ loading: false })
      })
  },

  loadRooms() {
    this.setData({ roomLoading: true })

    return Promise.all([getRooms(), getKeywords()])
      .then(([roomData, keywordData]) => {
        const rooms = (roomData.items || []).map(normalizeRoom)
        const keywordOptions = this.buildKeywordOptions(rooms, keywordData.items || [])

        this.setData({
          rooms,
          keywordOptions,
          featuredRoom: rooms[0] || null,
          roomCount: rooms.length,
          watchableCount: rooms.filter((item) => item.canWatch).length,
          recruitingCount: rooms.filter((item) => !item.isFull).length,
          onlineCount: roomData.online_count || 0
        })

        this.applyRoomFilters()
      })
      .catch(() => {
        showToast('对局列表暂时不可用')
      })
      .finally(() => {
        this.setData({ roomLoading: false })
      })
  },

  buildKeywordOptions(rooms, keywords) {
    const roomKeywords = rooms.map((room) => room.keyword).filter(Boolean)
    const merged = Array.from(new Set(roomKeywords.concat(keywords || [])))
    return merged.slice(0, 8)
  },

  applyRoomFilters() {
    const searchValue = this.data.roomSearchValue.trim().toLowerCase()
    const filteredRooms = this.data.rooms.filter((room) => {
      const matchKeyword = !this.data.roomKeyword || room.keyword === this.data.roomKeyword
      const matchStatus = this.matchRoomStatus(room)
      const searchable = [
        room.title,
        room.keyword,
        room.roundText,
        room.statusText,
        room.creator.nickname,
        room.creator.title
      ].join(' ').toLowerCase()
      const matchSearch = !searchValue || searchable.indexOf(searchValue) >= 0

      return matchKeyword && matchStatus && matchSearch
    })

    this.setData({ filteredRooms })
  },

  matchRoomStatus(room) {
    if (this.data.roomStatus === 'watchable') {
      return room.canWatch
    }

    if (this.data.roomStatus === 'recruiting') {
      return !room.isFull
    }

    if (this.data.roomStatus === 'active') {
      return room.statusText === '进行中'
    }

    return true
  },

  switchChannel(event) {
    const activeChannel = event.currentTarget.dataset.channel

    if (!activeChannel || activeChannel === this.data.activeChannel) {
      return
    }

    this.setData({ activeChannel })

    if (activeChannel === 'feihualing' && !this.data.rooms.length) {
      this.loadRooms()
    }
  },

  openSearch() {
    if (this.data.activeChannel === 'feihualing') {
      return
    }

    showToast('搜索开发中')
  },

  composePost() {
    if (this.data.activeChannel === 'square') {
      navigateTo('/pages/square-publish/square-publish')
      return
    }

    showToast('发起对局开发中')
  },

  handleRoomSearchInput(event) {
    this.setData({
      roomSearchValue: event.detail.value
    })

    this.applyRoomFilters()
  },

  clearRoomSearch() {
    this.setData({ roomSearchValue: '' })
    this.applyRoomFilters()
  },

  chooseRoomKeyword(event) {
    const keyword = event.currentTarget.dataset.keyword || ''

    this.setData({
      roomKeyword: keyword === this.data.roomKeyword ? '' : keyword
    })

    this.applyRoomFilters()
  },

  chooseRoomStatus(event) {
    const status = event.currentTarget.dataset.status || 'all'

    this.setData({ roomStatus: status })
    this.applyRoomFilters()
  },

  resetRoomFilters() {
    this.setData({
      roomKeyword: '',
      roomStatus: 'all',
      roomSearchValue: ''
    })

    this.applyRoomFilters()
  },

  openTopic(event) {
    const topicId = event.currentTarget.dataset.id

    if (!topicId) {
      return
    }

    navigateTo(`/pages/square-detail/square-detail?id=${topicId}`)
  },

  previewTopicImage(event) {
    const topicId = event.currentTarget.dataset.id
    const src = event.currentTarget.dataset.src
    const topic = this.data.list.find((item) => String(item.id) === String(topicId))

    if (!topic || !src) {
      return
    }

    wx.previewImage({
      current: src,
      urls: topic.images
    })
  },

  toggleTopicLike(event) {
    const topicId = event.currentTarget.dataset.id

    toggleSquareLike(topicId)
      .then((topic) => {
        this.replaceTopic(topic)
      })
      .catch(() => {
        showToast('点赞失败')
      })
  },

  toggleTopicFavorite(event) {
    const topicId = event.currentTarget.dataset.id

    toggleSquareFavorite(topicId)
      .then((topic) => {
        this.replaceTopic(topic)
      })
      .catch(() => {
        showToast('收藏失败')
      })
  },

  shareTopic(event) {
    const topicId = event.currentTarget.dataset.id

    increaseSquareShare(topicId)
      .then((topic) => {
        this.replaceTopic(topic)
      })
      .catch(() => {})
  },

  toggleCommentLike(event) {
    this.updateCommentAction(event, 'isLiked', 'likeCount')
  },

  toggleCommentFavorite(event) {
    this.updateCommentAction(event, 'isFavorited', 'favoriteCount')
  },

  updateCommentAction(event, stateKey, countKey) {
    const topicId = event.currentTarget.dataset.topicId
    const commentId = event.currentTarget.dataset.commentId
    const action = stateKey === 'isLiked' ? toggleSquareCommentLike : toggleSquareCommentFavorite

    action(topicId, commentId)
      .then((topic) => {
        this.replaceTopic(topic)
      })
      .catch(() => {
        showToast(countKey === 'likeCount' ? '点赞失败' : '收藏失败')
      })
  },

  replaceTopic(topic) {
    if (!topic) {
      return
    }

    const normalizedTopic = normalizeTopic(topic)
    const list = this.data.list.map((item) => {
      if (String(item.id) !== String(normalizedTopic.id)) {
        return item
      }

      return normalizedTopic
    })

    this.setData({ list })
  },

  openComments(event) {
    const topicId = event.currentTarget.dataset.id

    if (!topicId) {
      return
    }

    navigateTo(`/pages/square-detail/square-detail?id=${topicId}`)
  },

  enterRoom(event) {
    const roomId = event.currentTarget.dataset.id
    const room = this.data.rooms.find((item) => String(item.id) === String(roomId))

    showToast(room ? `进入「${room.title}」` : '进入对局')
  },

  onShareAppMessage(options) {
    const topicId = options && options.target ? options.target.dataset.id : ''
    const topic = this.data.list.find((item) => String(item.id) === String(topicId))

    return {
      title: topic ? getTopicShareTitle(topic) : '星语诗词广场',
      path: '/pages/square/square'
    }
  }
})
