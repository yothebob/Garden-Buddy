<template>
    <q-layout view="lHh Lpr lFf">
	<div class="app-content">
	    <q-page-container>
	  	<div style="padding-top:10%;padding-left:25%;">
		    <q-btn @click="editUserplantTrack" color="white" text-color="black" label="Edit User Plant" />
		    <q-btn @click="newUserplantTrack" color="white" text-color="black" label="Add User Plant" />
		    <q-btn @click="listUserplantTrack" color="white" text-color="black" label="List User Plant" />
		</div>

		<div v-if="userplantTrack == 'new'">
		    <h3>Add New Plant</h3><br/>
		    
		    <q-input rounded outlined v-model="_userPlantName" label="Plant Name" />
		    <br/>

		    <q-select rounded outlined v-model="_plant" @update:model-value="val => apiGetVarietyData(val)" :options="_plants" emit-value label="Plant Name" />
		    <br/>

		    <q-select rounded outlined v-model="_variety" :options="_varietys" emit-value label="Variety Name" />
		    <br/>
	      
	      <q-input rounded outlined v-model="_userPlantFootSize" label="Foot Size (1x1 == 1)" />
	      <br/>

	      <q-input
		  v-model="_userPlantDescription"
		  filled
		  autogrow
		  label="Description"
	      />
	      <br/>
	      <q-select rounded outlined v-model="_userPlantGarden" :options="_gardens" emit-value label="Garden" /><br/>
	      
	      <h5>Metadata</h5>
	      <q-item v-for="md in metadataFieldLength" :key="md">
		  <div>
		      <q-input rounded outlined v-model.string="metadataFields[md].name" label="Name" /><br/>
		      <q-input filled autogrow v-model.string="metadataFields[md].description" label="description" /><br/>
		      <q-select rounded outlined v-model.string="metadataFields[md].dataType" :options="_dataTypes" label="DataType" /><br/>
		      <q-btn  @click="addMetaDataField" color="white" text-color="black" label="Add Extra DataField" />
		  </div>
	      </q-item>

	      
	      <q-btn @click="sendNewUserPlant" color="white" text-color="black" label="Add Plant" />

		</div>
		<div v-if="userplantTrack == 'edit'">
		    <h3>Edit User Plant</h3><br/>
		    <q-select rounded outlined v-model.string="_userPlantId" :options="_userPlants" label="UserPlant to Edit" emit-value /><br/>

		    <q-select rounded outlined v-model="_plant" @update:model-value="val => apiGetVarietyData(val)" :options="_plants" emit-value label="Plant Name" />
		    <br/>

		    <q-select rounded outlined v-model="_variety" :options="_varietys" emit-value label="Variety Name" />
		    <br/>
		    
		    <q-input rounded outlined v-model="_userPlantName" label="Plant Name" />
	      <br/>
	      <q-input rounded outlined v-model="_userPlantFootSize" label="Foot Size (1x1 == 1)" />
	      <br/>

	      <q-input
		  v-model="_userPlantDescription"
		  filled
		  autogrow
		  label="Description"
	      />
	      <br/>
	      <q-select rounded outlined v-model="_userPlantGarden" :options="_gardens" emit-value label="Garden" /><br/>
	      
	      <h5>Metadata</h5>
	      <q-item v-for="md in metadataFieldLength" :key="md">
		  <div>
		      <q-input rounded outlined v-model.string="metadataFields[md].name" label="Name" /><br/>
		      <q-input filled autogrow v-model.string="metadataFields[md].description" label="description" /><br/>
		      <q-select rounded outlined v-model.string="metadataFields[md].dataType" :options="_dataTypes" label="DataType" /><br/>
		      <q-btn  @click="addMetaDataField" color="white" text-color="black" label="Add Extra DataField" />
		  </div>
	      </q-item>

	      
	      <q-btn @click="sendEditUserPlant" color="white" text-color="black" label="Add Plant" />

		</div>
		<div>
		<div v-if="userplantTrack == 'list'">
		    <div v-for="ups in _userPlants" class="q-pa-md">
			<q-list dense bordered padding class="rounded-borders">
			    <q-item>
				<q-item-section>
				    <q-item-label>{{ups.label}}</q-item-label>
				    <q-item-label caption lines="2">{{ups.description}}</q-item-label>
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
     name: 'NewUserPlantLayout',
     data: () => {
	 return {
	     _alert: null,
	     userplantTrack: null,
	     _userPlantName: null,
	     _userPlantId: null,
	     _plant: null,
	     _plants: null,
	     _variety: null,
	     _varietys: null,
	     _userPlants: null,
	     _userPlantFootSize: null,
	     _userPlantGarden: null,
	     _userPlantDescription: null,
	     _message: null,
	     _userId: null,
	     metadataFields: [],
	     metadataFieldLength: null,
	     _dataTypes: null,
	 };
     },
     created() {
	 this._dataTypes = [
	     "bool",
	     "int",
	     "text",
	     "textarea",
	 ];
	 this.apiCheckLogin();
	 this.apiGetPlantData();
	 this.metadataFieldLength = 0;
	 this.addMetaDataField();
	 this.metadataFields.push({
	     "name": "",
	     "dataType": "",
	     "description": "",
	 })
	 this._alert = false;
	 this.apiGetUserData();
	 this.userplantTrack = "list";
     },
     methods: {
	 editUserplantTrack: function () {
	     this.userplantTrack = "edit"
	 },	 
	 newUserplantTrack: function () {
	     this.userplantTrack = "new"
	 },
	 listUserplantTrack: function () {
	     this.userplantTrack = "list"
	 },
	 apiGetPlantData: function () {
	     axios.get("/api/plants/").then((response) => {
		 if (response.status == 200) {
		     this._plants = response.data.plants
		 }
		 console.log(response);
	     })
	 },
	 apiGetVarietyData: function (given_plant_id) {
	     axios.get(`/api/varietys/?plant_id=${given_plant_id}`).then((response) => {
		 console.log(response);
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
	 addMetaDataField: function() {
	     this.metadataFieldLength = this.metadataFieldLength + 1;
	     this.metadataFields.push({
		 "name": "",
		 "dataType": "",
		 "description": "",
	     })
	 },
	 apiGetUserData: function () {
	     axios.get("/api/user/").then((response) => {
		 console.log(response)
		 if (response.status == 200) {
		     this._userId = response.data.user_id;
		     this._gardens = response.data.gardens;
		     this._userPlants = response.data.user_plants;
		 }
	     })
	 },
	 sendNewUserPlant: function () {
	     let date = new Date();
	     let dateString = String(((date.getMonth() > 8) ? (date.getMonth() + 1) : ('0' + (date.getMonth() + 1))) + '/' + ((date.getDate() > 9) ? date.getDate() : ('0' + date.getDate())) + '/' + date.getFullYear())
	     let sendMetadata = this.metadataFields.shift()
	     let sendData = {
		 "user_id": this._userId,
		 "plant_id": this._plant,
		 "variety_id": this._variety,
		 "garden_id": this._userPlantGarden,
		 "date": dateString,
		 "name": this._userPlantName,
		 "foot_size": this._userPlantFootSize,
		 "description": this._userPlantDescription,
		 "metadata": this.metadataFields
	     };
	     
	     axios.post("/api/userplant/new",sendData).then((response) => {
		 console.log(response)
		 if (response.status == 200) {
		     this._alert = true;
		     this._message = response.data.message
		     this.userplantTrack = "list"
		 }
	     })
	 },
	 sendEditUserPlant: function () {
	     let date = new Date();
	     let dateString = String(((date.getMonth() > 8) ? (date.getMonth() + 1) : ('0' + (date.getMonth() + 1))) + '/' + ((date.getDate() > 9) ? date.getDate() : ('0' + date.getDate())) + '/' + date.getFullYear())
	     let sendMetadata = this.metadataFields.shift()
	     let sendData = {
		 "userplant_id": this._userPlantId,
		 "user_id": this._userId,
		 "plant_id": this._plant,
		 "variety_id": this._variety,
		 "garden_id": this._userPlantGarden,
		 "date": dateString,
		 "name": this._userPlantName,
		 "foot_size": this._userPlantFootSize,
		 "description": this._userPlantDescription,
		 "metadata": this.metadataFields
	     };
	     
	     axios.post("/api/userplant/update",sendData).then((response) => {
		 console.log(response)
		 if (response.status == 200) {
		     this._alert = true;
		     this._message = response.data.message
		     this.userplantTrack = "list"
		     window.location.reload()
		 }
	     })
	 },
     },

 })
</script>
