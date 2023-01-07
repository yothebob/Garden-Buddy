<template>
    <q-layout view="lHh Lpr lFf">
	<div class="app-content">
	    <q-page-container>
		<div v-if="_logged_in == true">
		    <h3>Harvests</h3>
		    <div>
			<q-btn @click="apiExportHarvests('csv')" label="Export Harvests csv" outline color="red" /><br/>
			<!-- <q-btn @click="apiExportHarvests('xlsx')" label="Export Harvests xlsx" outline color="red" /><br/> -->
		    </div>
		</div>
	    </q-page-container>
	</div>
    </q-layout>
</template>

<script>
 import { defineComponent } from 'vue'
 import axios from 'axios'
 
 export default defineComponent({
     name: 'ExportPage',
     
     data: () => {
	 return {
	     "_logged_in": true,
	 };
     },

     created() {
	 this.apiCheckLogin();
     },

     methods: {
	 apiExportHarvests: function (exportType) {
	     location.href = "/api/export_data/" + exportType
	 },
	 
	 apiCheckLogin: function () {
	     axios.get("/api/who-am-i/").then((response) => {
		 console.log(response)
		 if (response.status == 200 && response.data.status == 200) {
		     this._logged_in = true;
		 } else {
		     this._logged_in = false;
		     window.location.href = "/login";
		 }
	     })
	 },
     }
 })
</script>
