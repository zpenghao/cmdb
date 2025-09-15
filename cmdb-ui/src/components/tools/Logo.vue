<template>
  <div class="logo">
    <div v-if="showTitle && !collapsed" @click="jumpTo" style="cursor: pointer;display: flex;align-items: center;justify-content: center;">
      <img
        style="width: 30px; height: 100%;"
        :src="require('@/assets/logo-new.png')"
      />
      <span>一站式智能运维平台</span>
    </div>
    <img
      @click="jumpTo"
      v-else
      style="width: 32px; height: 32px; margin-left: 24px; cursor: pointer"
      :src="require('@/assets/logo-new.png')"
    />
  </div>
</template>

<script>
export default {
  name: 'Logo',
  components: {},
  computed: {},
  props: {
    title: {
      type: String,
      default: 'OneOps',
      required: false,
    },
    showTitle: {
      type: Boolean,
      default: true,
      required: false,
    },
    collapsed: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  methods: {
    jumpTo() {
      if (this.$route.path !== '/cmdb/dashboard') {
        this.$router.push('/cmdb/dashboard')
      }
    },
  },
}
</script>
