import { defineNuxtConfig } from 'nuxt/config'
import vuetify from 'vite-plugin-vuetify'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  build: {
    transpile: ['vuetify'],
  },
  css: ['@/assets/main.scss'],

  modules: [
    // vite-plugin-vuetifyで必要なvuetifyのコンポーネントのみをバンドルするための設定
    async (options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        config.plugins!.push(vuetify())
      })
    },
  ],
  vite: {
    ssr: {  // SSRオプション: https://ja.vitejs.dev/config/ssr-options.html
      // 指定した依存関係が SSR のために外部化されるのを防ぎます。
      noExternal: ['vuetify'],
    },
    define: {  // define: https://ja.vitejs.dev/config/shared-options.html#define
      'process.env.DEBUG': false,
    },
  },
  runtimeConfig: {
    public: {
      clientBaseUrl: '//localhost:8080/api/v1',
      serverBaseUrl: 'http://localhost:8080/api/v1',
      clientId: 'oidc-tutorial',
      redirectUri: 'http://localhost:3000/callback',
    }
  },
})