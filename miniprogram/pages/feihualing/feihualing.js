const {
  getKeywords,
  getRooms,
  getRoom,
  createRoom: createRoomApi,
  checkAnswer,
  saveRecord
} = require('../../services/feihualing')
const { showToast } = require('../../utils/toast')

function getRoomPhase(room, roundText) {
  const rawPhase = String(room.phase || room.status || room.room_status || '').toLowerCase()
  const text = String(roundText || room.roundText || room.round_text || '')

  if (rawPhase === 'ended' || rawPhase === 'finished' || text.indexOf('结束') >= 0) {
    return 'ended'
  }

  if (rawPhase === 'waiting' || rawPhase === 'recruiting' || text.indexOf('等待') >= 0 || text.indexOf('招募') >= 0) {
    return 'waiting'
  }

  return 'playing'
}

function normalizeRoom(room) {
  const creator = room.creator || {}
  const playerCount = Number(room.playerCount || room.player_count || 0)
  const maxPlayers = Number(room.maxPlayers || room.max_players || 4)
  const roundText = room.roundText || room.round_text || '招募中'
  const phase = getRoomPhase(room, roundText)
  const canWatch = Boolean(room.canWatch || room.can_watch)
  const isFull = maxPlayers > 0 && playerCount >= maxPlayers
  const canEnter = phase === 'ended' ? canWatch : !isFull || canWatch
  const primaryRole = canWatch && (phase === 'ended' || isFull) ? 'spectator' : 'player'
  const primaryActionText = phase === 'waiting'
    ? '入局等待'
    : phase === 'ended'
      ? (canWatch ? '查看回顾' : '已结束')
      : isFull
        ? (canWatch ? '观战' : '已满员')
        : '进入对局'

  return {
    ...room,
    id: room.id,
    title: room.title || '飞花令对局',
    keyword: room.keyword || '月',
    canWatch,
    playerCount,
    maxPlayers,
    roundText,
    phase,
    isFull,
    canEnter,
    primaryRole,
    primaryActionText,
    battleMessages: room.battleMessages || room.battle_messages || [],
    replyPool: room.replyPool || room.reply_pool || [],
    creator: {
      avatarText: creator.avatarText || creator.avatar_text || '诗',
      avatarTone: creator.avatarTone || creator.avatar_tone || 'sage',
      nickname: creator.nickname || room.creator_name || '诗友',
      level: creator.level || room.creator_level || 1,
      title: creator.title || room.creator_title || '飞花令玩家'
    }
  }
}

function getRoleName(role) {
  if (role === 'host') {
    return '令主'
  }

  if (role === 'spectator') {
    return '观战'
  }

  return '入局'
}

