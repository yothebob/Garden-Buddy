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
		      <h3>List Gardens</h3><br/>
		      <div v-for="gg in _gardens" class="q-pa-md">
			  <q-list dense bordered padding class="rounded-borders">
			      <q-item>
				  <q-item-section>
				      <q-item-label>{{gg.label}}</q-item-label>
				      <q-item-label caption lines="2">{{gg.description}}</q-item-label>
				  </q-item-section>
				  
				  
				  <q-item-section side top>
					  <q-item-label caption>Fav</q-item-label>
				      <q-icon name="star" color="yellow" />
				  </q-item-section>
				      <q-item-section side top>
					  <q-item-label caption>Delete</q-item-label>
					  <q-icon @click="apiDeleteItem('user_gardens', gg.value)" name="warning" color="red" />
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
		      
		      <q-input rounded outlined v-model="_gardenHeight"
			       @update:model-value="UpdateGardenSize()"
			       label="Garden Width" /><br/>
		      <q-input rounded outlined v-model="_gardenWidth"
			       @update:model-value="UpdateGardenSize()"
			       label="Garden Height" /><br/>
		      

		      <div id="garden-box" style="display: flex;justify-content: space-evenly;">
		      </div>

		      <q-btn @click="sendNewGarden" color="white" text-color="black" label="Add Garden" />
		      
		  </div>
		  <div v-else>
		    <h3>Edit Garden</h3><br/>
		      
		    <q-select rounded outlined v-model.number="_gardenId" :options="_gardens" emit-value label="Which Garden?" /><br/>
		      
		  <q-input rounded outlined v-model="_gardenName" label="Garden Name" />
		  <br/>
		  
		  <q-input
		      v-model="_gardenDescription"
		      filled
		      autogrow
		      label="Description"
		  />
		  <br/>
		  
		  <q-btn @click="sendEditGarden" color="white" text-color="black" label="Edit Garden" />
		  
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
	     _gardenId: null,
	     userId: null,
	     gardenTrack: null,
	     _gardens: null,
	     _alert: null,
	     _message: null,
	     _gardenName: null,
	     _gardenDescription: null,
	     _gardenWidth: null,
	     _gardenHeight: null,
	 };
     },

     created() {
	 this._gardenWidth = 0;
	 this._gardenHeight = 0;
	 this.apiCheckLogin();
	 this._alert = false;
	 this.apiGetUserData();
	 this.gardenTrack = "list";
     },

     methods: {
	 createRow: function (idName, parentId, tag) {
	     const newDiv = document.createElement(tag);
	     newDiv.id = idName
	     /* newDiv.style.display = "inline-block" */
	     const parentDiv = document.getElementById(parentId);
	     parentDiv.append(newDiv)
	 },

	 createDiv: function (idName, content, parentId, tag) {
	     const newDiv = document.createElement(tag);
	     if (tag == "div") {
		 newDiv.innerText = content;
	     }
	     newDiv.id = idName
	     const parentDiv = document.getElementById(parentId);
	     parentDiv.append(newDiv)
	 },

	 UpdateGardenSize: function () {
	     if ((!isNaN(this._gardenWidth) && !isNaN(this._gardenHeight)) && (this._gardenHeight > 0 && this._gardenWidth > 0)) {
		 let startId = "row_0"
		 let prevIdStr = ""
		 let strId = ""
		 document.getElementById("garden-box").innerHTML = "";
		 for (let i = 0 ; i < this._gardenHeight; i++) {
		     prevIdStr = `row_${i}`
		     this.createRow(prevIdStr, "garden-box", "div")		     
		     for (let ii = 0 ; ii < this._gardenWidth; ii++) {
			 strId = `${i}__${ii}`
			 if (document.getElementById(strId) == null) {
			     this.createDiv(strId, "t", prevIdStr, "div")
			 } 
		     }
		     this.createDiv(`garden_${i}_br`, "", "garden-box", "br")
		 }
	     }
	 },

	 editGardenTrack: function () {
	     this.gardenTrack = "edit"
	 },	 

	 newGardenTrack: function () {
	     this.gardenTrack = "new"
	 },

	 listGardenTrack: function () {
	     this.gardenTrack = "list"
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

	 apiDeleteItem: function (dataType, itemId) {
	     axios.get(`/api/delete/${dataType}/${itemId}`).then((response) => {
		 if (response.status == 200 && response.data.status == 200) {
		     this._alert = true
		     this._message = response.data.message;
		 } else {
		     this._alert = true
		     this._message = response.data.message;
		 }
	     })
	 },

	 apiGetUserData: function () {
	     axios.get("/api/user/").then((response) => {
		 console.log(response)
		 if (response.status == 200) {
		     this._gardens = response.data.gardens;
		     this.userId = response.data.user_id;
		 }
	     })
	 },
	 sendNewGarden: function () {
	     let date = new Date();
	     let dateString = String(((date.getMonth() > 8) ? (date.getMonth() + 1) : ('0' + (date.getMonth() + 1))) + '/' + ((date.getDate() > 9) ? date.getDate() : ('0' + date.getDate())) + '/' + date.getFullYear());

	     let newGardenPost = {
		 "user_id": this.userId,
		 "date": dateString,
		 "name": this._gardenName,
		 "description": this._gardenDescription,
		 "layout": "coming soon",
		 "metadata": "coming soon"
	     }
	     axios.post("/api/garden/new",newGardenPost).then((response) => {
		 console.log(response)
		 if (response.status == 200) {
		     this._alert = true
		     this._message = response.data.message;
		     this.listGardenTrack()
		 }
	     })
	 },
	 sendEditGarden: function () {
	     let date = new Date();
	     let dateString = String(((date.getMonth() > 8) ? (date.getMonth() + 1) : ('0' + (date.getMonth() + 1))) + '/' + ((date.getDate() > 9) ? date.getDate() : ('0' + date.getDate())) + '/' + date.getFullYear());

	     let updateGardenPost = {
		 "garden_id": this._gardenId,
		 "date": dateString,
		 "name": this._gardenName,
		 "description": this._gardenDescription,
		 "layout": "coming soon",
		 "metadata": "coming soon"
	     }
	     axios.post("/api/garden/update",updateGardenPost).then((response) => {
		 console.log(response)
		 if (response.status == 200) {
		     this._alert = true
		     this._message = response.data.message;
		     this.listGardenTrack()
		 }
	     })
	 },
     },
 })
</script>
<style>
 div.garden-box {
     display: flex;
     justify-content: space-evenly;
 }

 
</style>
