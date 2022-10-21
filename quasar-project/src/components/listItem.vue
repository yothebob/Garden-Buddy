<template>
	<q-item-section>
	    <q-item-label>{{label}}</q-item-label>
	    <q-item-label caption lines="2">{{description}}</q-item-label>
	</q-item-section>
	
	<q-item-section side top>
	    <q-item-label caption>Fav</q-item-label>
	    <q-icon name="star" color="yellow" />
	</q-item-section>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'listItem',
  props: {
    label: {
      type: String,
      required: true
    },
    description: {
      type: String,
      default: ''
    }
  }
})
</script>
