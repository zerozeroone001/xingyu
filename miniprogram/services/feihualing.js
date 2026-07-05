const request = require('./request')
const config = require('../utils/config')
const { mockPoems, pageResult } = require('./mock')

const ROOM_STORAGE_KEY = 'feihualing:created_rooms'
const KNOWN_LINE_CORRECTIONS = {
  床前看月光: '床前明月光',
  举头望山月: '举头望明月'
}

const mockBattleData = {
  月: {
    history: [
      {
        role: 'opponent',
        playerName: '苏东坡',
        content: '明月几时有，把酒问青天。',
        source: {
          title: '水调歌头·明月几时有',
          dynasty: '宋',
          author: '苏轼'
        }
      },
      {
        role: 'opponent',
        playerName: '林深不知处',
        content: '床前明月光，疑是地上霜。',
        source: {
          title: '静夜思',
          dynasty: '唐',
          author: '李白'
        }
      }
    ],
    replies: [
      {
        playerName: '采菊东篱',
        content: '明月松间照，清泉石上流。',
        source: {
          title: '山居秋暝',
          dynasty: '唐',
          author: '王维'
        }
      },
      {
        playerName: '墨客小张',
        content: '举头望明月，低头思故乡。',
        source: {
          title: '静夜思',
          dynasty: '唐',
          author: '李白'
        }
      }
    ]
  },
  春: {
    history: [
      {
        role: 'opponent',
        playerName: '林深不知处',
        content: '好雨知时节，当春乃发生。',
        source: {
          title: '春夜喜雨',
          dynasty: '唐',
          author: '杜甫'
        }
      }
    ],
    replies: [
      {
        playerName: '苏东坡',
        content: '竹外桃花三两枝，春江水暖鸭先知。',
        source: {
          title: '惠崇春江晚景',
          dynasty: '宋',
          author: '苏轼'
        }
      }
    ]
  },
  秋: {
    history: [
      {
        role: 'opponent',
        playerName: '采菊东篱',
        content: '空山新雨后，天气晚来秋。',
        source: {
          title: '山居秋暝',
          dynasty: '唐',
          author: '王维'
        }
      }
    ],
    replies: [
      {
        playerName: '墨客小张',
        content: '万里悲秋常作客，百年多病独登台。',
        source: {
          title: '登高',
          dynasty: '唐',
          author: '杜甫'
        }
      }
    ]
  },
  雪: {
    history: [
      {
        role: 'opponent',
        playerName: '墨客小张',
        content: '孤舟蓑笠翁，独钓寒江雪。',
        source: {
          title: '江雪',
          dynasty: '唐',
          author: '柳宗元'
        }
      }
    ],
    replies: [
      {
        playerName: '苏东坡',
        content: '梅须逊雪三分白，雪却输梅一段香。',
        source: {
          title: '雪梅',
          dynasty: '宋',
          author: '卢梅坡'
        }
      }
    ]
  }
}

function getMockBattle(keyword) {
  return mockBattleData[keyword] || {
    history: [],
    replies: []
  }
}

function canUseStorage() {
  return typeof wx !== 'undefined' && wx.getStorageSync && wx.setStorageSync
}

function getStoredRooms() {
  if (!canUseStorage()) {
    return []
  }

  try {
    return wx.getStorageSync(ROOM_STORAGE_KEY) || []
  } catch (error) {
    return []
  }
}

function saveStoredRooms(rooms) {
  if (canUseStorage()) {
    wx.setStorageSync(ROOM_STORAGE_KEY, rooms)
  }
}

function getMockRooms() {
  return [
    {
      id: 101,
      title: '月下雅集',
      keyword: '月',
      canWatch: true,
      playerCount: 3,
      maxPlayers: 6,
      roundText: '第 3 轮',
      battleMessages: getMockBattle('月').history,
      replyPool: getMockBattle('月').replies,
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
      battleMessages: getMockBattle('春').history,
      replyPool: getMockBattle('春').replies,
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
      battleMessages: getMockBattle('雪').history,
      replyPool: getMockBattle('雪').replies,
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
      battleMessages: getMockBattle('秋').history,
      replyPool: getMockBattle('秋').replies,
      creator: {
        avatarText: '采',
        avatarTone: 'warm',
        nickname: '采菊东篱',
        level: 7,
        title: '田园诗友'
      }
    }
  ]
}

function getKeywords() {
  if (config.useMock) {
    return Promise.resolve({
      items: ['花', '月', '山', '水', '春', '秋', '风', '雪', '人', '江']
    })
  }

  return request({
    url: '/feihualing/keywords'
  })
}

function getRooms() {
  if (config.useMock) {
    return Promise.resolve({
      items: getStoredRooms().concat(getMockRooms()),
      online_count: 28
    })
  }

  return request({
    url: '/feihualing/rooms'
  })
}

function getRoom(roomId) {
  if (config.useMock) {
    const room = getStoredRooms()
      .concat(getMockRooms())
      .find((item) => String(item.id) === String(roomId))

    return Promise.resolve(room || null)
  }

  return request({
    url: `/feihualing/rooms/${roomId}`
  })
}

function getMyRooms(params = {}) {
  if (config.useMock) {
    const rooms = getStoredRooms().concat(getMockRooms()).map((room, index) => {
      const latestMessage = (room.battleMessages || [])[0] || null

      return Object.assign({}, room, {
        joinedAt: index === 0 ? '刚刚' : `${index + 1} 天前`,
        statusText: room.roundText || '招募中',
        latestLine: latestMessage ? latestMessage.content : '等待诗友开局',
        resultText: index % 3 === 0 ? '进行中' : (index % 3 === 1 ? '已参与' : '已围观')
      })
    })

    return Promise.resolve(pageResult(rooms, params.page || 1, params.page_size || 10))
  }

  return request({
    url: '/feihualing/rooms',
    data: params
  })
}

