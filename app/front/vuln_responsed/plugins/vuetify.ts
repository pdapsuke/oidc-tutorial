import { createVuetify, ThemeDefinition } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'

const myCustomLightTheme: ThemeDefinition = {
  dark: false,
  colors: {
      primary: "#1F2D5A",
      secondary: "#38508a",
      accent: "#FB8C00",
      success: "#43A047",
      info: "#0288D1",
      warning: "#FFC107",
      error: "#F44336",
  },
}

export default defineNuxtPlugin(nuxtApp => {
  const vuetify = createVuetify({
    ssr: true,  // Vue3はssrが利用されているかを自動的に検出できないので、明示的にssrの利用有無を設定する
    icons: {
			defaultSet: 'mdi',
			aliases,
			sets: {
					mdi,
			},
    },
		theme: {
      defaultTheme: "myCustomLightTheme",
      themes: {
        myCustomLightTheme,
      }
    },
  })
  nuxtApp.vueApp.use(vuetify)
})