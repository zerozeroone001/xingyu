const {
  getSquareTopic,
  toggleSquareLike,
  toggleSquareFavorite,
  increaseSquareShare,
  createSquareComment,
  toggleSquareCommentLike,
  toggleSquareCommentFavorite
} = require('../../services/square')
const { showToast } = require('../../utils/toast')
const { navigateBack } = require('../../utils/route')

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
  const source = topic || {}
  const author = source.author || {}
  const images = (source.images || source.image_urls || []).slice(0, 9)
  const comments = (source.comments || []).map(normalizeComment)

  return {
    ...source,
    content: source.content || source.summary || '',
    tags: normalizeTags(source),
    time: source.time || source.created_at || '',
    author: {
      nickname: author.nickname || source.author_name || '诗友',
      avatarText: author.avatarText || author.avatar_text || source.author_avatar_text || '诗',
      avatarTone: author.avatarTone || author.avatar_tone || source.author_avatar_tone || 'sage'
    },
    images,
    imageGridClass: `image-grid--count-${images.length}`,
    comments,
    isLiked: Boolean(source.isLiked || source.is_liked),
    isFavorited: Boolean(source.isFavorited || source.is_favorited),
    likeCount: source.likeCount || source.like_count || 0,
    favoriteCount: source.favoriteCount || source.favorite_count || 0,
    shareCount: source.shareCount || source.share_count || 0
  }
}

Page({
  data: {
    topicId: '',
    topic: null,
    loading: true,
    commentValue: '',
    sendingComment: false
  },

  onLoad(options) {
    this.setData({ topicId: options.id || '' })
    this.loadTopic(options.id)
  },

  onShareAppMessage() {
    this.increaseShareCount()

    return {
      title: this.data.topic ? getTopicShareTitle(this.data.topic) : '星语诗词广场',
      path: `/pages/square-detail/square-detail?id=${this.data.topicId}`
    }
  },

  loadTopic(topicId) {
    this.setData({ loading: true })

    return getSquareTopic(topicId)
      .then((topic) => {
        if (!topic) {
          showToast('话题不存在')
          return
        }

        const normalizedTopic = normalizeTopic(topic)

        this.setData({
          topic: normalizedTopic
        })
        wx.setNavigationBarTitle({ title: '动态详情' })
      })
      .catch(() => {
        showToast('话题加载失败')
      })
      .finally(() => {
        this.setData({ loading: false })
      })
  },

  setTopic(topic) {
    if (!topic) {
      return
    }

    this.setData({
      topic: normalizeTopic(topic)
    })
  },

  previewImage(event) {
    const src = event.currentTarget.dataset.src

    if (!this.data.topic || !src) {
      return
    }

    wx.previewImage({
      current: src,
      urls: this.data.topic.images
    })
  },

  toggleLike() {
    toggleSquareLike(this.data.topicId)
      .then((topic) => {
        this.setTopic(topic)
      })
      .catch(() => {
        showToast('点赞失败')
      })
  },

  toggleFavorite() {
    toggleSquareFavorite(this.data.topicId)
      .then((topic) => {
        this.setTopic(topic)
        showToast(topic && topic.isFavorited ? '已收藏' : '已取消', 'success')
      })
      .catch(() => {
        showToast('收藏失败')
      })
  },

  shareTopic() {
    this.increaseShareCount()
  },

  increaseShareCount() {
    increaseSquareShare(this.data.topicId)
      .then((topic) => {
        this.setTopic(topic)
      })
      .catch(() => {})
  },

  handleCommentInput(event) {
    this.setData({ commentValue: event.detail.value })
  },

  submitComment() {
    if (this.data.sendingComment) {
      return
    }

    const content = this.data.commentValue.trim()

    if (!content) {
      showToast('请输入评论内容')
      return
    }

    this.setData({ sendingComment: true })

    createSquareComment(this.data.topicId, content)
      .then((topic) => {
        this.setTopic(topic)
        this.setData({ commentValue: '' })
        showToast('评论已发布', 'success')
      })
      .catch(() => {
        showToast('评论失败')
      })
      .finally(() => {
        this.setData({ sendingComment: false })
      })
  },

  toggleCommentLike(event) {
    const commentId = event.currentTarget.dataset.commentId

    toggleSquareCommentLike(this.data.topicId, commentId)
      .then((topic) => {
        this.setTopic(topic)
      })
      .catch(() => {
        showToast('点赞失败')
      })
  },

  toggleCommentFavorite(event) {
    const commentId = event.currentTarget.dataset.commentId

    toggleSquareCommentFavorite(this.data.topicId, commentId)
      .then((topic) => {
        this.setTopic(topic)
      })
      .catch(() => {
        showToast('收藏失败')
      })
  },

  goBack() {
    navigateBack()
  }
})
