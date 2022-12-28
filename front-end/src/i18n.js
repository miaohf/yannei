import Vue from 'vue'
import VueI18n from 'vue-i18n'

import ar from 'vuetify/lib/locale/ar'
import en from 'vuetify/lib/locale/en'
import zhHans from 'vuetify/lib/locale/zh-Hans'

Vue.use(VueI18n)

const messages = {
  en: {
    ...require('@/locales/en.json'),
    $vuetify: en,
  },
  ar: {
    ...require('@/locales/ar.json'),
    $vuetify: ar,
  },
  zh: {
    ...require('@/locales/zh.json'),
    $vuetify: zhHans,
  },
}

export default new VueI18n({
  locale: process.env.VUE_APP_I18N_LOCALE || 'en',
  fallbackLocale: process.env.VUE_APP_I18N_FALLBACK_LOCALE || 'en',
  messages,
})
