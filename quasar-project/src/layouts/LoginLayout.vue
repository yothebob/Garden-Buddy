<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
Garden Buddy
        </q-toolbar-title>

      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
      <div>
	  <input v-model="_username" name="username" type="text" />
	  <input v-model="_password" name="password" type="text" />
	  <button @click="printme">SUBMIT</button>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script>
 import { defineComponent, ref } from 'vue'
 import axios from 'axios'
 
 export default defineComponent({
     name: 'LoginLayout',
     data: () => {
	 return {
	     "_username": null,
	     "_password": null
	 };
     },
     components: {
     },
     methods: {
	 printme: function () {
	     /* TODO add jwt */
	     axios.post(`:5000/login/?username=${this._username}&password=${this._password}`, {}).then((response) => {
		 if (response.status === 200) {
		     window.location.href = '/home/'
		 }
	     })
	 }
     }
 })
</script>
