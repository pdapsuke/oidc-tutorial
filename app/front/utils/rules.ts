export const useRules = () => {
	return ValidationRules
}

class ValidationRules {
	// 必須入力のバリデーション
	public static required(v: string) {
		return !!v || "入力必須です。"
	}

	// 口座番号のバリデーション
	// 7文字の半角数字
	public static accountNumberValidate(v: string) {
		const accountNumberRegex = /^\d{7}$/
		return (v && accountNumberRegex.test(v)) || "7文字の半角数字で入力してください。"
	}

	// 暗証番号のバリデーション
	// 4文字の数字
	public static secretNumberValidate(v: string) {
		const accountNumberRegex = /^\d{4}$/
		return (v && accountNumberRegex.test(v)) || "4文字の半角数字で入力してください。"
	}
}
