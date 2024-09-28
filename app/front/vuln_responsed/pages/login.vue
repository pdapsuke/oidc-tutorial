<template>
  <v-container class="fill-height">
		<Alert ref="alert" />
		<v-row  justify="center" align-content="center" class="d-flex">
			<v-btn color="primary" @click="login">login with keycloak</v-btn>
		</v-row>
	</v-container>
</template>

<script setup lang="ts">
import Keycloak from 'keycloak-js'

const { redirectUri } = useRuntimeConfig().public

// useStateでkeycloakの状態を取得
const keycloak = useState<Keycloak>('keycloak')

console.log(keycloak.value.authenticated)
function login() {
	keycloak.value.login({redirectUri: redirectUri})
}
</script>
