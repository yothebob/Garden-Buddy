<template>
    <q-layout view="lHh Lpr lFf">
	<div class="app-content">
    <q-page-container>
	
	<div>
	    <div style="padding-top:10%;padding-left:25%;">
		<q-btn @click="editPlantTrack" color="white" text-color="black" label="Edit Plant" />
		<q-btn @click="newPlantTrack" color="white" text-color="black" label="Add Plant" />
		<q-btn @click="listPlantTrack" color="white" text-color="black" label="List Plant" />
	    </div>
	    <div v-if="plantTrack == 'list'">
		<h3>Plants</h3><br/>
		<div v-for="pp in _plants" class="q-pa-md">
		    <q-list dense bordered padding class="rounded-borders">
			<q-item >
			       <q-item-section>
				   <q-item-label @click="goToPlantPage(pp.value)">{{pp.label}}</q-item-label>
				   <q-item-label caption lines="2">{{pp.description}}</q-item-label>
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
	    <div v-else-if="plantTrack == 'new'">
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

		<q-input rounded outlined v-model="_plantFootSize" label="Plant Foot Size" />
		<br/>
		
		<q-btn @click="sendNewPlant" color="white" text-color="black" label="Add Plant" />
		
	    </div>
	    <div v-else>
		<h3>Edit Plant</h3><br/>
		<q-select rounded outlined v-model="_plantId" :options="_plants" emit-value label="Plant" /><br/>
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

		<q-input rounded outlined v-model="_plantFootSize" label="Plant Foot Size" />
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
     name: 'NewPlantLayout',

     data: () => {
	 return {
	     _plantFootSize: null,
	     plantTrack: null,
	     _plants: null,
	     _alert: null,
	     _message: null,
	     _plantName: null,
	     _plantId: null,
	     _plantDescription: null,
	     _plantInfoUrl: null
	 };
     },

     created() {
	 this.apiCheckLogin();
	 this.plantTrack = "list";
	 this.apiGetPlantData();
     },
     
     methods: {
	 goToPlantPage: function (pid) {
	     window.location = `/plant/${pid}/`
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

	 editPlantTrack: function() {
	     this.plantTrack = "edit"
	 },
	 newPlantTrack: function() {
	     this.plantTrack = "new"
	 },
	 listPlantTrack: function() {
	     this.plantTrack = "list"
	 },
	 sendNewPlant: function () {
	     let _newPlantdata = {
		 "name": this._plantName,
		 "description": this._plantDescription, 
		 "info_url": this._plantInfoUrl,
		 "foot_size": this._plantFootSize
	     };
	     
	     axios.post(`/api/plant/new`, _newPlantdata).then((response) => {
		 if (response.status === 200) {
		     
		     this._alert = true
		     this._message = "Save Successful"
		     this.plantTrack = "list"

		     // should I just have this on a generic plant page? 
		     /* window.location.href = '/home/' */
		 } else {
		     this._alert = true
		     this._message = "Uh Oh Something went wrong!"
		     this.plantTrack = "list"

		 }
	     })
	 },
	 sendUpdatePlant: function () {
	     let _updatePlantdata = {
		 "plant_id": this._plantName,
		 "name": this._plantName,
		 "description": this._plantDescription, 
		 "info_url": this._plantInfoUrl,
	     };
	     
	     axios.post(`/api/plant/update`, _updatePlantdata).then((response) => {
		 if (response.status === 200) {
		     
		     this._alert = true
		     this._message = "Save Successful"
		     this.plantTrack = "list"
		 } else {
		     this._alert = true
		     this._message = "Uh Oh Something went wrong!"
		     this.plantTrack = "list"

		 }
	     })
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