function normalizeAnswer(answer) {
  return String(answer || '')
    .replace(/[\s，。！？、；：“”‘’《》（）,.!?;:'"()[\]{}-]/g, '')
    .trim()
}

function getSourceText(result) {
  if (result.source_text || result.sourceText) {
    return result.source_text || result.sourceText
  }

  if (typeof result.source === 'string') {
    return result.source
  }

  const source = result.source || result.poem || {}
  const title = source.title || result.title || result.poem_title
  const dynasty = source.dynasty || result.dynasty || result.poem_dynasty
  const author = source.author || result.author || result.poem_author

  if (title || dynasty || author) {
    return `《${title || '佚名篇目'}》${dynasty ? `${dynasty} · ` : ''}${author || '佚名'}`
  }

  return result.is_correct || result.isCorrect ? '出处待补充' : '未匹配到出处'
}

function normalizeSource(result = {}) {
  const source = result.source || result.poem || result.sourceInfo || {}

  if (!source || typeof source === 'string') {
    return null
  }

  const title = source.title || result.title || result.poem_title
  const dynasty = source.dynasty || result.dynasty || result.poem_dynasty
  const author = source.author || result.author || result.poem_author
  const content = source.content || source.full_content || source.fullContent || result.poem_content || ''

  if (!title && !author && !content) {
    return null
  }

  return {
    id: source.id || source.poem_id || result.poem_id || '',
    title: title || '佚名篇目',
    dynasty: dynasty || '',
    author: author || '佚名',
    content
  }
}

function getSourceKey(source) {
  if (!source) {
    return ''
  }

  return [source.title, source.dynasty, source.author].filter(Boolean).join('|')
}

function normalizeBattleMessage(message, index) {
  const role = message.role || 'opponent'
  const content = message.content || ''
  const source = normalizeSource(message)

  return {
    id: message.id || `message-history-${index}`,
    role,
    playerName: message.playerName || message.player_name || (role === 'opponent' ? '对手' : ''),
    content,
    contentParts: message.contentParts || message.content_parts || buildContentParts(content, message),
    isCorrect: message.isCorrect !== undefined ? message.isCorrect : message.is_correct !== undefined ? message.is_correct : true,
    statusText: message.statusText || message.status_text || (role === 'user' ? '通过' : ''),
    source,
    sourceKey: getSourceKey(source),
    sourceText: message.sourceText || message.source_text || getSourceText(message)
  }
}

function getWrongIndices(result) {
  return result.wrong_indices || result.wrongIndices || []
}

function getTypoCorrections(result) {
  return result.corrections || result.typo_corrections || result.typoCorrections || []
}

function normalizeContentWithIndex(content) {
  const chars = []
  const indexMap = []
  const punctuationPattern = /[\s，。！？、；：“”‘’《》（）,.!?;:'"()[\]{}-]/

  Array.from(String(content || '')).forEach((char, index) => {
    if (punctuationPattern.test(char)) {
      return
    }

    chars.push(char)
    indexMap.push(index)
  })

  return {
    chars,
    indexMap
  }
}

function buildContentParts(content, result = {}) {
  const source = Array.from(String(content || ''))
  const normalized = normalizeContentWithIndex(content)
  const correctedAnswer = Array.from(String(result.corrected_answer || result.correctedAnswer || ''))
  const correctionMap = {}

  getTypoCorrections(result).forEach((item) => {
    const index = Number(item.index)
    if (!Number.isNaN(index)) {
      correctionMap[index] = {
        corrected: item.corrected,
        original: item.original
      }
    }
  })

  getWrongIndices(result).forEach((index) => {
    const sourceIndex = Number(index)
    const normalizedIndex = normalized.indexMap.indexOf(sourceIndex)
    if (Number.isNaN(sourceIndex) || correctionMap[sourceIndex]) {
      return
    }

    correctionMap[sourceIndex] = {
      corrected: correctedAnswer[normalizedIndex],
      original: source[sourceIndex]
    }
  })

  return source.reduce((parts, text, index) => {
    const correction = correctionMap[index]

    if (!correction) {
      parts.push({ text, wrong: false })
      return parts
    }

    parts.push({ text: correction.corrected || text, wrong: false })
    parts.push({ text: `(${correction.original || text})`, wrong: true })
    return parts
  }, [])
}

function getAnswerStatusText(result, isCorrect) {
  if (isCorrect) {
    return '通过'
  }

  const typoCount = Number(result.typo_count || result.typoCount || 0)
  if (typoCount > 0) {
    return '有错字'
  }

  return '未通过'
}

Page({
  data: {
    mode: 'lobby',
    loading: false,
    entering: false,
    checking: false,
    creating: false,
    keywords: ['月', '春', '秋', '雪'],
    rooms: [],
    roomCount: 0,
    watchableCount: 0,
    onlineCount: 0,
    activeRoom: null,
    keyword: '',
    messages: [],
    answerInput: '',
    messageAnchor: '',
    opponentThinking: false,
    viewerRole: 'player',
    entryRole: '',
    entryFrom: '',
    roomPhase: 'waiting',
    readyState: '',
    waitTitle: '',
    waitHint: '',
    waitActionText: '',
    resultTitle: '',
    resultSummary: '',
    resultStats: [],
    sourcePopupVisible: false,
    activeSource: null
  },

  onLoad(options = {}) {
    this.pendingRoomId = options.roomId || ''
    this.entryRole = options.role || ''
    this.entryFrom = options.from || ''
    this.setData({
      entryRole: this.entryRole,
      entryFrom: this.entryFrom
    })

    if (this.pendingRoomId) {
      this.setData({
        mode: 'entering',
        entering: true
      })
    }

    this.loadKeywords()
    this.loadRooms().then(() => {
      if (this.pendingRoomId) {
        this.enterRoomById(this.pendingRoomId)
        this.pendingRoomId = ''
      }
    })
  },

  onPullDownRefresh() {
    if (this.data.mode === 'room' && this.data.activeRoom) {
      this.refreshActiveRoom().finally(() => {
        wx.stopPullDownRefresh()
      })
      return
    }

    this.loadRooms().finally(() => {
      wx.stopPullDownRefresh()
    })
  },

  onUnload() {
    if (this.replyTimer) {
      clearTimeout(this.replyTimer)
      this.replyTimer = null
    }
  },

  loadKeywords() {
    return getKeywords()
      .then((data) => {
        const keywords = data.items || []

        if (keywords.length) {
          this.setData({ keywords })
        }
      })
      .catch(() => {})
  },

  loadRooms() {
    this.setData({ loading: true })

    return getRooms()
      .then((data) => {
        const rooms = (data.items || []).map(normalizeRoom)

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

  refreshActiveRoom() {
    const roomId = this.data.activeRoom.id

    return getRoom(roomId)
      .then((room) => {
        if (room) {
          this.openRoom(normalizeRoom(room), { keepRole: true })
        }
      })
      .catch(() => {
        showToast('房间状态刷新失败')
      })
  },

  createRoom() {
    if (this.data.creating) {
      return
    }

    const keyword = this.pickKeyword()

    this.entryRole = 'host'
    this.setData({
      creating: true,
      entryRole: 'host',
      entryFrom: 'create',
      mode: 'entering',
      entering: true
    })

    createRoomApi({
      keyword,
      title: `${keyword}字雅集`,
      canWatch: true,
      maxPlayers: 4
    })
      .then((room) => {
        this.openRoom(normalizeRoom(room), { role: 'host' })
        return this.loadRooms()
      })
      .catch(() => {
        this.setData({ mode: 'lobby' })
        showToast('发起对局失败')
      })
      .finally(() => {
        this.setData({
          creating: false,
          entering: false
        })
      })
  },

  pickKeyword() {
    const keywords = this.data.keywords.length ? this.data.keywords : ['月']
    const index = Math.floor(Math.random() * keywords.length)

    return keywords[index] || '月'
  },

  enterRoom(event) {
    const roomId = event.currentTarget.dataset.id
    const role = event.currentTarget.dataset.role || 'player'
    const room = this.data.rooms.find((item) => String(item.id) === String(roomId))

    if (room && !room.canEnter) {
      showToast('该对局暂不可进入')
      return
    }

    this.entryRole = role
    this.setData({ entryRole: role })
    this.enterRoomById(roomId)
  },

  enterRoomById(roomId) {
    if (!roomId) {
      return Promise.resolve(null)
    }

    this.setData({
      mode: 'entering',
      entering: true
    })

    const localRoom = this.data.rooms.find((item) => String(item.id) === String(roomId))

    if (localRoom) {
      this.openRoom(localRoom)
      this.setData({ entering: false })
      return Promise.resolve(localRoom)
    }

    return getRoom(roomId)
      .then((room) => {
        if (!room) {
          showToast('对局不存在')
          this.setData({ mode: 'lobby' })
          return null
        }

        const normalizedRoom = normalizeRoom(room)
        this.openRoom(normalizedRoom)
        return normalizedRoom
      })
      .catch(() => {
        this.setData({ mode: 'lobby' })
        showToast('进入对局失败')
      })
      .finally(() => {
        this.setData({ entering: false })
      })
  },

  openRoom(room, options = {}) {
    const normalizedRoom = normalizeRoom(room)
    const viewerRole = options.role || (options.keepRole ? this.data.viewerRole : this.resolveViewerRole(normalizedRoom))
    const roomPhase = normalizedRoom.phase
    const welcomeMessage = {
      id: 'message-welcome',
      role: 'system',
      content: viewerRole === 'spectator'
        ? `正在观战「${normalizedRoom.keyword}」字飞花令，诗句更新会在这里展示。`
        : `本局令字「${normalizedRoom.keyword}」，请发出含有该字的诗句；已经出现过的诗句不能重复。`
    }
    const historyMessages = normalizedRoom.battleMessages.map(normalizeBattleMessage)
    const messages = [welcomeMessage].concat(historyMessages)

    wx.setNavigationBarTitle({
      title: `${normalizedRoom.keyword}字飞花令`
    })

    if (this.replyTimer) {
      clearTimeout(this.replyTimer)
      this.replyTimer = null
    }

    this.setData({
      mode: 'room',
      activeRoom: normalizedRoom,
      keyword: normalizedRoom.keyword,
      messages,
      answerInput: '',
      messageAnchor: messages[messages.length - 1].id,
      opponentThinking: false,
      viewerRole,
      roomPhase,
      readyState: '',
      resultTitle: roomPhase === 'ended' ? (viewerRole === 'spectator' ? '观战结束' : '本局结束') : '',
      resultSummary: roomPhase === 'ended' ? '本局飞花令已完成，可回看诗句记录。' : '',
      resultStats: this.getResultStats(normalizedRoom, messages)
    })

    this.updateWaitingCopy(viewerRole, roomPhase, normalizedRoom)
  },

  resolveViewerRole(room) {
    if (this.entryRole === 'host' || this.entryRole === 'player' || this.entryRole === 'spectator') {
      return this.entryRole
    }

    if (room.phase === 'ended' || room.playerCount >= room.maxPlayers) {
      return room.canWatch ? 'spectator' : 'player'
    }

    return 'player'
  },

  updateWaitingCopy(viewerRole, roomPhase, room) {
    if (roomPhase !== 'waiting') {
      return
    }

    const readyCount = Math.max(1, Number(room.playerCount || 1))
    const waitCopy = {
      host: {
        waitTitle: '已发起对局，等待诗友入局',
        waitHint: `${readyCount}/${room.maxPlayers} 人在房间，开局后将进入轮流接令。`,
        waitActionText: '开始对局'
      },
      player: {
        waitTitle: '已进入房间，等待令主开局',
        waitHint: `令字为「${room.keyword}」，当前 ${readyCount}/${room.maxPlayers} 人。`,
        waitActionText: this.data.readyState ? '已准备' : '准备好了'
      },
      spectator: {
        waitTitle: '正在观战等待区',
        waitHint: '令主还未开局，可先查看房间信息。',
        waitActionText: '刷新状态'
      }
    }[viewerRole]

    this.setData(waitCopy)
  },

  returnLobby() {
    if (this.replyTimer) {
      clearTimeout(this.replyTimer)
      this.replyTimer = null
    }

    wx.setNavigationBarTitle({
      title: '飞花令'
    })

    this.setData({
      mode: 'lobby',
      activeRoom: null,
      keyword: '',
      messages: [],
      answerInput: '',
      messageAnchor: '',
      opponentThinking: false,
      viewerRole: 'player',
      roomPhase: 'waiting',
      readyState: '',
      waitTitle: '',
      waitHint: '',
      waitActionText: '',
      resultTitle: '',
      resultSummary: '',
      resultStats: []
    })

    this.loadRooms()
  },

  handleAnswerInput(event) {
    this.setData({
      answerInput: event.detail.value
    })
  },

  submitAnswer() {
    if (this.data.checking || this.data.opponentThinking || this.data.roomPhase !== 'playing' || this.data.viewerRole === 'spectator') {
      return
    }

    const answer = this.data.answerInput.trim()
    const keyword = this.data.keyword

    if (!answer) {
      showToast('请先写一句诗')
      return
    }

    if (answer.indexOf(keyword) < 0) {
      showToast(`诗句需包含「${keyword}」`)
      return
    }

    if (this.hasUsedAnswer(answer)) {
      showToast('这句已经出现过')
      return
    }

    this.setData({ checking: true })

    checkAnswer({
      room_id: this.data.activeRoom.id,
      keyword,
      answer
    })
      .then((result) => {
        const isCorrect = Boolean(result.is_correct || result.isCorrect)

        if (this.hasUsedPoemSource(result)) {
          showToast('同一首诗本局已出现过')
          return
        }

        if (!isCorrect) {
          this.appendCheckedMessage(answer, result, false)
          showToast('诗句校验未通过')
          return
        }

        this.appendCheckedMessage(answer, result, true)

        saveRecord({
          keyword,
          answer,
          is_correct: true,
          score: result.score || 10,
          source: result.source || null
        }).catch(() => {})

        this.queueOpponentReply()
      })
      .catch(() => {
        showToast('校验失败')
      })
      .finally(() => {
        this.setData({ checking: false })
      })
  },

  appendCheckedMessage(answer, result, isCorrect) {
    const source = normalizeSource(result)
    const message = {
      id: `message-${Date.now()}`,
      role: 'user',
      playerName: '我',
      content: answer,
      contentParts: buildContentParts(answer, result),
      isCorrect,
      statusText: getAnswerStatusText(result, isCorrect),
      source,
      sourceKey: getSourceKey(source),
      sourceText: getSourceText(Object.assign({}, result, { is_correct: isCorrect }))
    }

    this.setData({
      messages: this.data.messages.concat(message),
      answerInput: isCorrect ? '' : this.data.answerInput,
      messageAnchor: message.id,
      opponentThinking: isCorrect
    })
  },

  hasUsedPoemSource(result) {
    const sourceKey = getSourceKey(normalizeSource(result))

    if (!sourceKey) {
      return false
    }

    return this.data.messages.some((message) => {
      if (!message.sourceKey || message.sourceKey !== sourceKey) {
        return false
      }

      if (message.role === 'opponent') {
        return true
      }

      return message.role === 'user' && message.isCorrect
    })
  },

  handleSourceTap(event) {
    const messageId = event.currentTarget.dataset.id
    const message = this.data.messages.find((item) => String(item.id) === String(messageId))

    if (!message || !message.source) {
      return
    }

    this.setData({
      activeSource: message.source,
      sourcePopupVisible: true
    })
  },

  closeSourcePopup() {
    this.setData({
      sourcePopupVisible: false,
      activeSource: null
    })
  },

  noop() {},

  hasUsedAnswer(answer) {
    const normalizedAnswer = normalizeAnswer(answer)

    if (!normalizedAnswer) {
      return false
    }

    return this.data.messages.some((message) => {
      if (message.role !== 'user' && message.role !== 'opponent') {
        return false
      }

      return normalizeAnswer(message.content) === normalizedAnswer
    })
  },

  queueOpponentReply() {
    if (this.replyTimer) {
      clearTimeout(this.replyTimer)
    }

    this.replyTimer = setTimeout(() => {
      const reply = this.getNextOpponentReply()

      if (!reply) {
        const endMessage = {
          id: `message-system-${Date.now()}`,
          role: 'system',
          content: '对手本轮未能接上，你守住了这轮诗令。'
        }

        this.setData({
          messages: this.data.messages.concat(endMessage),
          messageAnchor: endMessage.id,
          opponentThinking: false
        })
        this.finishRoom('对手本轮未能接上，你守住了这轮诗令。')
        return
      }

      const message = normalizeBattleMessage(
        Object.assign({}, reply, {
          id: `message-opponent-${Date.now()}`,
          role: 'opponent',
          isCorrect: true
        }),
        this.data.messages.length
      )
      const activeRoom = Object.assign({}, this.data.activeRoom, {
        roundText: `第 ${this.getBattleLineCount() + 1} 轮`
      })

      this.setData({
        activeRoom,
        messages: this.data.messages.concat(message),
        messageAnchor: message.id,
        opponentThinking: false
      })
    }, 600)
  },

  getNextOpponentReply() {
    const replyPool = this.data.activeRoom ? this.data.activeRoom.replyPool || [] : []

    return replyPool.find((reply) => !this.hasUsedAnswer(reply.content))
  },

  getBattleLineCount() {
    return this.data.messages.filter((message) => message.role === 'user' || message.role === 'opponent').length
  },

  handleWaitingAction() {
    if (this.data.roomPhase !== 'waiting') {
      return
    }

    if (this.data.viewerRole === 'spectator') {
      this.refreshActiveRoom()
      return
    }

    if (this.data.viewerRole === 'player' && !this.data.readyState) {
      this.setData({
        readyState: 'ready',
        waitActionText: '已准备',
        waitHint: `令字为「${this.data.activeRoom.keyword}」，等待令主开局。`
      })

      setTimeout(() => {
        if (this.data.roomPhase === 'waiting') {
          this.startRoom()
        }
      }, 700)
      return
    }

    this.startRoom()
  },

  startRoom() {
    if (!this.data.activeRoom || this.data.roomPhase === 'playing') {
      return
    }

    const activeRoom = Object.assign({}, this.data.activeRoom, {
      phase: 'playing',
      roundText: '第 1 轮',
      playerCount: Math.max(2, this.data.activeRoom.playerCount)
    })
    const startMessage = {
      id: `message-system-${Date.now()}`,
      role: 'system',
      content: `${getRoleName(this.data.viewerRole)}已就位，对局开始。`
    }

    this.setData({
      activeRoom,
      roomPhase: 'playing',
      messages: this.data.messages.concat(startMessage),
      messageAnchor: startMessage.id,
      readyState: ''
    })
  },

  finishRoom(summary) {
    if (!this.data.activeRoom || this.data.roomPhase === 'ended') {
      return
    }

    const activeRoom = Object.assign({}, this.data.activeRoom, {
      phase: 'ended',
      roundText: '已结束'
    })

    this.setData({
      activeRoom,
      roomPhase: 'ended',
      opponentThinking: false,
      resultTitle: this.data.viewerRole === 'spectator' ? '观战结束' : '本局结束',
      resultSummary: summary || '本局飞花令已完成，可回看诗句记录。',
      resultStats: this.getResultStats(activeRoom, this.data.messages)
    })
  },

  endRoom() {
    this.finishRoom('本局已结束，诗句记录已保留在对局中。')
  },

  replayRoom() {
    if (!this.data.activeRoom) {
      return
    }

    const activeRoom = Object.assign({}, this.data.activeRoom, {
      phase: 'waiting',
      roundText: '招募中',
      battleMessages: []
    })
    const welcomeMessage = {
      id: `message-welcome-${Date.now()}`,
      role: 'system',
      content: `新一局令字「${activeRoom.keyword}」，等待诗友入局。`
    }
    const nextRole = this.data.viewerRole === 'spectator' ? 'player' : this.data.viewerRole

    this.setData({
      activeRoom,
      roomPhase: 'waiting',
      viewerRole: nextRole,
      messages: [welcomeMessage],
      messageAnchor: welcomeMessage.id,
      answerInput: '',
      readyState: '',
      resultTitle: '',
      resultSummary: '',
      resultStats: []
    })

    this.updateWaitingCopy(nextRole, 'waiting', activeRoom)
  },

  getResultStats(room, messages) {
    const battleMessages = (messages || []).filter((message) => message.role === 'user' || message.role === 'opponent')
    const playerLines = battleMessages.filter((message) => message.role === 'user' && message.isCorrect).length
    const opponentLines = battleMessages.filter((message) => message.role === 'opponent').length

    return [
      { label: '令字', value: room.keyword || this.data.keyword || '-' },
      { label: '诗句', value: battleMessages.length },
      { label: '我方', value: playerLines },
      { label: '对手', value: opponentLines }
    ]
  }
})
