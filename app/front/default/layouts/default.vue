<template>
  <v-app>
    <!-- ヘッダー >>> -->
    <v-app-bar color="primary" :elevation="2">
      <v-app-bar-title>
        <div @click="useRouter().push('/')" style="cursor: pointer;">OIDC-TUTORIAL</div>
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
import { mdiLogout } from '@mdi/js'

const auth = useAuth()

async function logout() {
  // ログアウトエンドポイントへのリクエストのパラメータを定義
  const logoutEndpoint = 'http://localhost:8888/realms/oidc-tutorial/protocol/openid-connect/logout'
  const { clientId } = useRuntimeConfig().public
  const refreshToken = useAuth().getToken("refresh")
  const params = new URLSearchParams();

  params.append('client_id', `${clientId}`);
  params.append('refresh_token', `${refreshToken}`);

  try {
    const response = await fetch(logoutEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params.toString(),
    })
    if (response.ok) {
      auth.logout()
      useRouter().push({path: "/login"})
    } else {
      throw new Error('Failed to fetch access token');
    }

  } catch (error) {
    console.error('Error fetching access token:', error);
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