<template>
	<Alert ref="alert" />
	<v-dialog v-model="dialog" persistent max-width="400px">
		<v-card>
			<v-card-title class="my-3">
				<span class="headline">{{props.title}}</span>
			</v-card-title>
			<v-form ref="postForm" lazy-validation class="mx-3">
				<v-select
					v-model="selectedBank"
					variant="outlined"
					label="銀行名"
					:items="params.banks"
					:rules="[rules.required]"
					item-title="bank_name"
					item-value="id"
					clearable
					class="mb-3"
				></v-select>
				<v-select
					v-model="selectedBranch"
					variant="outlined"
					label="支店"
					:items="branches ?? []"
					:rules="[rules.required]"
					item-title="branch_name"
					item-value="id"
					clearable
					class="mb-3"
				></v-select>
				<v-select
					v-model="selectedAccountType"
					variant="outlined"
					label="口座種別"
					:items="[{id: 1, value: '普通口座'}, {id: 2, value: '定期口座'}, {id: 3, value: '総合口座'}]"
					item-title="value"
					item-value="value"
					:rules="[rules.required]"
					clearable
					class="mb-3"
				></v-select>
				<v-text-field
					v-model="accountNumber"
					label="口座番号"
					variant="outlined"
					:rules="[rules.accountNumberValidate]"
				></v-text-field>
				<v-text-field
					v-model="secretNumber"
					:rules="[rules.secretNumberValidate]"
					:append-inner-icon="showPasswords ? mdiEye : mdiEyeOff"
					:type="showPasswords ? 'text' : 'password'"
					variant="outlined"
					label="暗証番号"
					@click:append-inner="showPasswords = !showPasswords"
				></v-text-field>
			</v-form>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn :color="props.colorCancel" @click="confirm(false)">{{cancelBtn}}</v-btn>
				<v-btn :color="props.colorConfirm" @click="confirm(true)">{{confirmBtn}}</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script setup lang="ts">
import { mdiEye, mdiEyeOff } from '@mdi/js'
import type { BankResponse } from '~/composables/bankApi';
import type { BranchResponse } from '~/composables/branchApi';

interface Props {
	title: string
	message: string
	cancelBtn: string
	confirmBtn: string
	colorCancel: "primary" | "secondary" | "error" | "warning" | "info" | "success"
	colorConfirm: "primary" | "secondary" | "error" | "warning" | "info" | "success"
}

const alert = ref<any>(null)
const postForm = ref<any>(null)
const rules = useRules()

// ダイアログの表示・非表示のコントロール
const dialog = ref<boolean>(false)

const selectedAccountType = ref<string | null>(null)
const accountNumber = ref<string | null>(null)
const secretNumber = ref<string | null>(null)
const showPasswords = ref<boolean>(false)

let selectedBank = ref<number | null>(null)
let selectedBranch = ref<number | null>(null)
let branches = ref<BranchResponse[] | null>(null)
let params: { banks: BankResponse[], branches: BranchResponse[]}

function open(v: { banks: BankResponse[], branches: BranchResponse[]}) {
	dialog.value = true // ダイアログを表示
	params = v
}

// 選択したbankIdによるbranchesフィルター処理
async function filterBranchesByBankId(bankId: number | null) {
	// bankIdにnullが渡された時（selectedBankがクリアされた時）は選択されているbranchと選択肢をリセット
	if (bankId == null) {
		branches.value = null
		selectedBranch.value = null
	}
	if (bankId != null) {
		branches.value = params.branches.filter((branch) => branch.bank_id == bankId)
	}
}

async function confirm(confirm: boolean) {
	if (confirm==true) {
		const { valid: postFormValid } = await postForm.value.validate()
		if (!postFormValid) {
			return
		}
	}
	let params: any = {
		selectedBranch: selectedBranch.value,
		selectedAccountType: selectedAccountType.value,
		accountNumber: accountNumber.value,
		secretNumber: secretNumber.value
	}
	dialog.value = false
	branches.value = null // branchの選択肢をリセット
	postForm.value.reset() // フォームに入力した値をリセット
	emit(
		"confirm",
		confirm,
		params
	)
}

// propsを定義
const props = withDefaults(defineProps<Props>(), {
	title: "",
	cancelBtn: "Cancel",
	confirmBtn: "OK",
	colorCancel: "primary",
	colorConfirm: "error",
})

// イベントを定義
const emit = defineEmits<{
	confirm: [confirm: boolean, params: any]
}>()

// 明示的にopen()を公開
defineExpose({
	open: open,
})

// selectedBankのitem-valueが変更された時、bankに紐づくbranchを抽出
watch(selectedBank, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    filterBranchesByBankId(newValue)
  }
});
</script>