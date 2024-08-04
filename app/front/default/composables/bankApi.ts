// 銀行情報取得時のレスポンスボディの型定義
export interface BankResponse {
    id: number
    bank_name: string
}

// useBankApiの名前で関数をエクスポート
export const useBankApi = () => {
	return {
		// 銀行情報一覧取得
		async getAll() {
			return useApi().get<BankResponse[]>("getBanks", "/banks/")
		},
	}
}