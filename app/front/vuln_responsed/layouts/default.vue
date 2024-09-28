<template>
  <v-app>
    <!-- ヘッダー >>> -->
    <v-app-bar color="primary" :elevation="2">
      <v-app-bar-title>
        <div @click="useRouter().push('/')" style="cursor: pointer;">OIDC-TUTORIAL *VULN_RESPONSED VERSION</div>
      </v-app-bar-title>
      <div v-if="auth.authenticated('access')">ようこそ、{{ useAuth().getUsername() }}さん</div>
      <v-btn v-if="auth.authenticated('access')" :icon="mdiLogout" @click="logout()"></v-btn>
    </v-app-bar>
    <!-- <<< ヘッダー -->

    <!-- コンテンツ >>> -->
    <v-main>
      <slot />
    </v-main>
    <!-- <<< コンテンツ -->

    <!-- フッター >>> -->
    <v-footer class="footer justify-center">
      <div>&copy; 2024 OIDC-TUTORIAL</div>
    </v-footer>
    <!-- <<< フッター -->
  </v-app>
</template>

<script setup lang="ts">
import Keycloak from 'keycloak-js'
import { mdiLogout } from '@mdi/js'

const { clientId, loginUri } = useRuntimeConfig().public
const auth = useAuth()

// useStateでKeycloakオブジェクトを保持する
const keycloak = useState<Keycloak>('keycloak', () => {
  return new Keycloak({
    url: 'http://localhost:8888',
    realm: 'oidc-tutorial',
    clientId: clientId,
  })
})

try {
  const authenticated = await keycloak.value.init({
    onLoad: 'check-sso',
  })
  console.log(`User is ${authenticated ? 'authenticated' : 'not authenticated'}`)
} catch (error) {
  console.error('Failed to initialize adapter:', error)
}

async function logout() {
  await new Promise<void>((resolve) => {
    auth.logout()
    resolve()
  })
  if (!auth.authenticated('access')) {
    keycloak.value.logout({redirectUri: loginUri})
  }
}
</script>

<style lang="scss">
.footer {
  width: 100%;
  position: absolute;
  bottom: 0;
}
</style>