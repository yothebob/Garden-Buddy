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
	<div style="position:relative;padding-left:45%;">
	    <h3>Login</h3><br/>
	    <label for="">Username</label><br/>
	    <input v-model="_username" name="username" type="text" /><br/>
	    <label for="">Password</label><br/>
	    <input v-model="_password" name="password" type="text" /><br/>
	    <button @click="printme">SUBMIT</button><br/>
	</div>
	<router-view />
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
	     axios.post(`/api/login/?username=${this._username}&password=${this._password}`, {}).then((response) => {
		 if (response.status === 200) {
		     window.location.href = '/home/'
		 }
	     })
	 }
     }
 })
</script>
