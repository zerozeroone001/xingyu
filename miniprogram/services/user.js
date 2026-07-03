const request = require('./request')
const config = require('../utils/config')
const { mockUser, mockPoems, pageResult } = require('./mock')

function getCurrentUser() {
  if (config.useMock) {
    return Promise.resolve(mockUser)
  }

  return request({
    url: '/users/me'
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

module.exports = {
  getCurrentUser,
  getFavorites,
  addFavorite,
  removeFavorite,
  getHistory
}
