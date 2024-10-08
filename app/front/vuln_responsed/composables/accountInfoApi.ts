// 口座情報作成時のリクエストボディの型定義
interface AccountInfoPost {
  branch_id: number
  account_type: string
  account_number: string
  secret_number: string
}

// 口座情報取得時のレスポンスボディの型定義
interface AccountInfoResponse {
  id: number
  user_id: number
  bank_name: string
  branch_name: string
  account_type: string
  account_number: string
  secret_number: string
  created: string
}

// useAccountInfoApiの名前で関数をエクスポート
export const useAccountInfoApi = () => {
	return {
		// 口座情報一覧取得
		async getAll() {
			return useApi().get<AccountInfoResponse[]>("getAccountInfos", "/account_infos/")
		},
    // 口座情報削除
    async delete(id: number) {
      return useApi().delete<{[index: string]: string}>("getAccountInfos", `/account_infos/${id}`)
    },
    // 口座情報作成
    async post(params: AccountInfoPost) {
      return useApi().post<{[index: string]: string}>("postAccountInfo", "/account_infos/", params)
    }
	}
}