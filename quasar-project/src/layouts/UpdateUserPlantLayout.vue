<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
	<q-toolbar>
            <q-btn
		flat
		dense
		round
		icon="menu"
		aria-label="Menu"
		@click="toggleLeftDrawer"
            />

            <q-toolbar-title>
		Garden Buddy
            </q-toolbar-title>

	</q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
	    GardenBuddy
        </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'

const linksList = [
  {
      title: 'Home',
      caption: 'My Home Page',
      icon: 'school',
      link: '/home/'
  },
  {
      title: 'Gardens',
      caption: 'View, create and update my gardens',
      icon: 'school',
      link: '/gardens/'
  },
  {
      title: 'My Plants',
      caption: 'Track any data you want with custom plants!',
      icon: 'code',
      link: '/userplants/'
  },
  {
      title: 'Harvests',
      caption: 'Add a new harvest for the day',
      icon: 'chat',
      link: '/harvests/'
  },
]

export default defineComponent({
  name: 'UpdateUserPlantLayout',

  components: {
    EssentialLink
  },

  setup () {
    const leftDrawerOpen = ref(false)

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
