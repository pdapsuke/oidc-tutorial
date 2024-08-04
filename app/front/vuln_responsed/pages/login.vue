<template>
  <v-container class="fill-height">
		<Alert ref="alert" />
		<v-row  justify="center" align-content="center" class="d-flex">
			<v-btn color="primary" :href="authRequesturl">login with keycloak(vuln_responsed)</v-btn>
		</v-row>
	</v-container>
</template>

<script setup lang="ts">
const { clientId, redirectUri } = useRuntimeConfig().public
const baseUrl = 'http://localhost:8888/realms/oidc-tutorial/protocol/openid-connect/auth';
const clientIdParam = `client_id=${clientId}`;
const responseTypeParam = 'response_type=code';
const responseModeParam = 'response_mode=query';
const redirectUriParam = `redirect_uri=${redirectUri}`;

const authRequesturl = `${baseUrl}?${clientIdParam}&${responseTypeParam}&${responseModeParam}&${redirectUriParam}`;
</script>
