<template>
    <q-layout view="lHh Lpr lFf">
	<div class="app-content">
      <q-page-container>
	  <div>
	      <h3>Add New Plant</h3><br/>
	      
	      <q-input rounded outlined v-model="_userPlantName" label="Plant Name" />
	      <br/>

	      <q-input
		  v-model="_userPlantDescription"
		  filled
		  autogrow
		  label="Description"
	      />
	      <br/>
	      <q-select rounded outlined v-model="_userPlantGarden" :options="_gardens" emit-value label="Garden" /><br/>
	      
	      
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
	     _userPlantGarden: null,
	     _userPlantDescription: null,
	     _message: null,
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
		     this._gardens = response.data.gardens;
		 }
	     })
	 },
	 sendNewUserPlant: function () {
	     let date = new Date();
	     let dateString = String(((date.getMonth() > 8) ? (date.getMonth() + 1) : ('0' + (date.getMonth() + 1))) + '/' + ((date.getDate() > 9) ? date.getDate() : ('0' + date.getDate())) + '/' + date.getFullYear())
	     let sendData = {
		 "user_id": 1,
		 "plant_id": 2,
		 "variety_id": 2,
		 "garden_id": this._userPlantGarden,
		 "date": dateString,
		 "name": this._userPlantName,
		 "description": this._userPlantDescription,
		 "metadata": this.metadataFields//.shift()
	     };
	     
	     axios.post("/api/userplant/new",sendData).then((response) => {
		 console.log(response)
		 if (response.status == 200) {
		     this._alert = "save Successful"
		 }
	     })
	 },
	 sendEditGarden: function () {
	     console.log("hello")
	 },
     },

 })
</script>
