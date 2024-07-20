<template>
  <v-container class="py-8 px-6" fluid >
    <div>
      <Alert ref="alert" />
      <div class="mb-3 d-flex align-center">
        <div class="text-h4 mr-5">銀行口座 情報一覧</div>
        <div>
          <v-btn icon flat
            @click="createDialog.open({
              banks: banks,
              branches: branches,
            })">
            <v-icon size="x-large" color="primary" :icon="mdiPlusCircle"></v-icon>
            <v-tooltip
              activator="parent"
              location="end"
            >新規登録</v-tooltip>
          </v-btn>
        </div>
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
  </v-container>

  <!-- 削除確認ダイアログ -->
  <ConfirmDialog
    title="口座情報の削除"
    message="本当に削除しますか"
    confirmBtn="削除"
    cancelBtn="キャンセル"
    colorCancel="primary"
    colorConfirm="error"
    ref="confirmDeletion"
    @confirm="deleteAccountInfo">
  </ConfirmDialog>

  <!-- 新規作成ダイアログ -->
  <CreateDialog
    title="銀行口座の新規登録"
    message="必要事項を入力してください"
    confirmBtn="登録"
    cancelBtn="キャンセル"
    colorCancel="primary"
    colorConfirm="error"
    ref="createDialog"
    @confirm="createAccountInfo">
  </CreateDialog>
</template>

<script setup lang="ts">
import { mdiEye, mdiEyeOff, mdiDeleteForever, mdiPlusCircle } from '@mdi/js'

// 認証機能を実装するまで、userId=1とする
const userId = ref<number>(1)
// パスワードの表示・非表示のコントロール
const showPasswords = ref<{ [index: number]: boolean}>({})

const alert = ref<any>(null)
const confirmDeletion = ref<any>(null)
const createDialog = ref<any>(null)

// datetimeをYYYY/MM/DD形式に変換
function formatDate(datetime: string): string {
  let d = new Date(datetime)
  let year = d.getFullYear()
  let month = d.getMonth() + 1
  let day = d.getDate()
  return `${year}/${month}/${day}`
}

// 口座情報一覧取得
const { data: accountInfos, error: getAccountInfosError, refresh: refreshAccountInfos } = await useAccountInfoApi().getAll(userId.value)
if (!accountInfos.value || getAccountInfosError.value) {
  alert.value.error(getAccountInfosError.value)
}
if (accountInfos.value !== null) {
  accountInfos.value.forEach((ai) => {
    showPasswords.value[ai.id] = false
  })
}

// 銀行一覧取得
const { data: banks, error: getBanksError } = await useBankApi().getAll()
if (!banks.value || getBanksError.value) {
  alert.value.error(getBanksError.value)
}

// 支店一覧取得
const { data: branches, error: getBranchesError } = await useBranchApi().getAll()
if (!branches.value || getBranchesError.value) {
  alert.value.error(getBranchesError.value)
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

// 口座情報の作成処理
async function createAccountInfo(
  confirm: boolean,
  params: any,
) {
  if (!confirm) { return }
  const { data: postResponse, error: postError } = await useAccountInfoApi().post({
    branch_id: params.selectedBranch,
    user_id: userId.value,
    account_type: params.selectedAccountType,
    account_number: params.accountNumber,
    secret_number: params.secretNumber,
  })
  if (!postResponse.value || postError.value) {
    alert.value.error(postError.value)
    return
  }
  if (postResponse.value) {
    alert.value.success('口座情報の登録に成功しました')
  }
  refreshAccountInfos()
}
</script>