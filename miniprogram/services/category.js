const request = require('./request')
const config = require('../utils/config')
const { mockCategories, mockPoems, pageResult } = require('./mock')

function getCategories() {
  if (config.useMock) {
    return Promise.resolve({
      items: mockCategories
    })
  }

  return request({
    url: '/categories'
  })
}

function getCategoryPoems(categoryId, params = {}) {
  if (config.useMock) {
    const category = mockCategories.find((item) => String(item.id) === String(categoryId))
    const source = category ? mockPoems.filter((poem) => matchPoemByCategory(poem, category)) : mockPoems

    return Promise.resolve(pageResult(source, params.page || 1, params.page_size || 10))
  }

  return request({
    url: `/categories/${categoryId}/poems`,
    data: params
  })
}

function matchPoemByCategory(poem, category) {
  const name = category.name || ''
  const type = category.type || ''
  const tags = poem.tags || []
  const searchable = [poem.title, poem.author, poem.dynasty, poem.content].concat(tags).join(' ')

  if (searchable.indexOf(name) >= 0) {
    return true
  }

  if (type === '朝代') {
    return name.indexOf(poem.dynasty) >= 0
  }

  const relatedMap = {
    写景: ['山水', '春天', '秋天', '月'],
    思乡: ['思乡', '月', '故乡'],
    飞花令常用: ['月', '山', '水', '春', '秋'],
    宋词: ['词', '宋词']
  }
  const related = relatedMap[name] || []

  return related.some((keyword) => searchable.indexOf(keyword) >= 0)
}

module.exports = {
  getCategories,
  getCategoryPoems
}
