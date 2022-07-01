<template>
  <div class="operate-container">
      <el-button type="primary" plain icon="el-icon-delete" @click="deleteRect"
        >删除矩形</el-button
      >
      <el-button type="primary" plain icon="el-icon-edit" @click="toggleLine"
        >辅助线</el-button
      >
  </div>
</template>

<script>
import vm from "@/utils/vm";
export default {
  data() {
    return {
      color: "#000000",
    };
  },
  methods: {
    deleteRect() {
      vm.$emit("deleteRect");
    },
    toggleLine() {
      vm.$emit("toggleLine");
    },
  },
};
</script>

<style lang="less" scoped>
.operate-container {
  display: flex;
  flex-direction: row;
}
</style>
