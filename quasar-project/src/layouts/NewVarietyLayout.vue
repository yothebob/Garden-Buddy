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
	<div style="position:relative;padding-left:45%;">
	    <h3>Add New Variety</h3>
	    <br/>
	    <label for="plantSelect">Plant Type</label><br/>
	    <select id="plant-select" name="plantSelect" v-model="_plantId"><br/>
		<option v-for="pl in _plants" value="{{pl.id}}">{{pl.name}}</option>
	    </select>
	    <br/>
	    <label for="varietyName">Variety Name</label><br/>
	    <input name="varietyName" type="text" value="" v-model="_varietyName" />
	    <br/>
	    <label for="">Variety Description</label><br/>
	    <textarea cols="30" id="" name="" rows="10" v-model="_varietyDescription"></textarea>
	    <br/>
	    <label for="">Variety Info Url</label><br/>
	    <input name="" type="text" value="" v-model="_varietyInfoUrl" />
	    <br/>
	    <button @click="sendNewVariety">Add Variety</button>
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
	 link: '/garden/new/'
     },
     {
	 title: 'My Plants',
	 caption: 'Track any data you want with custom plants!',
	 icon: 'code',
	 link: '/userplant/new/'
     },
     {
	 title: 'Harvests',
	 caption: 'Add a new harvest for the day',
	 icon: 'chat',
	 link: '/harvest/new/'
     },
 ]

 export default defineComponent({
     name: 'NewVarietyLayout',

     components: {
	 EssentialLink
     },

     data: () => {
	 return {
	     _message: null,
	     _plants: [],
	     _plantId: null,
	     _varietyName: null,
	     _varietyDescription: null,
	     _varietyInfoUrl: null
	 };
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
	 this.apiGetPlantData();
     },

     methods: {
	 sendNewVariety: function () {
	     let _newVarietyData = {
		 "plant_id": this._plantId,
		 "name": this._varietyName,
		 "description": this._varietyDescription, 
		 "info_url": this._varietyInfoUrl 
	     };
	     
	     axios.post(`/api/variety/new`, _newVarietyData).then((response) => {
		 if (response.status === 200) {
		     this._message = "Save Successful"
		     // should I just have this on a generic Variety page? 
		     window.location.href = '/home/'
		 } else {
		     /* this._message = "Uh Oh Something went wrong!" */
		     this._message = "Uh Oh Something went wrong!"
		 }
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

     }

 })
</script>
