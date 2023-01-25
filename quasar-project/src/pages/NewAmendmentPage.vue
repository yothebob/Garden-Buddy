<template>
    <q-layout view="lHh Lpr lFf">
	<div class="app-content">
    <q-page-container>
	
	<div>
	    <div style="padding-top:10%;padding-left:25%;">
		<q-btn @click="newAmendmentTrack" color="white" text-color="black" label="Add Amendment" />
		<q-btn @click="listAmendmentTrack" color="white" text-color="black" label="List Amendment" />
	    </div>
	    <div v-if="amendmentTrack == 'list'">
		<h3>Amendments</h3><br/>
		<div v-for="am in _amendments" class="q-pa-md">
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
	    <div v-else-if="amendmentTrack == 'new'">
		<h3>Add New Amendment</h3><br/>
		
		<q-input rounded outlined v-model="_amendmentName" label="Name" />
		<br/>
		
		<q-input
		    v-model="_amendmentDescription"
			     filled
		    autogrow
		    label="Description"
		/>
		<br/>
		
		<q-input rounded outlined v-model="_amendmentInfoUrl" label="Amendment Info Url" />
		<br/>

		<q-btn @click="sendNewAmendment" color="white" text-color="black" label="Add Amendment" />
		
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
     name: 'NewAmendmentLayout',

     data: () => {
	 return {
	     amendmentTrack: null,
	     _amendments: null,
	     _alert: null,
	     _message: null,
	     _amendmentName: null,
	     _amendmentId: null,
	     _amendmentDescription: null,
	     _amendmentInfoUrl: null
	 };
     },

     created() {
	 this.apiCheckLogin();
	 this.amendmentTrack = "list";
	 this.apiGetAmendmentData();
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

	 newAmendmentTrack: function() {
	     this.amendmentTrack = "new"
	 },
	 listAmendmentTrack: function() {
	     this.amendmentTrack = "list"
	 },
	 sendNewAmendment: function () {
	     let _newAmendmentdata = {
		 "name": this._amendmentName,
		 "description": this._amendmentDescription, 
		 "info_url": this._amendmentInfoUrl,
	     };
	     
	     axios.post(`/api/amendment/new`, _newAmendmentdata).then((response) => {
		 if (response.status === 200) {
		     
		     this._alert = true
		     this._message = "Save Successful"
		     this.amendmentTrack = "list"

		 } else {
		     this._alert = true
		     this._message = "Uh Oh Something went wrong!"
		     this.amendmentTrack = "list"

		 }
	     })
	 },

	 apiGetAmendmentData: function () {
	     axios.get("/api/amendments/").then((response) => {
		 if (response.status == 200) {
		     this._amendments = response.data.amendments
		 }
		 console.log(response);
	     }).catch(function (error) {
		 console.log(error.toJSON());
	     });
	 },
	 apiGetUserData: function () {
	     /* TODO add jwt */
	     // I think I can make an api call that checks the backend for user_id and passes that up
	     axios.get(`/api/user/`).then((response) => {
		 console.log(response);
		 if (response.status == 200) {
		     this._gardens = response.data.gardens;
		     this._userData = response.data;
		 }
	     })
	 },

     }
 })
</script>
