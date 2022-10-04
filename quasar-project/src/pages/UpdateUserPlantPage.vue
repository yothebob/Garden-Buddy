<template>
  <q-layout view="lHh Lpr lFf">
  <div class="app-content">
    <q-page-container>
      <router-view />
    </q-page-container>
    </div>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'UpdateUserPlantLayout',
})
</script>
