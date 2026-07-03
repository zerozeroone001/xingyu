const request = require('./request')
const config = require('../utils/config')

function getKeywords() {
  if (config.useMock) {
    return Promise.resolve({
      items: ['花', '月', '山', '水', '春', '秋']
    })
  }

  return request({
    url: '/feihualing/keywords'
  })
}

function getRooms() {
  if (config.useMock) {
    return Promise.resolve({
      items: [
        {
          id: 101,
          title: '月下雅集',
          keyword: '月',
          canWatch: true,
          playerCount: 3,
          maxPlayers: 6,
          roundText: '第 3 轮',
          creator: {
            avatarText: '苏',
            avatarTone: 'sage',
            nickname: '苏东坡',
            level: 12,
            title: '翰林学士'
          }
        },
        {
          id: 102,
          title: '春山快局',
          keyword: '春',
          canWatch: false,
          playerCount: 2,
          maxPlayers: 4,
          roundText: '等待开局',
          creator: {
            avatarText: '林',
            avatarTone: 'green',
            nickname: '林深不知处',
            level: 8,
            title: '青衫诗客'
          }
        },
        {
          id: 103,
          title: '江雪夜话',
          keyword: '雪',
          canWatch: true,
          playerCount: 5,
          maxPlayers: 6,
          roundText: '第 6 轮',
          creator: {
            avatarText: '墨',
            avatarTone: 'ink',
            nickname: '墨客小张',
            level: 10,
            title: '行吟者'
          }
        },
        {
          id: 104,
          title: '秋声一令',
          keyword: '秋',
          canWatch: true,
          playerCount: 1,
          maxPlayers: 4,
          roundText: '招募中',
          creator: {
            avatarText: '采',
            avatarTone: 'warm',
            nickname: '采菊东篱',
            level: 7,
            title: '田园诗友'
          }
        }
      ],
      online_count: 28
    })
  }

  return request({
    url: '/feihualing/rooms'
  })
}

function checkAnswer(data) {
  if (config.useMock) {
    const isCorrect = data.answer.indexOf(data.keyword) >= 0
    return Promise.resolve({
      keyword: data.keyword,
      answer: data.answer,
      is_correct: isCorrect,
      score: isCorrect ? 10 : 0
    })
  }

  return request({
    url: '/feihualing/check',
    method: 'POST',
    data
  })
}

function saveRecord(data) {
  if (config.useMock) {
    return Promise.resolve(
      Object.assign(
        {
          id: Date.now()
        },
        data
      )
    )
  }

  return request({
    url: '/feihualing/records',
    method: 'POST',
    data
  })
}

module.exports = {
  getKeywords,
  getRooms,
  checkAnswer,
  saveRecord
}
