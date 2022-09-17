<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
	<q-toolbar>
            <q-btn
		flat
		dense
		round
		icon="menu"
		aria-label="Menu"
		@click="toggleLeftDrawer"
            />

            <q-toolbar-title>
		Garden Buddy
            </q-toolbar-title>

	</q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
	    GardenBuddy
        </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
	<div v-for="item in _harvestedPlants">
	    <div style="display">
		<div>
		    <h3>What Kind of plant?</h3>
		    <label for="userplant">Tracked Plant</label>
		    <input id="up-radio" name="userplant" type="radio" value=""/>
		    <label for="plant">Generic Plant</label>
		    <input id="p-radio" name="plant" type="radio" value=""/>
		</div>
		<br/>
		<select id="userplant-select" name="userplant">
		    <option v-for="up in _userPlants" value="{{up.id}}">{{up.name}}</option>
		</select>

		<select id="plant-select" name="plant">
		    <option v-for="pl in _plants" value="{{pl.id}}">{{pl.name}}</option>
		</select>

		<input name="plant" type="text" value=""/> 

		<div>
		    <input name="quantity" type="text" value="{{item.quantity}}"/>
		    <button>/\</button>
		    <button>\/</button>
		    <br/>
		</div>

		<div>
		    <input name="pound" type="text" value="{{item.pound}}"/>
		    <button>/\</button>
		    <button>\/</button>
		    <br/>
		</div>
		
		<div>
		    <input name="ounce" type="text" value="{{item.ounce}}"/>
		    <button>/\</button>
		    <button>\/</button>
		    <br/>
		</div>

		<input name="notes" type="text" value=""/>
		<input name="metadata" type="text" value=""/>
	    </div>    
	</div>
	<div>
	    <button @click="AnotherHarvestedPlant">
		Track Another Plant
	    </button>
	</div>

	<router-view />
	
    </q-page-container>
  </q-layout>
</template>

<script>
 import { defineComponent, ref } from 'vue'
 import EssentialLink from 'components/EssentialLink.vue'
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
	     "_userData": null,
	     "_harvestedPlants": [],
	     "_plants": null,
	     "_gardens": null,
	     "_varietys": null,
	     "_userPlants": null,
	 };
     },
     components: {
	 EssentialLink
     },
     setup () {
	 const leftDrawerOpen = ref(false)
	 
	 return {
	     essentialLinks: linksList,
	     leftDrawerOpen,
	     toggleLeftDrawer () {
		 leftDrawerOpen.value = !leftDrawerOpen.value
	     }
	 }
     },
     created() {
	 this.AnotherHarvestedPlant();
	 this.apiGetPlantData();
	 console.log(this.apiGetUserData());
	 console.log("harvestedplants", this._harvestedPlants)
     },
     methods: {
	 AnotherHarvestedPlant: function () {
	     this._harvestedPlants.push({
		 "userplant_id": 0,
		 "plant_id": 0,
		 "quantity": 0,
		 "pound": 0,
		 "ounce": 0,
		 "notes": "",
		 "metadata": ""
	     })
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
	 printme: function () {
	     /* TODO add jwt */
	     axios.post(`/api/login/?username=${this._username}&password=${this._password}`, {}).then((response) => {
		 if (response.status === 200) {
		     window.location.href = '/home/'
		 }
	     })
	 }
     }
 })
</script>
