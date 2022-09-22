<template>
    <q-layout view="lHh Lpr lFf">
	<q-page-container>
	    <div v-if="_logged_in == true">
		<div>
		    <q-btn to="/plant/new/" label="Add a new Plant" outline color="green" /><br/>
		    <q-btn to="/variety/new/" label="Add a new Variety" outline color="green" /><br/>
		    <q-btn to="/api/logout/" label="Logout" outline color="yellow" /><br/>
		</div>
		<div>
		    <h3>Recently Harvested</h3>
		    <div v-for="harvest in _recentlyHarvested" class="q-pa-md" style="max-width: 350px">
			<h5>Harvested: {{harvest.plant_name}}</h5>
			<q-list dense bordered padding class="rounded-borders">
			    <q-item>
				<q-item-section>
				    Harvested at: {{harvest.harvested_at}}
				</q-item-section>
			    </q-item>
			    
			    <q-item>
				<q-item-section>
				    Harvest Weight: {{harvest.pound}} lbs {{harvest.ounce}} oz
				</q-item-section>
			    </q-item>
			    
			    <q-item>
				<q-item-section>
				    Harvest Quantity: {{harvest.quantity}}
				</q-item-section>
			    </q-item>
			    
			    <q-item>
				<q-item-section>
				    Harvested In: {{harvest.garden_name}}
				</q-item-section>
			    </q-item>
			    
			    <q-item>
				<q-item-section>
				    Harvest Notes: {{harvest.notes}}
				</q-item-section>
			    </q-item>
			</q-list>
		    </div>
		</div>
	    </div>
	    <div v-else>
		<p>Please Log in</p>
	    </div>
	    <router-view />
	</q-page-container>
    </q-layout>
</template>

<script>
 import { defineComponent, ref } from 'vue'
 import axios from 'axios'
 
 export default defineComponent({
     name: 'HomeLayout',

     data: () => {
	 return {
	     "_logged_in": false,
	     "_recentlyHarvested": null,
	     "_harvestData": null,
	 };
     },

     components: {
     },
     created() {
	 this.apiCheckLogin();
	 this.apiGetharvestData();
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

	 apiGetharvestData: function () {
	     axios.get("/api/userharvests/").then((response) => {
		 console.log(response)
		 if (response.status == 200) {
		     this._harvestData = response.data.harvests
		     this._recentlyHarvested = response.data.harvests
		     console.log(this._harvestData)
		 }
	     })
	 },
     }

 })
</script>
