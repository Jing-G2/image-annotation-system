<template>
  <div>
    <div>
      <router-link to>
        <el-button
          type="primary"
          plain
          size="small"
          icon="el-icon-back"
          style="margin-left: 20px"
          @click="$router.back(-1)"
        >
          返回
        </el-button>
      </router-link>
    </div>
    <div style="margin-left: 40px">
      注意:您需要在<strong>标注之前</strong>设置好标签,在标注未完成时添加标签会<strong
        >清空标注数据</strong
      >
    </div>
    <AnnotateContent />
  </div>
</template>

<script>
import AnnotateContent from "./annotateContent/AnnotateContent";

export default {
  name: "Annotate",
  components: {
    AnnotateContent,
  },
  mounted() {
    this.isPC();
  },
  methods: {
    /**
     *  判断是否是电脑
     */
    isPC() {
      let Agents = [
        "Android",
        "iPhone",
        "Windows Phone",
        "iPad",
        "iPad Pro",
        "iPod",
      ];
      let userAgentInfo = navigator.userAgent;
      for (let v = 0; v < Agents.length; v++) {
        if (userAgentInfo.indexOf(Agents[v]) > 0) {
          this.$message.warning({
            message: "手机是无法进行标注的哦,请使用电脑浏览器。",
            duration: 5000,
            showClose: true,
          });
          break;
        }
      }
    },
  },
};
</script>
<style scoped>
* {
  box-sizing: border-box;
  color: black;
}
</style>
