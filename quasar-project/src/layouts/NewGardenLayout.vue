<template>
  <q-layout view="lHh Lpr lFf">
      <div class="app-content">
	  <q-page-container>

	      <div>
		  <div style="padding-top:10%;padding-left:25%;">
		      <q-btn @click="editGardenTrack" color="white" text-color="black" label="Edit Garden" />
		      <q-btn @click="newGardenTrack" color="white" text-color="black" label="Add Garden" />
		      <q-btn @click="listGardenTrack" color="white" text-color="black" label="List Garden" />
		  </div>
		  <div v-if="gardenTrack == 'list'">
		      <h3>Plants</h3><br/>
		      <div v-for="gg in _gardens" class="q-pa-md">
			  <q-list dense bordered padding class="rounded-borders">
			      <q-item>
				  <q-item-section>
				      <q-item-label>{{gg.name}}</q-item-label>
				      <q-item-label caption lines="2">{{gg.description}}</q-item-label>
				  </q-item-section>
				  
				  <q-item-section side top>
				      <q-item-label caption>garden</q-item-label>
				      <q-icon name="star" color="yellow" />
				  </q-item-section>
			      </q-item>

			      <q-separator spaced inset />
			  </q-list>
		      </div>
		  </div>
		  <div v-else-if="gardenTrack == 'new'">
		      <h3>Add New Garden</h3><br/>
		      
		      <q-input rounded outlined v-model="_gardenName" label="Garden Name" />
		      <br/>
		      
		      <q-input
			  v-model="_gardenDescription"
			  filled
			  autogrow
			  label="Description"
		      />
		      <br/>
		      
		      <q-btn @click="sendNewGarden" color="white" text-color="black" label="Add Garden" />
		      
		  </div>
		  <div v-else>
		  <h3>Edit Garden</h3><br/>
		  
		  <q-input rounded outlined v-model="_gardenName" label="Garden Name" />
		  <br/>
		  
		  <q-input
		      v-model="_gardenDescription"
		      filled
		      autogrow
		      label="Description"
		  />
		  <br/>
		  
		  <q-btn @click="sendEditGarden" color="white" text-color="black" label="Add Garden" />
		  
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
     name: 'NewGardenLayout',
     data: () => {
	 return {
	     gardenTrack: null,
	     _gardens: null,
	     _alert: null,
	     _message: null,
	     _gardenName: null,
	     _gardenDescription: null,
	 };
     },
     created() {
	 this._alert = false;
	 this.apiGetUserData();
	 this.gardenTrack = "list";
     },
     methods: {
	 editGardenTrack: function () {
	     this.gardenTrack = "edit"
	 },	 
	 newGardenTrack: function () {
	     this.gardenTrack = "new"
	 },
	 listGardenTrack: function () {
	     this.gardenTrack = "list"
	 },
	 apiGetUserData: function () {
	     axios.get("/api/user/").then((response) => {
		 console.log(response)
		 if (response.status == 200) {
		     this._gardens = response.data.gardens;
		 }
	     })
	 },
	 sendNewGarden: function () {
	     console.log("hello")
	 },
	 sendEditGarden: function () {
	     console.log("hello")
	 },
     },
 })
</script>
