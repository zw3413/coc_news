<template>
  <el-menu
    default-active="1"
    class="el-menu-vertical-demo"
    @open="handleOpen"
    @close="handleClose"
    mode="vertical"
  >
    <sidebar-item v-for="route in routes" :key="route.path" :item="route" :base-path="route.path" />
  </el-menu>
</template>
<script>
import SidebarItem from "./SidebarItem.vue";
export default {
  name: "Aside",
  components: {
    SidebarItem
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    }
  },
  computed: {
    routes() {
      var r=[];
      this.$router.options.routes.forEach((v)=>{
        console.log(v.path)
        if(v.path.indexOf("/admin")==0){
          r.push(v)
        }
      })
      return r;
    }
  }
};
</script>
<style scoped>
</style>