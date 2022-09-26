<template>
    <router-view />
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
	<div>
            <EssentialLink
		v-for="link in essentialLinks"
		       :key="link.title"
		v-bind="link"
            />
	</div>
      </q-list>
    </q-drawer>
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
      link: '/garden/new/'
  },
  {
      title: 'Plants',
      caption: 'Read about new plants, Or add new plants!',
      icon: 'code',
      link: '/plant/new/'
  },
  {
      title: 'Varieties',
      caption: 'Check out new Varieties for your garden, Or add your own!',
      icon: 'code',
      link: '/variety/new/'
  },
  {
      title: 'My Plants',
      caption: 'Track any data you want with custom plants!',
      icon: 'code',
      link: '/userplant/new/'
  },
  {
      title: 'Harvests',
      caption: 'Add a new harvest for the day',
      icon: 'chat',
      link: '/harvest/new/'
  },
]

export default defineComponent({
  name: 'App',

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
