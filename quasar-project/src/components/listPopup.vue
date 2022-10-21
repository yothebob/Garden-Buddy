<template>
  <div class="q-pa-md">
    <q-btn color="purple" @click="showNotif" label="Show Notifications" />
  </div>
</template>

<script>
import { useQuasar } from 'quasar'

export default {
  setup () {
    const $q = useQuasar()

    return {

	showNotif (itemJson) {
        $q.notify({
          message: `${itemJson.label}`,
          color: 'primary',
          avatar: 'https://cdn.quasar.dev/img/boy-avatar.png',
          actions: [
            { label: 'View', color: 'white', handler: () => { /* ... */ } },
            { label: 'Edit', color: 'yellow', handler: () => { /* ... */ } },
            { label: 'Delete', color: 'red', handler: () => { /* ... */ } }
          ]
        })
      }

    }

  }
}
</script>
