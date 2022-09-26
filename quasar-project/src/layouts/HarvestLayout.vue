<template>
    <q-layout view="lHh Lpr lFf">
	<q-page-container>
	    <div class="app-content">
		<q-item v-for="hp in totalHarvestedPlants" :key="hp">
		    <div>
			<h3>What Kind of plant?</h3>
			<div>
			    <q-radio v-model.string="_harvestedPlants[hp].plantType" checked-icon="task_alt" unchecked-icon="panorama_fish_eye" val="userplant" label="Tracked Plant" />
			    <q-radio v-model.string="_harvestedPlants[hp].plantType" checked-icon="task_alt" unchecked-icon="panorama_fish_eye" val="plant" label="Plant" />
			    <br/>
			</div>
			<div v-if="_harvestedPlants[hp].plantType == 'plant'">
			    <q-select rounded outlined v-model.number="_harvestedPlants[hp].plant_id" :options="_plants" emit-value label="Plant Name" />
			    <br/>
			</div>
			<div v-else >
			    <q-select rounded outlined v-model.number="_harvestedPlants[hp].userplant_id" :options="_userPlants" emit-value label="Tracked Plant Name" />
			    <br/>
			</div>
			
			<q-select rounded outlined v-model.number="_harvestedPlants[hp].garden_id" :options="_gardens" emit-value label="Which Garden?" /><br/>
			<q-input rounded outlined v-model.number="_harvestedPlants[hp].quantity" label="Quantity" /><br/>
			<q-input rounded outlined v-model.number="_harvestedPlants[hp].pound" label="Pound" /><br/>
			<q-input rounded outlined v-model.number="_harvestedPlants[hp].ounce" label="Ounce" /><br/>
			<q-input
			    v-model.string="_harvestedPlants[hp].notes"
			    filled
			    autogrow
			    label="Notes"
			/>
			<br/>
			
			<q-btn @click="AnotherHarvestedPlant" color="white" text-color="black" label="Track Another Plant" /><br/>
		    </div>
		    <q-btn @click="submitHarvest" color="white" text-color="black" label="Submit Harvest" /><br/>
		    
		</q-item>
		
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
	    </div>
	</q-page-container>
      </q-layout>
</template>

<script>
 import { defineComponent, ref } from 'vue'
 import axios from 'axios'
 
 const linksList = [
     {
	 title: 'Home',
	 caption: 'My Home Page',
	 icon: 'school',
	 link: '/home/'
     },
     {
	 title: 'Gardens',
	 caption: 'View, create and update my gardens',
	 icon: 'school',
	 link: '/gardens/'
     },
     {
	 title: 'My Plants',
	 caption: 'Track any data you want with custom plants!',
	 icon: 'code',
	 link: '/userplants/'
     },
     {
	 title: 'Harvests',
	 caption: 'Add a new harvest for the day',
	 icon: 'chat',
	 link: '/harvests/'
     },
 ]

 export default defineComponent({
     name: 'HarvestLayout',
     data: () => {
	 return {
	     "_alert": null,
	     "_message": null,
	     "_userData": null,
	     "_harvestedPlants": [],
	     "totalHarvestedPlants": null,
	     "_plants": null,
	     "_gardens": null,
	     "_varietys": null,
	     "_userPlants": null,
	 };
     },
     created() {
	 this.apiCheckLogin();
	 this.totalHarvestedPlants = 0;
	 this.AnotherHarvestedPlant();
	 this._harvestedPlants.push({
	     "plantType": "",
	     "userplant_id": 0,
	     "garden_id": 0,
	     "plant_id": 0,
	     "quantity": 0,
	     "pound": 0,
	     "ounce": 0,
	     "notes": "",
	     "metadata": ""
	 })

	 this.apiGetPlantData();
	 console.log(this.apiGetUserData());
	 console.log("harvestedplants", this._harvestedPlants)
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

	 AnotherHarvestedPlant: function () {
	     this.totalHarvestedPlants = this.totalHarvestedPlants + 1;
	     this._harvestedPlants.push({
		 "userplant_id": 0,
		 "garden_id": 0,
		 "plant_id": 0,
		 "quantity": 0,
		 "pound": 0,
		 "ounce": 0,
		 "notes": "",
		 "metadata": ""
	     })
	 },
	 submitHarvest: function() {
	     // for now the first index of the array seems to be blank? here is the fix, remove if doesnt nwork
	     this._harvestedPlants.shift();
	     var date = new Date();
	     let dateString = String(((date.getMonth() > 8) ? (date.getMonth() + 1) : ('0' + (date.getMonth() + 1))) + '/' + ((date.getDate() > 9) ? date.getDate() : ('0' + date.getDate())) + '/' + date.getFullYear())
	     let sendData = {
		 "user_id": this._userData.user_id,
		 "date": dateString,
		 "harvested": this._harvestedPlants
	     }
	     console.log("sendData",sendData)
	     axios.post('/api/harvest/', sendData).then((response) => {
		 if (response.status === 200) {
		     console.log(response)
		     this._alert = true
		     this._message = "Save Successful"
		 } else {
		     this._alert = true
		     this._message = "Uh Oh Something went wrong!"
		 }
	     }) // put error here.. if i remember
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
	     axios.get(`/api/varietys/plant_id=${given_plant_id}`).then((response) => {
		 console.log(response);
	     })
	 },
	 apiGetUserData: function () {
	     /* TODO add jwt */
	     // I think I can make an api call that checks the backend for user_id and passes that up
	     axios.get(`/api/user/`).then((response) => {
		 console.log(response);
		 if (response.status == 200) {
		     this._userPlants = response.data.user_plants;
		     this._gardens = response.data.gardens;
		     this._userData = response.data;
		 }
	     })
	 },
     }
 })
</script>