function createRoom(data) {
  if (config.useMock) {
    const storedRooms = getStoredRooms()
    const keyword = String(data.keyword || '').trim().slice(0, 2) || '月'
    const title = String(data.title || '').trim() || `${keyword}字雅集`
    const room = {
      id: `local-room-${Date.now()}`,
      title,
      keyword,
      canWatch: data.canWatch !== undefined ? Boolean(data.canWatch) : Boolean(data.can_watch),
      playerCount: 1,
      maxPlayers: Number(data.maxPlayers || data.max_players || 4),
      roundText: '招募中',
      phase: 'waiting',
      battleMessages: [],
      replyPool: getMockBattle(keyword).replies,
      creator: {
        avatarText: '我',
        avatarTone: 'green',
        nickname: '诗词访客',
        level: 1,
        title: '新晋令主'
      }
    }

    storedRooms.unshift(room)
    saveStoredRooms(storedRooms)
    return Promise.resolve(room)
  }

  return request({
    url: '/feihualing/rooms',
    method: 'POST',
    data
  })
}

function normalizeSentence(value) {
  return String(value || '')
    .replace(/[\s，。！？、；：“”‘’《》（）,.!?;:'"()[\]{}-]/g, '')
    .trim()
}

function applyKnownCorrections(value) {
  return Object.keys(KNOWN_LINE_CORRECTIONS).reduce((text, wrong) => {
    return text.replace(new RegExp(wrong, 'g'), KNOWN_LINE_CORRECTIONS[wrong])
  }, String(value || ''))
}

function normalizeWithIndex(value) {
  const chars = []
  const indexMap = []
  const source = String(value || '')
  const punctuationPattern = /[\s，。！？、；：“”‘’《》（）,.!?;:'"()[\]{}-]/

  Array.from(source).forEach((char, index) => {
    if (punctuationPattern.test(char)) {
      return
    }

    chars.push(char)
    indexMap.push(index)
  })

  return {
    text: chars.join(''),
    indexMap
  }
}

function getAllowedTypos(length) {
  if (length <= 4) {
    return 1
  }

  if (length <= 14) {
    return 2
  }

  return 3
}

function getTypoCorrections(answer, candidate, indexMap) {
  if (answer.length !== candidate.length) {
    return []
  }

  const corrections = []
  Array.from(answer).forEach((char, index) => {
    if (char !== candidate[index]) {
      corrections.push({
        index: indexMap[index],
        original: char,
        corrected: candidate[index]
      })
    }
  })
  return corrections
}

function getPoemSource(poem) {
  return poem
    ? {
        id: poem.id,
        title: poem.title,
        author: poem.author,
        dynasty: poem.dynasty,
        content: applyKnownCorrections(poem.content)
      }
    : null
}

function findBestFuzzyMatch(normalizedAnswer, indexMap) {
  if (normalizedAnswer.length < 4) {
    return null
  }

  const allowedTypos = getAllowedTypos(normalizedAnswer.length)
  let best = null

  mockPoems.some((poem) => {
    const text = normalizeSentence(applyKnownCorrections([poem.content, poem.recommend_sentence].filter(Boolean).join('')))

    for (let start = 0; start <= text.length - normalizedAnswer.length; start += 1) {
      const candidate = text.slice(start, start + normalizedAnswer.length)
      let typoCount = 0

      for (let index = 0; index < normalizedAnswer.length; index += 1) {
        if (normalizedAnswer[index] !== candidate[index]) {
          typoCount += 1
        }
      }

      if (typoCount === 0 || typoCount > allowedTypos) {
        continue
      }

      if (!best || typoCount < best.typo_count) {
        const corrections = getTypoCorrections(normalizedAnswer, candidate, indexMap)
        best = {
          poem,
          corrected_answer: candidate,
          typo_count: typoCount,
          wrong_indices: corrections.map((item) => item.index),
          corrections
        }
      }

      if (typoCount === 1) {
        return true
      }
    }

    return false
  })

  return best
}

function checkAnswer(data) {
  if (config.useMock) {
    const answer = String(data.answer || '').trim()
    const normalized = normalizeWithIndex(answer)
    const normalizedAnswer = normalized.text
    const isCorrect = Boolean(data.keyword && answer.indexOf(data.keyword) >= 0)
    const poem = mockPoems.find((item) => {
      const sourceText = applyKnownCorrections([item.content, item.recommend_sentence].filter(Boolean).join(''))
      return normalizeSentence(sourceText).indexOf(normalizedAnswer) >= 0
    })
    const fuzzyMatch = poem ? null : findBestFuzzyMatch(normalizedAnswer, normalized.indexMap)
    const sourcePoem = poem || (fuzzyMatch ? fuzzyMatch.poem : null)

    return Promise.resolve({
      keyword: data.keyword,
      answer,
      is_correct: Boolean(isCorrect && poem),
      score: isCorrect && (poem || fuzzyMatch) ? 10 : 0,
      source: getPoemSource(sourcePoem),
      recognized: Boolean(poem || fuzzyMatch),
      recognition_status: poem && isCorrect ? 'exact' : (fuzzyMatch ? 'typo' : 'not_found'),
      corrected_answer: fuzzyMatch ? fuzzyMatch.corrected_answer : answer,
      typo_count: fuzzyMatch ? fuzzyMatch.typo_count : 0,
      wrong_indices: fuzzyMatch ? fuzzyMatch.wrong_indices : [],
      corrections: fuzzyMatch ? fuzzyMatch.corrections : []
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
  getMyRooms,
  getRoom,
  createRoom,
  checkAnswer,
  saveRecord
}
