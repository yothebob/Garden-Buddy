<template>
    <q-layout view="lHh Lpr lFf">
	<q-page-container>
	    <div>
		<q-btn to="/plant/new/" label="Add a new Plant" outline color="green" /><br/>
		<q-btn to="/variety/new/" label="Add a new Variety" outline color="green" /><br/>
		<q-btn to="/api/logout/" label="Logout" outline color="yellow" /><br/>
	    </div>
	    <router-view />
	</q-page-container>
    </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'HomeLayout',
})
</script>
