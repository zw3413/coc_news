<template>
  <el-container>
    <el-header>听见花开ListenFlower</el-header>
    <el-container>
      <el-aside width="200px">
        <Aside/>
       
      </el-aside>
      <el-container>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>
<script>
import Aside from "./Aside";
export default {
  name: "Admin",
  components: {
    Aside
  },
  data: function() {
    return {
     
    };
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    }
  }
};
</script>
<style>
.el-header,
.el-footer {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-container {
  height: calc( 100% - 0px);
  overflow-y: hidden;
}

</style>