const request = require('./request')
const config = require('../utils/config')
const { mockPoems, pageResult, findPoem } = require('./mock')

function getHomeData() {
  if (config.useMock) {
    return Promise.resolve({
      banners: [
        {
          id: 1,
          title: '今日诗意',
          poem_id: 1
        }
      ],
      today_poem: mockPoems[0],
      recommend_poems: mockPoems,
      hot_keywords: ['花', '月', '山', '水']
    })
  }

  return request({
    url: '/home'
  })
}

function getPoemDetail(poemId) {
  if (config.useMock) {
    return Promise.resolve(findPoem(poemId))
  }

  return request({
    url: `/poems/${poemId}`
  })
}

function getPoems(params = {}) {
  if (config.useMock) {
    return Promise.resolve(pageResult(mockPoems, params.page || 1, params.page_size || 10))
  }

  return request({
    url: '/poems',
    data: params
  })
}

function searchPoems(params = {}) {
  if (config.useMock) {
    const keyword = params.keyword || ''
    const items = mockPoems.filter((poem) => {
      return poem.title.indexOf(keyword) >= 0 || poem.author.indexOf(keyword) >= 0 || poem.content.indexOf(keyword) >= 0
    })
    return Promise.resolve(pageResult(items, params.page || 1, params.page_size || 10))
  }

  return request({
    url: '/poems/search',
    data: params
  })
}

function setMockPoemCounts(poemId, patch = {}) {
  const poem = mockPoems.find((item) => String(item.id) === String(poemId))

  if (!poem) {
    return null
  }

  Object.assign(poem, patch)
  return {
    poem_id: poem.id,
    id: poem.id,
    is_liked: Boolean(poem.is_liked),
    is_favorite: Boolean(poem.is_favorite),
    like_count: poem.like_count || 0,
    favorite_count: poem.favorite_count || 0,
    share_count: poem.share_count || 0
  }
}

function likePoem(poemId) {
  if (config.useMock) {
    const poem = mockPoems.find((item) => String(item.id) === String(poemId))
    if (!poem) {
      return Promise.resolve(null)
    }

    if (!poem.is_liked) {
      poem.is_liked = true
      poem.like_count = (poem.like_count || 0) + 1
    }

    return Promise.resolve(setMockPoemCounts(poemId))
  }

  return request({
    url: `/poems/${poemId}/like`,
    method: 'POST'
  })
}

function unlikePoem(poemId) {
  if (config.useMock) {
    const poem = mockPoems.find((item) => String(item.id) === String(poemId))
    if (!poem) {
      return Promise.resolve(null)
    }

    if (poem.is_liked) {
      poem.is_liked = false
      poem.like_count = Math.max(0, (poem.like_count || 0) - 1)
    }

    return Promise.resolve(setMockPoemCounts(poemId))
  }

  return request({
    url: `/poems/${poemId}/like`,
    method: 'DELETE'
  })
}

function sharePoem(poemId) {
  if (config.useMock) {
    const poem = mockPoems.find((item) => String(item.id) === String(poemId))
    if (!poem) {
      return Promise.resolve(null)
    }

    poem.share_count = (poem.share_count || 0) + 1
    return Promise.resolve(setMockPoemCounts(poemId))
  }

  return request({
    url: `/poems/${poemId}/share`,
    method: 'POST'
  })
}

module.exports = {
  getHomeData,
  getPoemDetail,
  getPoems,
  searchPoems,
  likePoem,
  unlikePoem,
  sharePoem
}
