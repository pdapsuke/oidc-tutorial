<template>
	<!--  -->
	<v-dialog v-model="dialog" persistent max-width="400px">
		<v-card>
			<v-card-title>
				<span class="headline">{{ props.title }}</span>
			</v-card-title>
			<v-card-text>
				{{ props.message }}
			</v-card-text>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn :color="props.colorCancel" @click="confirm(false)">{{ cancelBtn }}</v-btn>
				<v-btn :color="props.colorConfirm" @click="confirm(true)">{{ confirmBtn }}</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script setup lang="ts">
interface Props {
	title: string
	message: string
	cancelBtn: string
	confirmBtn: string
	colorCancel: "primary" | "secondary" | "error" | "warning" | "info" | "success"
	colorConfirm: "primary" | "secondary" | "error" | "warning" | "info" | "success"
}

// ダイアログの表示・非表示のコントロール
const dialog = ref<boolean>(false)
// コンポーネントの呼び出し元から受け取るパラメータ
let params: any = {}

// 親コンポーネントがダイアログを開くときに呼び出す関数
function open(v: any = {}) {
	dialog.value = true // ダイアログを表示
	params = v
}

// ダイアログのボタンがクリックされたときに呼び出す関数
function confirm(confirm: boolean) {
	dialog.value = false
	// confirmイベントを発生
	emit("confirm", confirm, params)
}

const props = withDefaults(defineProps<Props>(), {
	title: "",
	message: "",
	cancelBtn: "Cancel",
	confirmBtn: "OK",
	colorCancel: "primary",
	colorConfirm: "error",
})

// イベントを発生させたいときは、defineEmitsを使う。
const emit = defineEmits<{
	// confirmイベントを定義
	confirm: [ok: boolean, params: any]
}>()

// 明示的にopen()を公開
defineExpose({
	open: open,
})
</script>
