<template>
  <v-container class="py-8 px-6 fillheight" fluid >
    <Alert ref="alert" />
    <div class="d-flex justify-center mb-5 font-weight-bold"><リダイレクトURLから取得した認可コード> <br>{{ queryParam }}</div>
    <div class="d-flex justify-center">
      <v-img
        :src="imgUrl"
        alt="Tooltip Image"
        max-width="600"
        max-height="600"
      ></v-img>
    </div>
	</v-container>
</template>

<script setup lang="ts">
import imgUrl from '@/assets/oidc_token_request_animation.svg';

const alert = ref<any>(null)
const route = useRoute();

// クエリパラメータのcode(認可コード)の値を取得
const queryParam = route.query.code || '';
queryParam.toString()

async function fetchAccessToken(authCode: string) {
  // トークンエンドポイントへのリクエストのパラメータを定義
  const tokenEndpoint = 'http://localhost:8888/realms/oidc-tutorial/protocol/openid-connect/token'
  const { clientId, redirectUri } = useRuntimeConfig().public
  const params = new URLSearchParams()

  params.append('grant_type', 'authorization_code')
  params.append('code', authCode)
  params.append('client_id', `${clientId}`)
  params.append('redirect_uri', `${redirectUri}`)

  const sleep = (ms:number) => new Promise(resolve => {
    setTimeout(resolve, ms)
  })

  try {
    await sleep(15000)
    const response = await fetch(tokenEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: params.toString(),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch access token');
    }

    // トークンエンドポイントからのレスポンスを返す
    return response.json();
  } catch (error) {
    alert.value.error(`Error fetching access token: ${error}`);
    console.error('Error fetching access token:', error);
  }
}

onMounted(() => {
  // 認可コードを使用してアクセストークンを取得
	fetchAccessToken(`${queryParam}`).then(data => {
		if (data) {
      console.log(data) // デバッグ用
      useAuth().login(data.access_token, data.refresh_token)
      navigateTo('/')
		} else {
      setTimeout(() => {
        navigateTo('/login')
      }, 2000)
    }
	});
});
</script>
