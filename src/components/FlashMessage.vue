<template>
  <div>
    <b-alert :variant="variant" show>{{ message }}</b-alert>
  </div>
</template>

<script>
export default {
  props: ['message','variant'],
};
</script>