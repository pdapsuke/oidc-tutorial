<template>
  <div>
    <Alert ref="alert" />
    <div class="mb-3">
      <div class="text-h4">銀行口座 情報一覧</div>
    </div>
    <v-table>
      <thead>
        <tr>
          <th>ID</th>
          <th>銀行名</th>
          <th>支店名</th>
          <th>口座種別</th>
          <th>口座番号</th>
          <th>暗証番号</th>
          <th>登録日</th>
          <th>アクション</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ai in accountInfos" :key="ai.id">
          <td>{{ ai.id }}</td>
          <td>{{ ai.bank_name }}</td>
          <td>{{ ai.branch_name }}</td>
          <td>{{ ai.account_type }}</td>
          <td>{{ ai.account_number }}</td>
          <td>
            <v-text-field
              :model-value="ai.secret_number"
              :prepend-icon="showPasswords[ai.id] ? mdiEye : mdiEyeOff"
              :type="showPasswords[ai.id] ? 'text' : 'password'"
              @click:prepend="showPasswords[ai.id] = !showPasswords[ai.id]"
              variant="plain"
              readonly
            ></v-text-field>
          </td>
          <td>{{ formatDate(ai.created) }}</td>
          <td>
            <v-btn icon flat
              @click="confirmDeletion.open({
                userId: userId,
                accountInfoId: ai.id,
              })"
            ><v-icon color="error" :icon="mdiDeleteForever"></v-icon>
            </v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>

  <!-- 削除確認ダイアログ -->
  <ConfirmDialog
    title="口座情報の削除"
    message="本当に削除しますか"
    confirmBtn="削除"
    cancelBtn="キャンセル"
    colorCancel="black"
    colorConfirm="error"
    ref="confirmDeletion"
    @confirm="deleteAccountInfo">
  </ConfirmDialog>

</template>

<script setup lang="ts">
import { mdiEye, mdiEyeOff, mdiDeleteForever } from '@mdi/js'

// 認証機能を実装するまで、userId=1とする
const userId = ref<number>(1)
const showPasswords = ref<{ [index: number]: boolean}>({})

const alert = ref<any>(null)
const confirmDeletion = ref<any>(null)

function formatDate(datetime: string): string {
  let d = new Date(datetime)
  let year = d.getFullYear()
  let month = d.getMonth() + 1
  let day = d.getDate()
  return `${year}/${month}/${day}`
}

// アイテム一覧取得
const { data: accountInfos, error: getAccountInfosError, refresh: refreshAccountInfos } = await useAccountInfoApi().getAll(userId.value)
if (!accountInfos.value || getAccountInfosError.value) {
  alert.value.error(getAccountInfosError.value)
}
if (accountInfos.value !== null) {
  accountInfos.value.forEach((ai) => {
    showPasswords.value[ai.id] = false
  })
}

// 口座情報の削除処理
async function deleteAccountInfo(confirm: boolean, params: {userId: number, accountInfoId: number}) {
  if (!confirm) { return }
  const { error: deleteAccountInfoError } = await useAccountInfoApi().delete(params.accountInfoId, params.userId)
  if (deleteAccountInfoError.value) {
    alert.value.error(deleteAccountInfoError.value)
    return
  }
  alert.value.success(`口座情報（id=${params.accountInfoId}）の削除に成功しました`)
  await refreshAccountInfos()
}

</script>