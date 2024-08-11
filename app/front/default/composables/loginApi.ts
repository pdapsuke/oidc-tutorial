// useLoginApiの名前で関数をエクスポート
export const useLoginApi = () => {
	return {
		// ログインリクエスト
		async validateAccessToken() {
			return useApi().get<string>("validateAccessToken", "/login/")
		},
  }
}