<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
	<div>
	    <h3>Login</h3><br/>
	    <!-- <label for="">Username</label><br/>
		 <input v-model="_username" name="username" type="text" /><br/> -->
	    <q-input rounded outlined v-model="_username" label="Username" />	    
	       <q-input rounded outlined v-model="_password" filled :type="isPwd ? 'password' : 'text'" label="Password">
		   <template v-slot:append>
		       <q-icon
			   :name="isPwd ? 'visibility_off' : 'visibility'"
			   class="cursor-pointer"
			   @click="isPwd = !isPwd"
		       />
		   </template>
	       </q-input>

	       <!-- <input v-model="_password" name="password" type="text" /><br/> -->
	       <q-btn @click="printme" color="white" text-color="black" label="Login" />
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
	     isPwd: true,
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
