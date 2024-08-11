// 銀行情報取得時のレスポンスボディの型定義
export interface BranchResponse {
	id: number
	bank_id: number
	branch_name: string
}

// useBranchApiの名前で関数をエクスポート
export const useBranchApi = () => {
	return {
		// 銀行情報一覧取得
		async getAll() {
			return useApi().get<BranchResponse[]>("getBranches", "/branches/")
		},
	}
}