<script setup>
 import { ref } from 'vue';
 const props = defineProps({
     propTitle: {
	 type: String,
	 default: "Garden Data",
	 description: "the title"
     },
     propRows: {
	 type: Array,
	 description: "a list of the rows"
     }
 });

 const columns = [
     {
	 name: "Harvested At",
	 label: "Harvested At",
	 align: "center",
	 field: "harvested_at",
	 sortable: true
     },
     {
	 name: "Plant Name",
	 label: "Plant Name",
	 align: "center",
	 field: "plant_name",
	 sortable: true
     },
     {
	 name: "Userplant Name",
	 label: "Userplant Name",
	 align: "center",
	 field: "userplant_name",
	 sortable: true
     },
     {
	 name: "Garden Name",
	 label: "Garden Name",
	 align: "center",
	 field: "garden_name",
	 sortable: true
     },
     {
	 name: "Quantity",
	 label: "Quantity",
	 align: "center",
	 field: "quantity",
	 sortable: true
     },
     {
	 name: "Pound",
	 label: "Pound",
	 align: "center",
	 field: "pound",
	 sortable: true
     },
     {
	 name: "Ounce",
	 label: "Ounce",
	 align: "center",
	 field: "ounce",
	 sortable: true
     },
     {
	 name: "Notes",
	 label: "Notes",
	 align: "center",
	 field: "notes",
     }
 ]

</script>
<template>
    <q-table
	:title="propTitle"
	:rows="propRows"
	:columns="columns"
	row-key="name"
    />
</template>
