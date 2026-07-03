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

module.exports = {
  getHomeData,
  getPoemDetail,
  getPoems,
  searchPoems
}
