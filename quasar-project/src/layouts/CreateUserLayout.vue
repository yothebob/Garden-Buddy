<template>
  <q-layout view="lHh Lpr lFf">
      <q-page-container>
	  <div class="app-content">
	<div>
	    <h3>Create New User</h3><br/>
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
	       <q-input rounded outlined v-model="_passwordAgain" filled :type="isPwd ? 'password' : 'text'" label="Password Again"/>
		   <div class="message" v-if="_message != null"> {{_message}} </div>

		   <q-btn @click="createUser" color="white" text-color="black" label="Create user" />
			</div>
	  </div>
	  <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
 import { defineComponent, ref } from 'vue'
 import axios from 'axios'
 
 export default defineComponent({
     name: 'CreateUserLayout',
     data: () => {
	 return {
	     isPwd: true,
	     "_username": null,
	     "_password": null,
	     "_passwordAgain": null,
	     "_message": null,
	 };
     },
     components: {
     },
     methods: {
	 createUser: function () {
	     /* TODO add jwt */
	     /* this._message = null; */
	     if (this._password == this._passwordAgain){
		 axios.post(`/api/create-user/`, {
		     "username": this._username,
		     "password": this._password
		 }).then((response) => {
		     console.log(response.data)
		     console.log(response.data.status)
		     if (response.data.status != 500) {
			 console.log(response.data.status)
			 this._message = response.data.message;
			 window.location.href = '/login/'
		     } else {
			 this._message = response.data.message;
		     }
		 })
	     } else {
		 this._message = "Passwords Don't Match."
	     }
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
