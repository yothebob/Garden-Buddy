<template>
  <q-layout view="lHh Lpr lFf">
      <div class="app-content">
	  <q-page-container>
	      <div style="padding-top:10%;padding-left:25%;">
		  <q-btn @click="editVarietyTrack" color="white" text-color="black" label="Edit Variety" />
		  <q-btn @click="newVarietyTrack" color="white" text-color="black" label="Add Variety" />
		  <q-btn @click="listVarietyTrack" color="white" text-color="black" label="List Variety" />
	      </div>

	      <div v-if="varietyTrack == 'new'">
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
	<div v-else-if="varietyTrack == 'edit'">
	    <h3>Edit Variety</h3>
	    <br/>

	    <q-select rounded outlined v-model="_plantId" @update:model-value="val => apiGetVarietyData(val)" :options="_plants" emit-value label="Plant Name" />
	    <br/>

	    <q-select rounded outlined v-model="_editVariety" :options="_varietys" emit-value label="Variety Name" />
	    <br/>

	    <q-input rounded outlined v-model="_varietyName" label=" Updated Variety Name" />
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
	<div v-else>
	    <h3>Varieties</h3>
	    <br/>
	    <q-select rounded outlined v-model="_plantId" @update:model-value="val => apiGetVarietyData(val)" :options="_plants" emit-value label="Plant Name" />
	    <br/>
	    <div v-for="vv in _varietys" class="q-pa-md">
		<q-list dense bordered padding class="rounded-borders">
		    <q-item>
			<q-item-section>
			    <q-item-label>{{vv.label}}</q-item-label>
			    <q-item-label caption lines="2">{{vv.description}}</q-item-label>
			</q-item-section>
			
			<q-item-section side top>
			    <q-item-label caption>High Yielder</q-item-label>
			    <q-icon name="star" color="yellow" />
			</q-item-section>
		    </q-item>

		    <q-separator spaced inset />
		</q-list>
		    </div>
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
      </div>
  </q-layout>
</template>

<script>
 import { defineComponent, ref } from 'vue'
 import axios from 'axios'

 export default defineComponent({
     name: 'NewVarietyLayout',

     data: () => {
	 return {
	     varietyTrack: null,
	     _varietys: null,
	     _alert: false,
	     _message: null,
	     _plants: [],
	     _plantId: null,
	     _editVariety: null,
	     _varietyName: null,
	     _varietyDescription: null,
	     _varietyInfoUrl: null
	 };
     },

     created() {
	 this.varietyTrack = "list";
	 this.apiCheckLogin();
	 this.apiGetPlantData();
     },
     
     methods: {
	 editVarietyTrack: function () {
	     this.varietyTrack = "edit"
	 },	 
	 newVarietyTrack: function () {
	     this.varietyTrack = "new"
	 },
	 listVarietyTrack: function () {
	     this.varietyTrack = "list"
	 },
	 apiGetVarietyData: function (given_plant_id) {
	     axios.get(`/api/varietys/?plant_id=${given_plant_id}`).then((response) => {
		 this._varietys = response.data.varietys 
	     })
	 },
	 apiCheckLogin: function () {
	     axios.get("/api/who-am-i/").then((response) => {
		 console.log(response)
		 if (response.status == 200 && response.data.status == 200) {
		     this._logged_in = true;
		     console.log(this._harvestData)
		 } else {
		     this._logged_in = false;
		     window.location.href = "/login";
		 }
	     })
	 },
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
