<template>
  <div>
    <el-dialog
      title="输出选项"
      width="fit-content"
      :visible.sync="dialogVisible"
      :modal="false"
    >
      <el-form>
        <!-- 文件名 -->
        <el-form-item label="文件名">
          <el-input
            v-model="fileName"
            placeholder="请输入文件名，默认为原数据集名"
          />
        </el-form-item>
        <!-- 后缀名 -->
        <el-form-item label="导出格式">
          <el-select v-model="datasetFormat" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <!-- 按钮 -->
      <div class="btn-group">
        <el-button type="primary" @click="outputFile"> 确定 </el-button>
        <el-button type="danger" @click="dialogVisible = false">
          取消
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { exportAnnotateDatasetApi } from "@/api/annotateImage";

export default {
  data() {
    return {
      dialogVisible: false,
      annotatedSet_id: 0,
      options: [
        {
          value: "voc",
          label: "voc",
        },
        {
          value: "coco",
          label: "coco",
        },
      ],
      fileName: "",
      datasetFormat: "voc",
    };
  },
  computed: {},
  methods: {
    outputFile() {
      this.dialogVisible = false;
      exportAnnotateDatasetApi(
        this.annotatedSet_id,
        this.fileName,
        this.datasetFormat
      ).then((res) => {
        const url = window.URL.createObjectURL(res);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `${this.fileName}.zip`);
        document.body.appendChild(link);
        link.click();
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.btn-group {
  margin-top: 20px;
  display: block;
}
</style>
