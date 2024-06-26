<template>
  <div class="app-container">
    <div class="button-group-item">
      <router-link to>
        <el-button
          type="primary"
          size="small"
          icon="el-icon-back"
          style="margin-bottom: 20px"
          @click="$router.back(-1)"
        >
          返回
        </el-button>
      </router-link>
    </div>
    <!-- 表格 -->
    <el-table
      ref="singleTable"
      :data="labels"
      :row-class-name="tableRowClassName"
      style="width: 100%"
      size="mini"
      border
    >
      <!-- 标签 -->
      <el-table-column type="index" width="50" label="序号" />
      <el-table-column label="标签" min-width="200" align="center">
        <template slot-scope="scope">
          <span> {{ scope.row.text }}</span>
        </template>
      </el-table-column>

      <!-- 标签快捷键 -->
      <el-table-column label="标签快捷键" min-width="200" align="center">
        <template slot-scope="scope">
          <span> {{ scope.row.shortcut }}</span>
        </template>
      </el-table-column>

      <!-- 标签颜色 -->
      <el-table-column label="标签颜色" width="150" align="center">
        <span slot-scope="scope">
          <el-color-picker
            v-model="scope.row.color"
            show-alpha
            :predefine="$store.state.annotation.colorArray"
            @change="updateColor(scope.row.color, scope.row.id)"
          />
        </span>
      </el-table-column>
      <!-- 操作 -->
      <el-table-column align="center" width="300" label="操作">
        <span slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            icon="el-icon-edit"
            @click="updateLabelInfo(scope.row)"
          >
            编辑
          </el-button>

          <el-button
            size="small"
            type="danger"
            icon="el-icon-delete"
            @click="handleDelete(scope.row.id, scope.$index)"
          >
            删除
          </el-button>
        </span>
      </el-table-column>
    </el-table>
    <el-dialog :visible.sync="showDialog" width="30%" center>
      <EditLabel
        :is-add-label="isAddLabel"
        :label-info="labelInfo"
        @closeDialog="closeDialog"
      />
    </el-dialog>
    <!-- 添加标签 -->
    <div class="addLabelButton">
      <el-button type="primary" size="small" @click="addLabel">
        添加标签
      </el-button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import {
  getLabelsApi,
  updateLabelColorApi,
  deleteLabelApi,
} from "@/api/annotateData";
import EditLabel from "./components/EditLabel";
export default {
  name: "TableSetting",
  components: {
    EditLabel,
  },
  data() {
    return {
      showDialog: false, // 输入框的显隐
      isAddLabel: true, // 是否是添加标签,不是的话就是更新标签
      labelInfo: { text: "", color: "#ff0000", shortcut: "" }, // 添加或更新时对应标签的信息
      editCurrent: -1,
      editValue: "",
      editShortcut: "",
    };
  },
  computed: {
    ...mapGetters(["labels"]),
  },
  created() {
    getLabelsApi().then((res) => {
      this.$store.dispatch("annotation/setLabels", res.data.labels);
    });
  },
  methods: {
    /**
     * 表格样式
     */
    tableRowClassName({ row, rowIndex }) {
      row;
      if (rowIndex % 2) {
        return "even-row";
      }
      return "odd-row";
    },
    addLabel() {
      this.isAddLabel = true;
      this.showDialog = true;
    },
    /**
     * 删除标签
     * @param {number} id 当前标签id
     * @param {number} index 标签序号
     */
    handleDelete(id, index) {
      deleteLabelApi(id);
      this.labels.splice(index, 1);
    },
    /**
     * 更新标签颜色
     * @param {string} color 当前标签颜色
     * @param {number} id 当前标签id
     */
    updateColor(color, id) {
      updateLabelColorApi(id, color);
    },
    /**
     * 更新标签信息
     * @param {object} currentLabelInfo 当前标签信息
     */
    updateLabelInfo(currentLabelInfo) {
      this.labelInfo = currentLabelInfo;
      this.isAddLabel = false;
      this.showDialog = true;
    },
    /**
     * 关闭对话框
     */
    closeDialog() {
      this.showDialog = false;
      this.labelInfo = {
        text: "",
        color: "#ff0000",
        shortcut: "",
      };
    },
  },
};
</script>

<style lang="scss">
// 表格样式
.el-table .even-row {
  background: #daece9;
}
.el-table .odd-row {
  background: #f7faed;
}
.addLabelButton {
  width: 100%;
  display: flex;
  margin-top: 30px;
  justify-content: center;
}
</style>
