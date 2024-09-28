<template>
  <v-container class="fill-height">
		<Alert ref="alert" />
		<v-row  justify="center" align-content="center" class="d-flex">
			<v-tooltip location="end" min-width="600" min-height="500">
				<template v-slot:activator="{ props }">
					<v-btn color="primary" :href="authRequesturl" v-bind="props">login with keycloak</v-btn>
				</template>
				<v-img
					:src="imgUrl"
					alt="Tooltip Image"
					min-width="500"
					min-height="500"
				></v-img>
			</v-tooltip>
		</v-row>
	</v-container>
</template>

<script setup lang="ts">
import imgUrl from '@/assets/oidc_auth_request_animation.svg';
const { clientId, redirectUri } = useRuntimeConfig().public
const baseUrl = 'http://localhost:8888/realms/oidc-tutorial/protocol/openid-connect/auth';
const clientIdParam = `client_id=${clientId}`;
const responseTypeParam = 'response_type=code';
const responseModeParam = 'response_mode=query';
const redirectUriParam = `redirect_uri=${redirectUri}`;

const authRequesturl = `${baseUrl}?${clientIdParam}&${responseTypeParam}&${responseModeParam}&${redirectUriParam}`;
</script>
