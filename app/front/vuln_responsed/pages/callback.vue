<template>
  <v-container class="py-8 px-6 fillheight" fluid >
    <Alert ref="alert" />
    <div>Please wait...</div>
	</v-container>
</template>

<script setup lang="ts">
import Keycloak from 'keycloak-js'

const alert = ref<any>(null)
const auth = useAuth()
const keycloak = useState<Keycloak>('keycloak') // keycloakの状態を取得

onMounted(() => {
  new Promise<void>((resolve) => {
    auth.login(keycloak.value.token || '', keycloak.value.refreshToken || '')
    resolve()
  }).then(() => {
    console.log(auth.authenticated('access'))
    setTimeout(() => {
      navigateTo('/')
    }, 2000)}
  )
  .catch((error) => { 
    console.error(error)
    setTimeout(() => {
      navigateTo('/login')
    }, 2000)
  })
})
</script>
