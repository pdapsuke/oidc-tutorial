// 各ページを読み込む前にトークンを検証する
export default defineNuxtRouteMiddleware(async(to, from) => {
	// Cookieからアクセストークン取得, 取得できなければ'/login'にリダイレクト
	const token = useAuth().getToken("access")
	if (token==null) {
		return navigateTo('/login')
	}

	let authenticated: boolean | undefined = undefined // トークン検証用フラグ

	async function validateAccessToken() {
		// バックエンドにアクセストークン検証リクエスト
		const { data, error } = await useLoginApi().validateAccessToken()
		if (!data.value || error.value) {
			console.error(error.value)
			authenticated = false
		} else {
			authenticated = true
		}
	}

	// トークン検証の結果、authenticatedフラグにfalseがセットされた場合、'/signin'にリダイレクト
	await validateAccessToken()
	if (authenticated==false) {
		return navigateTo('/login')
	}
})
