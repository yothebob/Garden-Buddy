<template>
    <q-layout view="lHh Lpr lFf">
	<div class="app-content">
    <q-page-container>
	
	<div>
	    <div style="padding-top:10%;padding-left:25%;">
		<q-btn @click="editAmendTrack" color="white" text-color="black" label="Edit Amend" />
		<q-btn @click="newAmendTrack" color="white" text-color="black" label="Add Amend" />
		<q-btn @click="listAmendTrack" color="white" text-color="black" label="List Amend" />
	    </div>
	    <div v-if="amendTrack == 'list'">
		<h3>Amends</h3><br/>
		<div v-for="am in _amends" class="q-pa-md">
		    <q-list dense bordered padding class="rounded-borders">
			<q-item>
			       <q-item-section>
				   <q-item-label>{{am.label}}</q-item-label>
				   <q-item-label caption lines="2">{{am.description}}</q-item-label>
			       </q-item-section>
			</q-item>

			<q-separator spaced inset />
		    </q-list>
		</div>
	    </div>
	    <div v-else-if="amendTrack == 'new'">
		<h3>Add New Amend</h3><br/>
		
		<q-input rounded outlined v-model="_amendName" label="Name" />
		<br/>
		
		<q-input
		    v-model="_amendDescription"
			     filled
		    autogrow
		    label="Description"
		/>
		<br/>
		
		<q-input rounded outlined v-model="_amendInfoUrl" label="Amend Info Url" />
		<br/>

		<q-btn @click="sendNewAmend" color="white" text-color="black" label="Add Amend" />
		
	    </div>
	    <div v-else>
		<h3>Edit Amend</h3><br/>
		<q-select rounded outlined v-model="_amendId" :options="_amends" emit-value label="Amend" /><br/>
		<q-input rounded outlined v-model="_amendName" label="Name" />
		<br/>
		
		<q-input
		    v-model="_amendDescription"
		    filled
		    autogrow
		    label="Description"
		/>
		<br/>
		
		<q-input rounded outlined v-model="_amendInfoUrl" label="Amend Info Url" />
		<br/>

		<q-btn @click="sendNewAmend" color="white" text-color="black" label="Add Amend" />
		
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
     name: 'NewAmendLayout',

     data: () => {
	 return {
	     amendTrack: null,
	     _amends: null,
	     _alert: null,
	     _message: null,
	     _amendName: null,
	     _amendId: null,
	     _amendDescription: null,
	     _amendInfoUrl: null
	 };
     },

     created() {
	 this.apiCheckLogin();
	 this.amendTrack = "list";
	 this.apiGetAmendData();
     },
     
     methods: {
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

	 editAmendTrack: function() {
	     this.amendTrack = "edit"
	 },
	 newAmendTrack: function() {
	     this.amendTrack = "new"
	 },
	 listAmendTrack: function() {
	     this.amendTrack = "list"
	 },
	 sendNewAmend: function () {
	     let _newAmenddata = {
		 "name": this._amendName,
		 "description": this._amendDescription, 
		 "info_url": this._amendInfoUrl,
	     };
	     
	     axios.post(`/api/amend/new`, _newAmenddata).then((response) => {
		 if (response.status === 200) {
		     
		     this._alert = true
		     this._message = "Save Successful"
		     this.amendTrack = "list"

		 } else {
		     this._alert = true
		     this._message = "Uh Oh Something went wrong!"
		     this.amendTrack = "list"

		 }
	     })
	 },
	 sendUpdateAmend: function () {
	     let _updateAmenddata = {
		 "amend_id": this._amendId,
		 "name": this._amendName,
		 "description": this._amendDescription, 
		 "info_url": this._amendInfoUrl,
	     };
	     
	     axios.post(`/api/amend/update`, _updateAmenddata).then((response) => {
		 if (response.status === 200) {
		     
		     this._alert = true
		     this._message = "Save Successful"
		     this.amendTrack = "list"
		 } else {
		     this._alert = true
		     this._message = "Uh Oh Something went wrong!"
		     this.amendTrack = "list"

		 }
	     })
	 },
	 apiGetAmendData: function () {
	     axios.get("/api/amends/").then((response) => {
		 if (response.status == 200) {
		     this._amends = response.data.amends
		 }
		 console.log(response);
	     }).catch(function (error) {
		 console.log(error.toJSON());
	     });
	 },

     }
 })
</script>
