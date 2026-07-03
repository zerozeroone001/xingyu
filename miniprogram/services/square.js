const request = require('./request')
const config = require('../utils/config')
const { mockSquareFeed, pageResult } = require('./mock')

const STORAGE_KEY = 'square:published_topics'

function canUseStorage() {
  return typeof wx !== 'undefined' && wx.getStorageSync && wx.setStorageSync
}

function getStoredTopics() {
  if (!canUseStorage()) {
    return []
  }

  try {
    return wx.getStorageSync(STORAGE_KEY) || []
  } catch (error) {
    return []
  }
}

function saveStoredTopics(topics) {
  if (!canUseStorage()) {
    return
  }

  wx.setStorageSync(STORAGE_KEY, topics)
}

function getAllMockTopics() {
  return getStoredTopics().concat(mockSquareFeed)
}

function findMockTopic(topicId) {
  return getAllMockTopics().find((item) => String(item.id) === String(topicId))
}

function updateMockTopic(topicId, updater) {
  const storedTopics = getStoredTopics()
  const storedIndex = storedTopics.findIndex((item) => String(item.id) === String(topicId))

  if (storedIndex >= 0) {
    const nextTopic = updater(storedTopics[storedIndex])
    storedTopics.splice(storedIndex, 1, nextTopic)
    saveStoredTopics(storedTopics)
    return nextTopic
  }

  const mockIndex = mockSquareFeed.findIndex((item) => String(item.id) === String(topicId))

  if (mockIndex < 0) {
    return null
  }

  const nextTopic = updater(mockSquareFeed[mockIndex])
  mockSquareFeed.splice(mockIndex, 1, nextTopic)
  return nextTopic
}

function offsetCount(value, active) {
  return Math.max(0, (value || 0) + (active ? 1 : -1))
}

function createTitleFromContent(content) {
  const text = String(content || '').replace(/\s+/g, ' ').trim()

  return text ? text.slice(0, 24) : '广场动态'
}

function getSquareFeed(params = {}) {
  if (config.useMock) {
    return Promise.resolve(pageResult(getAllMockTopics(), params.page || 1, params.page_size || 10))
  }

  return request({
    url: '/square/feed',
    data: params
  })
}

function getSquareTopic(topicId) {
  if (config.useMock) {
    return Promise.resolve(findMockTopic(topicId))
  }

  return request({
    url: `/square/feed/${topicId}`
  })
}

function createSquareTopic(data) {
  if (config.useMock) {
    const storedTopics = getStoredTopics()
    const tags = Array.isArray(data.tags) && data.tags.length ? data.tags : [data.badge || '随笔']
    const topic = {
      id: `local-${Date.now()}`,
      title: createTitleFromContent(data.content),
      content: data.content,
      tags,
      badge: tags[0],
      time: '刚刚',
      author: {
        nickname: '诗词访客',
        avatarText: '我',
        avatarTone: 'green'
      },
      images: data.images || [],
      likeCount: 0,
      favoriteCount: 0,
      shareCount: 0,
      isLiked: false,
      isFavorited: false,
      comments: []
    }

    storedTopics.unshift(topic)
    saveStoredTopics(storedTopics)
    return Promise.resolve(topic)
  }

  return request({
    url: '/square/feed',
    method: 'POST',
    data
  })
}

function toggleSquareLike(topicId) {
  if (config.useMock) {
    return Promise.resolve(
      updateMockTopic(topicId, (topic) => {
        const isLiked = !topic.isLiked

        return Object.assign({}, topic, {
          isLiked,
          likeCount: offsetCount(topic.likeCount, isLiked)
        })
      })
    )
  }

  return request({
    url: `/square/feed/${topicId}/like`,
    method: 'POST'
  })
}

function toggleSquareFavorite(topicId) {
  if (config.useMock) {
    return Promise.resolve(
      updateMockTopic(topicId, (topic) => {
        const isFavorited = !topic.isFavorited

        return Object.assign({}, topic, {
          isFavorited,
          favoriteCount: offsetCount(topic.favoriteCount, isFavorited)
        })
      })
    )
  }

  return request({
    url: `/square/feed/${topicId}/favorite`,
    method: 'POST'
  })
}

function increaseSquareShare(topicId) {
  if (config.useMock) {
    return Promise.resolve(
      updateMockTopic(topicId, (topic) =>
        Object.assign({}, topic, {
          shareCount: (topic.shareCount || 0) + 1
        })
      )
    )
  }

  return request({
    url: `/square/feed/${topicId}/share`,
    method: 'POST'
  })
}

function createSquareComment(topicId, content) {
  if (config.useMock) {
    return Promise.resolve(
      updateMockTopic(topicId, (topic) => {
        const comment = {
          id: `comment-${Date.now()}`,
          nickname: '诗词访客',
          avatarText: '我',
          avatarTone: 'green',
          content,
          time: '刚刚',
          likeCount: 0,
          favoriteCount: 0,
          isLiked: false,
          isFavorited: false
        }

        return Object.assign({}, topic, {
          comments: [comment].concat(topic.comments || [])
        })
      })
    )
  }

  return request({
    url: `/square/feed/${topicId}/comments`,
    method: 'POST',
    data: { content }
  })
}

function updateSquareComment(topicId, commentId, updater) {
  return updateMockTopic(topicId, (topic) => {
    const comments = (topic.comments || []).map((comment) => {
      if (String(comment.id) !== String(commentId)) {
        return comment
      }

      return updater(comment)
    })

    return Object.assign({}, topic, { comments })
  })
}

function toggleSquareCommentLike(topicId, commentId) {
  if (config.useMock) {
    return Promise.resolve(
      updateSquareComment(topicId, commentId, (comment) => {
        const isLiked = !comment.isLiked

        return Object.assign({}, comment, {
          isLiked,
          likeCount: offsetCount(comment.likeCount, isLiked)
        })
      })
    )
  }

  return request({
    url: `/square/feed/${topicId}/comments/${commentId}/like`,
    method: 'POST'
  })
}

function toggleSquareCommentFavorite(topicId, commentId) {
  if (config.useMock) {
    return Promise.resolve(
      updateSquareComment(topicId, commentId, (comment) => {
        const isFavorited = !comment.isFavorited

        return Object.assign({}, comment, {
          isFavorited,
          favoriteCount: offsetCount(comment.favoriteCount, isFavorited)
        })
      })
    )
  }

  return request({
    url: `/square/feed/${topicId}/comments/${commentId}/favorite`,
    method: 'POST'
  })
}

module.exports = {
  getSquareFeed,
  getSquareTopic,
  createSquareTopic,
  toggleSquareLike,
  toggleSquareFavorite,
  increaseSquareShare,
  createSquareComment,
  toggleSquareCommentLike,
  toggleSquareCommentFavorite
}
