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
	    <h3> Add New Plant</h3><br/>
	    <label for="plantName">Plant Name</label><br/>
	    <input name="plantName" type="text" value="" v-model="_plantName" /><br/>
	    <label for="plantDescription">Plant Description</label><br/>
	    <textarea cols="30" id="" name="plantDescription" rows="10" v-model="_plantDescription"></textarea><br/>
	    <label for="plantInfoUrl">Plant Info Url</label><br/>
	    <input name="plantInfoUrl" type="text" value=""/><br/>
	    <button @click="sendNewPlant"> Add Plant</button>
	</div>
	<div v-if="_message != null">
	    <h5>{{_message}}</h5>
	</div>
	<!-- <div></div> if successful save -->
	<!-- <div></div> not successful save -->
	
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
     name: 'NewPlantLayout',

     components: {
	 EssentialLink
     },

     data: () => {
	 return {
	     _message: null,
	     _plantName: null,
	     _plantDescription: null,
	     _plantInfoUrl: null
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
     },
     methods: {
	 sendNewPlant: function () {
	     let _newPlantdata = {
		 "name": this._plantName,
		 "description": this._plantDescription, 
		 "info_url": this._plantInfoUrl 
	     };
	     
	     axios.post(`/api/plant/new`, _newPlantdata).then((response) => {
		 if (response.status === 200) {
		     this._message = "Save Successful"
		     // should I just have this on a generic plant page? 
		     window.location.href = '/home/'
		 } else {
		     /* this._message = "Uh Oh Something went wrong!" */
		     this._message = "Uh Oh Something went wrong!"
		 }
	     })
	 },
     }
 })
</script>
