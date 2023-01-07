<template>
    <q-layout view="lHh Lpr lFf">
	<div v-if="_logged_in == true">
	    <div>
		<h3>Harvest Data</h3>
		<br/>
		<br/>
		<newHarvestTable
		    :propRows="rows"
		></newHarvestTable>
	    </div>
	<div class="app-content">
	    <q-page-container>
		<h3>Export Data</h3>
		<div>
		    <q-btn @click="apiExportHarvests('csv')" label="Export Harvests csv" outline color="red" /><br/>
		    <!-- <q-btn @click="apiExportHarvests('xlsx')" label="Export Harvests xlsx" outline color="red" /><br/> -->
		</div>
	    </q-page-container>
	</div>
	</div>
    </q-layout>
</template>

<script>
 import { defineComponent } from 'vue'
 import axios from 'axios'
 import newHarvestTable from "../components/newHarvestTable.vue";
 
 export default defineComponent({
     name: 'ExportPage',
     
     data: () => {
	 return {
	     "_logged_in": true,
	     "rows": []
	 };
     },
     components: {
	 newHarvestTable
     },
     created() {
	 this.apiCheckLogin();
	 this.apiGetharvestData();
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
	 apiGetharvestData: async function() {
	     const url = "/api/userharvests/";
	     const res = await fetch(url, {
		 method: "GET",
		 headers: {'Content-Type': 'application/json'}
	     })
	     const json = await res.json();
	     this.rows = json.harvests;
	 },
     }
 })
</script>
