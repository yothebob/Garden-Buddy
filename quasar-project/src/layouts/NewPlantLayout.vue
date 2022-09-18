<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
	<div>
	    <h3>Add New Plant</h3><br/>
	    
	    <q-input rounded outlined v-model="_plantName" label="Plant Name" />
	    <br/>

	    <q-input
		v-model="_plantDescription"
		filled
		autogrow
		label="Description"
	    />
	    <br/>
	    
	    <q-input rounded outlined v-model="_plantInfoUrl" label="Plant Info Url" />
	    <br/>
	    
	    <q-btn @click="sendNewPlant" color="white" text-color="black" label="Add Plant" />

	</div>
	<div>
	    <div v-if="_alert == true">
		<q-dialog v-model="_alert">
		    <q-card>
			<q-card-section>
			    <div class="text-h6">Alert</div>
			</q-card-section>
			
			<q-card-section class="q-pt-none">
			    {{_message}}
			</q-card-section>
			
			<q-card-actions align="right">
			    <q-btn flat label="OK" color="primary" v-close-popup />
			</q-card-actions>
		    </q-card>
		</q-dialog>
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
     name: 'NewPlantLayout',

     data: () => {
	 return {
	     _alert: null,
	     _message: null,
	     _plantName: null,
	     _plantDescription: null,
	     _plantInfoUrl: null
	 };
     },

     created() {
     },
     methods: {
	 sendNewPlant: function () {
	     let _newPlantdata = {
		 "name": this._plantName,
		 "description": this._plantDescription, 
		 "info_url": this._plantInfoUrl 
	     };
	     
	     axios.post(`/api/plant/new`, _newPlantdata).then((response) => {
		 if (response.status === 200) {
		     
		     this._alert = true
		     this._message = "Save Successful"
		     // should I just have this on a generic plant page? 
		     /* window.location.href = '/home/' */
		 } else {
		     this._alert = true
		     this._message = "Uh Oh Something went wrong!"
		 }
	     })
	 },
     }
 })
</script>
