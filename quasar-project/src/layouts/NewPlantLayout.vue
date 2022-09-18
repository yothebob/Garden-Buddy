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
	<div>
	    <h3>Add New Plant</h3><br/>
	    
	    <q-input rounded outlined v-model="_plantName" label="Plant Name" />
	    <br/>

	    <q-input
		v-model="_plantDescription"
		filled
		autogrow
		label="Description"
	    />
	    <br/>
	    
	    <q-input rounded outlined v-model="_plantInfoUrl" label="Plant Info Url" />
	    <br/>
	    
	    <q-btn @click="sendNewPlant" color="white" text-color="black" label="Add Plant" />

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
	     _alert: null,
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
		     
		     this._alert = true
		     this._message = "Save Successful"
		     // should I just have this on a generic plant page? 
		     /* window.location.href = '/home/' */
		 } else {
		     this._alert = true
		     this._message = "Uh Oh Something went wrong!"
		 }
	     })
	 },
     }
 })
</script>
