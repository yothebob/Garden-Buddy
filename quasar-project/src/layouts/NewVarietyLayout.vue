<template>
  <q-layout view="lHh Lpr lFf">

    <q-page-container>
	<div>
	    <h3>Add New Variety</h3>
	    <br/>

	    <q-select rounded outlined v-model="_plantId" :options="_plants" emit-value label="Plant Name" />
	    <br/>

	    <q-input rounded outlined v-model="_varietyName" label="Variety Name" />
	    <br/>

	    <q-input
		v-model="_varietyDescription"
		filled
		autogrow
		label="Description"
	    />
	    <br/>
	    
	    <q-input rounded outlined v-model="_varietyInfoUrl" label="Variety Info Url" />
	    <br/>
	    <q-btn @click="sendNewVariety" color="white" text-color="black" label="Add Variety" />
	</div>
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
	<router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
 import { defineComponent, ref } from 'vue'
 import axios from 'axios'

 export default defineComponent({
     name: 'NewVarietyLayout',

     data: () => {
	 return {
	     _alert: false,
	     _message: null,
	     _plants: [],
	     _plantId: null,
	     _varietyName: null,
	     _varietyDescription: null,
	     _varietyInfoUrl: null
	 };
     },

     created() {
	 this.apiGetPlantData();
     },
     
     methods: {

	 sendNewVariety: function () {
	     let _newVarietyData = {
		 "plant_id": this._plantId,
		 "name": this._varietyName,
		 "description": this._varietyDescription, 
		 "info_url": this._varietyInfoUrl 
	     };
	     
	     console.log(_newVarietyData);

	     axios.post(`/api/variety/new`, _newVarietyData).then((response) => {
		 if (response.status === 200) {
		     console.log(response)
		     this._message = 'Save Successful.'
		     this._alert = true;
		 } else {
		     this._alert = true;
		     this._message = 'Uh Oh Something went wrong!'
		 }
	     }).catch(function (error) {
		 console.log(error.toJSON());
		 this._alert = true;
		 this._message = 'Uh Oh Something went wrong!'
	     });
	 },

	 apiGetPlantData: function () {
	     axios.get("/api/plants/").then((response) => {
		 if (response.status == 200) {
		     this._plants = response.data.plants
		 }
		 console.log(response);
	     }).catch(function (error) {
		 console.log(error.toJSON());
	     });
	 },

     }

 })
</script>
