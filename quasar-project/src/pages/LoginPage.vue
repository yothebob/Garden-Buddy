<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
	<div class="app-content">
	    <h3>Login</h3><br/>
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
	       <div style="padding-left:45%;" >
		   <q-btn @click="apiLoginUser" color="white" text-color="black" label="Login" /><br/>
		   <a style="padding: 10px;" href="/create/"> Create User</a>
	       </div>
	       <div class="message" v-if="_message != null"> {{_message}} </div>
	</div>
	<router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
 import { defineComponent, ref } from 'vue'
 import axios from 'axios'
 /* import VueCryptojs from 'vue-cryptojs' */
 /* https://github.com/tpenaranda/vue-cryptojs */
 
 export default defineComponent({
     name: 'LoginLayout',
     data: () => {
	 return {
	     isPwd: true,
	     "_username": null,
	     "_password": null,
	     "apiSecret": "",
	     "_message": null
	 };
     },
     created() {
	 /* this.apiSecret = "usethisfordevenvonly" */
     },
     components: {
     },
     methods: {
	 apiLoginUser: function () {
	     /* TODO add jwt */
	     /* get crypto for online? */
	     /* const msg = Buffer.from(this._password).toString('base64')
		const hash = crypto.createHmac('sha256', this.apiSecret).update(msg).digest('base64') */
	     /* axios.post(`/api/login/?username=${this._username}&password=${hash}`, {}).then((response) => { */
	     axios.post(`/api/login/?username=${this._username}&password=${this._password}`, {}).then((response) => {
		 if (response.data.status === 200) {
		     window.location.href = '/home/'
		 }else {
		     this._message = response.data.message
		 }
	     })
	 }
     }
 })
</script>
<style>
 div.message {
     background: #ffec7b;
     border-radius: 5px;
     width: 50%;
     padding-left: 25%;
     margin-left: 25%;
     font-size: 1.5rem;
     padding: 10px;
     margin-top: 1em;}
</style>
