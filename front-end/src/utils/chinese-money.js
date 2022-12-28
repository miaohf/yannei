// JavaScript数字金额转换成中文大写显示
export default function moneyToString(num) {
  const digits = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
  const radices = ['', '拾', '佰', '仟', '万', '亿']
  const bigRadices = ['', '万', '亿']
  const decimals = ['角', '分'] // 这里只精确到分
  const cnDollar = '元'
  const cnInteger = '整'
  // intStr = Math.floor(num).toString();
  // floatStr = num % 1;
  const numArr = num.toString().split('.')
  const intStr = numArr[0] || ''
  let floatStr = numArr[1] || ''
  if (floatStr.length > 2) {
    floatStr = floatStr.substr(0, 2)
  }
  let outputCharacters = ''
  if (intStr) {
    let zeroCount = 0
    const intLen = intStr.length
    for (var i = 0; i < intLen; i++) {
      const p = intLen - i - 1
      var d = intStr.substr(i, 1)
      const quotient = p / 4
      var modulus = p % 4
      if (d === '0') {
        zeroCount++
      } else {
        if (zeroCount > 0) {
          outputCharacters += digits[0]
        }
        zeroCount = 0
        outputCharacters += digits[d] + radices[modulus]
      }
      if (modulus === 0 && zeroCount < 4) {
        outputCharacters += bigRadices[quotient]
        zeroCount = 0
      }
    }
    outputCharacters += cnDollar
  }

  if (floatStr) {
    const floatLen = floatStr.length
    for (let i = 0; i < floatLen; i++) {
      const d = floatStr.substr(i, 1)
      if (d !== '0') {
        outputCharacters += digits[d] + decimals[i]
      }
    }
  }

  if (outputCharacters === '') {
    outputCharacters = digits[0] + cnDollar
  }

  if (floatStr) {
    outputCharacters += cnInteger
  }

  return outputCharacters
}
