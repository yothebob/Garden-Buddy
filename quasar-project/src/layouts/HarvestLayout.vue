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
	<router-view />
	
	<div v-for="item in _harvestedPlants">
	    <div>
		<input name="userplant" type="text" value=""/>
		<input name="plant" type="text" value=""/>
		<input name="quantity" type="text" value=""/>
		<input name="pound" type="text" value=""/>
		<input name="ounce" type="text" value=""/>
		<input name="notes" type="text" value=""/>
		<input name="metadata" type="text" value=""/>
	    </div>    
	</div>
	<div>
	    <button @click="AnotherHarvestedPlant">
		Track Another Plant
	    </button>
	</div>
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
	     "_harvestedPlants": null,
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
     methods: {
	 AnotherHarvestedPlant: function () {
	     this._harvestedPlants.push({
		 "userplant_id": null,
		 "plant_id": null,
		 "quantity": null,
		 "pound": null,
		 "ounce": null,
		 "notes": null,
		 "metadata": null
	     })
	 },
	 apiGetPlantData: function () {
	     axios.get("/api/plants/").then((response) => {
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
	     let user_id = 1;
	     // I think I can make an api call that checks the backend for user_id and passes that up
	     axios.get(`/api/user/user_id=${user_id}`).then((response) => {
		 console.log(response);
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
