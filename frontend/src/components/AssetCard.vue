<template>
  <v-card>
    <v-card-title>{{ asset.name }}</v-card-title>
    <v-card-subtitle>Инв. № {{ asset.inventory_number }}</v-card-subtitle>
    <v-card-text>
      <div>Стоимость: {{ formatCurrency(asset.current_cost) }}</div>
      <div>Статус: {{ asset.status }}</div>
      <div>Ответственный: {{ asset.responsible?.name || 'Не назначен' }}</div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ['asset'],
  methods: {
    formatCurrency(value) {
      return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB'
      }).format(value);
    }
  }
}
</script>
