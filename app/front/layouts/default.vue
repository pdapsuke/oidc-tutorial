<template>
  <v-app>
    <!-- ヘッダー >>> -->
    <v-app-bar color="primary" :elevation="2">
      <v-app-bar-title>
        <div @click="useRouter().push('/')" style="cursor: pointer;">Account Manager</div>
      </v-app-bar-title>
    </v-app-bar>
    <!-- <<< ヘッダー -->

    <!-- コンテンツ >>> -->
    <v-main>
      <slot />
    </v-main>
    <!-- <<< コンテンツ -->

    <!-- フッター >>> -->
    <v-footer class="footer justify-center">
      <div>&copy; 2024 Account Manager</div>
    </v-footer>
    <!-- <<< フッター -->
  </v-app>
</template>

<script setup lang="ts">
</script>

<style lang="scss">
.footer {
  width: 100%;
  position: absolute;
  bottom: 0;
}
</style>