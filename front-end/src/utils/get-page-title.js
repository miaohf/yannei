// import defaultSettings from '@/settings'

const title = 'YANEI 研一智控'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
