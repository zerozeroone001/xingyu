const request = require('./request')
const config = require('../utils/config')
const { mockUser, mockPoems, mockSquareFeed, pageResult } = require('./mock')

const mockFollowings = [
  {
    id: 1,
    nickname: '林深不知处',
    avatarText: '林',
    title: '青衫诗客',
    signature: '偏爱山水诗与雨后松风',
    followedAt: '3 天前'
  },
  {
    id: 2,
    nickname: '采菊东篱',
    avatarText: '采',
    title: '田园诗友',
    signature: '一卷陶诗，一盏清茶',
    followedAt: '12 天前'
  },
  {
    id: 3,
    nickname: '夜读诗人',
    avatarText: '夜',
    title: '飞花令常客',
    signature: '今晚也要接住一句月',
    followedAt: '1 个月前'
  }
]

function getMockProfile() {
  const favoriteCount = mockPoems.filter((poem) => poem.is_favorite).length
  const likeCount = mockSquareFeed.reduce((total, post) => total + Number(post.likeCount || 0), 0)

  return Object.assign({}, mockUser, {
    nickname: mockUser.nickname || '诗词访客',
    avatarText: '苏',
    title: '翰林学士',
    level: 12,
    gender: '保密',
    city: '杭州',
    bio: '喜欢山水清词，也常在飞花令里练一句月。',
    poem_count: mockSquareFeed.length,
    like_count: likeCount,
    favorite_count: favoriteCount,
    following_count: mockFollowings.length
  })
}

function mapPoemList(poem, relation) {
  return {
    id: poem.id,
    kind: 'poem',
    title: poem.title,
    subtitle: `${poem.dynasty} · ${poem.author}`,
    content: poem.recommend_sentence || poem.content,
    badge: relation,
    meta: (poem.tags || []).slice(0, 3).join(' · '),
    likeCount: poem.like_count || 0,
    favoriteCount: poem.favorite_count || 0,
    targetUrl: `/pages/poem-detail/poem-detail?id=${poem.id}`
  }
}

function mapPostList(post) {
  return {
    id: post.id,
    kind: 'post',
    title: post.title,
    subtitle: post.author && post.author.nickname ? post.author.nickname : '诗词访客',
    content: post.content,
    badge: post.badge || '诗作',
    meta: post.time || '',
    likeCount: post.likeCount || 0,
    favoriteCount: post.favoriteCount || 0,
    targetUrl: `/pages/square-detail/square-detail?id=${post.id}`
  }
}

function mapFollowList(user) {
  return {
    id: user.id,
    kind: 'user',
    title: user.nickname,
    subtitle: user.title,
    content: user.signature,
    badge: '关注',
    meta: `关注于 ${user.followedAt}`,
    avatarText: user.avatarText
  }
}

function getMockProfileItems(type) {
  if (type === 'likes') {
    return mockSquareFeed
      .slice()
      .sort((left, right) => Number(right.likeCount || 0) - Number(left.likeCount || 0))
      .map((post) => Object.assign(mapPostList(post), { badge: '获赞' }))
  }

  if (type === 'favorites') {
    return mockPoems.filter((poem) => poem.is_favorite).map((poem) => mapPoemList(poem, '已收藏'))
  }

  if (type === 'follows') {
    return mockFollowings.map(mapFollowList)
  }

  return mockSquareFeed.map(mapPostList)
}

function getCurrentUser() {
  if (config.useMock) {
    return Promise.resolve(getMockProfile())
  }

  return request({
    url: '/users/me'
  })
}

function updateCurrentUser(data = {}) {
  if (config.useMock) {
    return Promise.resolve(Object.assign({}, getMockProfile(), data))
  }

  return request({
    url: '/users/me',
    method: 'PUT',
    data
  })
}

function getProfileOverview() {
  if (config.useMock) {
    const user = getMockProfile()

    return Promise.resolve({
      user,
      stats: {
        poems: user.poem_count,
        likes: user.like_count,
        favorites: user.favorite_count,
        follows: user.following_count
      }
    })
  }

  return request({
    url: '/users/me/overview'
  })
}

function getProfileItems(type = 'poems', params = {}) {
  if (config.useMock) {
    return Promise.resolve(pageResult(getMockProfileItems(type), params.page || 1, params.page_size || 10))
  }

  return request({
    url: `/users/me/${type}`,
    data: params
  })
}

function getFavorites(params = {}) {
  if (config.useMock) {
    return Promise.resolve(pageResult(mockPoems.filter((poem) => poem.is_favorite), params.page || 1, params.page_size || 10))
  }

  return request({
    url: '/favorites',
    data: params
  })
}

function addFavorite(poemId) {
  if (config.useMock) {
    return Promise.resolve({
      poem_id: poemId,
      is_favorite: true
    })
  }

  return request({
    url: `/favorites/${poemId}`,
    method: 'POST'
  })
}

function removeFavorite(poemId) {
  if (config.useMock) {
    return Promise.resolve({
      poem_id: poemId,
      is_favorite: false
    })
  }

  return request({
    url: `/favorites/${poemId}`,
    method: 'DELETE'
  })
}

function getHistory(params = {}) {
  if (config.useMock) {
    return Promise.resolve(pageResult(mockPoems, params.page || 1, params.page_size || 10))
  }

  return request({
    url: '/history',
    data: params
  })
}

function submitFeedback(data = {}) {
  if (config.useMock) {
    return Promise.resolve({
      id: Date.now(),
      status: 'received',
      created_at: new Date().toISOString(),
      content: data.content || ''
    })
  }

  return request({
    url: '/feedback',
    method: 'POST',
    data
  })
}

module.exports = {
  getCurrentUser,
  updateCurrentUser,
  getProfileOverview,
  getProfileItems,
  getFavorites,
  addFavorite,
  removeFavorite,
  getHistory,
  submitFeedback
}
