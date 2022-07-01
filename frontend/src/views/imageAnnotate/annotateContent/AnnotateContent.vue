<template>
  <div id="paper" class="app-container" style="overflow: scroll">
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css"
      integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u"
      crossorigin="anonymous"
    />

    <!-- 定义操作按钮 -->
    <el-row justify="center">
      <el-col style="margin-left: 40%"> <v-operate /></el-col>
      <el-col style="margin-left: 37%; margin-top: 5px">
        <el-button
          type="primary"
          plain
          @click="lastImage"
          icon="el-icon-arrow-left"
          >上一张</el-button
        >
        <el-tag type="success" style="margin: 5px" size="medium"
          >{{ imageIndex + 1 }} / {{ imageNum }}</el-tag
        >
        <el-button type="primary" plain @click="nextImage"
          >下一张<i class="el-icon-arrow-right el-icon--right"></i
        ></el-button>

        <el-button
          type="primary"
          plain
          vf
          style="margin-right: 50px"
          @click="exportData"
          >导出数据集<i class="el-icon-arrow-right el-icon-download"></i
        ></el-button>
        <output-options ref="outputOptions" />
      </el-col>
    </el-row>

    <!-- 定义一个容器 -->
    <el-container>
      <el-row type="flex">
        <!-- 标签显示 -->
        <el-aside width="240px">
          <el-col :span="25">
            <div class="panel panel-default">
              <div class="panel-heading">
                <div class="head">自定义标签</div>
                <hr />
                <div class="tip">
                  <strong>标签格式：</strong>
                  <p>&lt;标签名 &gt;(&lt;自定义快捷键 &gt;）</p>
                </div>
                <div class="tip">
                  <strong>Tips</strong>
                  <p>1. 标签选择：点击相应标签或按下自定义快捷键</p>
                  <p>
                    2.
                    矩形删除：点击删除矩形键或在选中矩形的情况下，按下Delete键
                  </p>
                  <p>3.标注保存：当前标注数据自动保存</p>
                  <p>4.导出数据集：只有所有图片都完成标注，才能导出数据集</p>
                </div>
              </div>

              <div class="panel-body">
                <div class="side">
                  <p>
                    <button
                      v-for="(info, index) in labels"
                      :key="index"
                      :style="{ backgroundColor: info.color }"
                      @click="annotateImage(index)"
                    >
                      {{ info.text }}({{ info.shortcut }})
                    </button>
                  </p>

                  <br /><br />
                  <router-link to="/labelsManage"> 添加或编辑标签 </router-link>
                </div>
              </div>
            </div>
          </el-col>
        </el-aside>

        <!-- 图片显示 -->
        <el-main style="min-width: 40%; margin-bottom: 0; magin-right: 10px">
          <el-col :offset="25">
            <div class="panel panel-default">
              <div class="panel-heading">
                <div class="head">当前标注图片</div>
              </div>
              <div id="panel-body" class="panel-body">
                <v-rect :img="img" ref="rectAnnotator" />
              </div>
            </div> </el-col
        ></el-main>
      </el-row>
    </el-container>
  </div>
</template>

<script>
import { getLabelsApi } from "@/api/annotateData";

import {
  getDatasetImageListApi,
  getAnnotateImageInfoApi,
  updateAnnotateImageInfoApi,
} from "@/api/annotateImage";
import { updateAnnotatedSetStatusApi } from "@/api/myDataset";

import OutputOptions from "./components/OutputOptions";
import operate from "./components/Operate";
import rect from "./components/Rect";

import store from "@/store/index";
import vm from "@/utils/vm";

import { mapGetters } from "vuex";

export default {
  name: "Image",
  components: {
    "v-operate": operate,
    "v-rect": rect,
    OutputOptions,
  },
  data() {
    return {
      annotatedSet_id: 0, // 当前标注数据集ID
      annotatedSet_name: "", // 当前数据集名
      annotatedSet_status: "未标注", // 当前标注数据集状态
      imageList: [], //图片id列表
      imageNum: 0, // 图片总数
      imageIndex: 0, // 当前标注的图片index
      cur_label: {}, // 当前图片的label
      rects: [], // 矩形框数据
      img: {
        // 图片信息
        name: "",
        url: "",
        width: 1920,
        height: 1080,
      },
    };
  },
  computed: {
    ...mapGetters(["labels"]), // 标签
  },
  created() {
    // 获取标签数据
    getLabelsApi().then((res) => {
      this.$store.dispatch("annotation/setLabels", res.data.labels);
    });
    // 获取数据集图片列表和其他信息
    getDatasetImageListApi(this.$route.params.id).then((res) => {
      this.$store.dispatch(
        "annotation/setAnnotatedSetInfo",
        this.$route.params.id,
        res.data.name
      );
      this.annotatedSet_id = this.$route.params.id;
      this.annotatedSet_name = res.data.name;
      this.annotatedSet_status = res.data.annotatedSet_status;
      this.imageList = res.data.image_list;
      this.imageNum = res.data.image_list.length;
      // 获取第一张图片和标注信息
      getAnnotateImageInfoApi(
        this.annotatedSet_id,
        res.data.image_list[0]
      ).then((resuslt) => {
        this.cur_label = resuslt.data.labelinfo.label;
        this.rects = resuslt.data.labelinfo.rects;
        this.img.url = resuslt.data.image;
        this.img.name = resuslt.data.name;
        this.img.width = resuslt.data.width;
        this.img.height = resuslt.data.height;
        if (JSON.stringify(resuslt.data.labelinfo.label) != "{}") {
          vm.$emit(
            "addRects",
            resuslt.data.labelinfo.rects,
            resuslt.data.height,
            resuslt.data.width,
            resuslt.data.labelinfo.label.color
          );
        } else {
          vm.$emit(
            "addRects",
            resuslt.data.labelinfo.rects,
            resuslt.data.height,
            resuslt.data.width,
            "#000000"
          );
        }
      });
    });

    // 获取矩形数据
    vm.$on("getRectData", (data) => {
      this.rects = data;
    });

    // 键盘标注，初始化即开始监听
    this.shortcutAction();
  },
  methods: {
    /**
     * : 上一张图片
     */
    lastImage() {
      if (this.imageIndex > 0) {
        //   保存当前标注，再切换
        updateAnnotateImageInfoApi(
          this.annotatedSet_id,
          this.imageList[this.imageIndex],
          this.cur_label,
          this.rects
        ).then(() => {
          if (this.imageIndex == this.imageNum - 1) {
            updateAnnotateImageInfoApi(
              this.annotatedSet_id,
              this.imageList[this.imageIndex],
              this.cur_label,
              this.rects
            );
            this.annotatedSet_status = "已标注";
            updateAnnotatedSetStatusApi(this.annotatedSet_id, "已标注");
          }
          getAnnotateImageInfoApi(
            this.annotatedSet_id,
            this.imageList[this.imageIndex - 1]
          ).then((res) => {
            this.imageIndex -= 1;
            this.img.url = res.data.image;
            this.img.name = res.data.name;
            this.img.width = res.data.width;
            this.img.height = res.data.height;
            // 恢复原本已经标注的情况
            this.cur_label = res.data.labelinfo.label;
            this.rects = res.data.labelinfo.rects;
            if (JSON.stringify(res.data.labelinfo.label) != "{}") {
              vm.$emit(
                "addRects",
                res.data.labelinfo.rects,
                this.img.height,
                this.img.width,
                res.data.labelinfo.label.color
              );
            } else {
              vm.$emit(
                "addRects",
                res.data.labelinfo.rects,
                this.img.height,
                this.img.width,
                "#000000"
              );
            }
          });
        });
      } else {
        this.$message("当前图片是第一张~");
      }
    },
    /**
     * : 下一张图片
     */
    nextImage() {
      if (this.rects.length == 0 || JSON.stringify(this.cur_label) == "{}") {
        this.$message("还没有进行标注哦~");
      } else if (this.imageIndex == this.imageNum - 1) {
        updateAnnotateImageInfoApi(
          this.annotatedSet_id,
          this.imageList[this.imageIndex],
          this.cur_label,
          this.rects
        );
        this.annotatedSet_status = "已标注";
        updateAnnotatedSetStatusApi(this.annotatedSet_id, "已标注");
        this.$message("当前图片是最后一张，标注完成~");
      } else {
        //   保存当前标注，再切换
        updateAnnotateImageInfoApi(
          this.annotatedSet_id,
          this.imageList[this.imageIndex],
          this.cur_label,
          this.rects
        ).then(() => {
          getAnnotateImageInfoApi(
            this.annotatedSet_id,
            this.imageList[this.imageIndex + 1]
          ).then((res) => {
            this.imageIndex += 1;
            this.img.url = res.data.image;
            this.img.name = res.data.name;
            this.img.width = res.data.width;
            this.img.height = res.data.height;
            // 恢复原本已经标注的情况
            this.cur_label = res.data.labelinfo.label;
            this.rects = res.data.labelinfo.rects;
            if (JSON.stringify(res.data.labelinfo.label) != "{}") {
              vm.$emit(
                "addRects",
                res.data.labelinfo.rects,
                this.img.height,
                this.img.width,
                res.data.labelinfo.label.color
              );
            } else {
              vm.$emit(
                "addRects",
                res.data.labelinfo.rects,
                this.img.height,
                this.img.width,
                "#000000"
              );
            }
          });
        });
      }
    },

    /**
     * : 数据集导出
     */
    exportData() {
      if (this.rects.length == 0 || JSON.stringify(this.cur_label) == "{}") {
        this.$message("当前图像还没有进行标注哦~");
      } else {
        updateAnnotateImageInfoApi(
          this.annotatedSet_id,
          this.imageList[this.imageIndex],
          this.cur_label,
          this.rects
        ).then(() => {
          if (this.imageIndex == this.imageNum - 1) {
            this.annotatedSet_status = "已标注";
            updateAnnotatedSetStatusApi(this.annotatedSet_id, "已标注");
            this.$refs.outputOptions.annotatedSet_id = this.annotatedSet_id;
            this.$refs.outputOptions.fileName = this.annotatedSet_name;
            this.$refs.outputOptions.dialogVisible = true;
          } else {
            if (this.annotatedSet_status == "已标注") {
              this.$refs.outputOptions.annotatedSet_id = this.annotatedSet_id;
              this.$refs.outputOptions.fileName = this.annotatedSet_name;
              this.$refs.outputOptions.dialogVisible = true;
            } else {
              this.$message("当前数据集还未完成标注，请完成标注再导出~");
            }
          }
        });
      }
    },

    /**
     *  标注图片
     * @param {number} index 标注颜色索引
     */
    annotateImage(index) {
      this.cur_label = this.$store.state.annotation.labels[index];
      vm.$emit("changeColor", `${store.state.annotation.labels[index].color}`);
    },

    /**
     *  快捷键选择标签或删除选中矩形框
     */
    shortcutAction() {
      document.onkeydown = ($event) => {
        let key = $event.key;
        if (key === "Delete") {
          // 按下Delete键删除选择矩形
          vm.$emit("deleteRect");
        } else {
          for (let j = 0; j < this.labels.length; j++) {
            if (key === this.labels[j].shortcut) {
              vm.$emit(
                "changeColor",
                `${store.state.annotation.labels[j].color}`
              );
              break;
            }
          }
        }
      };
    },
  },
  destroyed() {
    if (this.rects.length == 0 || JSON.stringify(this.cur_label) == "{}") {
      this.$message("当前图像还没有进行标注哦~");
    } else if (this.imageIndex == this.imageNum - 1) {
      updateAnnotateImageInfoApi(
        this.annotatedSet_id,
        this.imageList[this.imageIndex],
        this.cur_label,
        this.rects
      );
      updateAnnotatedSetStatusApi(this.annotatedSet_id, "已标注");
      this.$message("当前图片是最后一张，标注完成~");
    } else {
      updateAnnotateImageInfoApi(
        this.annotatedSet_id,
        this.imageList[this.imageIndex],
        this.cur_label,
        this.rects
      );
    }
  },
};
</script>

<style scoped lang="scss">
/* 因为是有固定定位，所以要有margin-top */
#paper {
  margin-top: 0px;

  /* 标注时对话框的样式 */
  .optionDialog {
    position: absolute;
    border-radius: 10px;
    background-color: rgb(147, 121, 121);
    padding: 5px;
    z-index: 10; /* 设置堆叠次序，防止被覆盖 */

    button {
      border: 1px solid black;
      margin-left: 10px;
      border-radius: 10px;
      cursor: pointer;
      outline: none;
      box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2),
        0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }
  }

  .head {
    font-size: 15px;
    color: white;
  }

  .tip {
    font-size: 10px;
    color: white;
  }

  /* 面板框样式 */
  .panel > .panel-heading {
    background-image: none;
    background-color: #3975c4;
    color: white;
    font-weight: 400;
  }

  /* 侧边栏样式 */
  .side {
    button {
      border: 1px solid black;
      margin-top: 10px;
      margin-left: 10px;
      border-radius: 10px;
      cursor: pointer;
      outline: none;
      box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2),
        0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }
  }

  /* 文本样式 */
  .annotate-content {
    margin-top: 50px;
    overflow: auto;
    flex: auto;
    min-height: 600px;
    padding: 0 5% 0 5%;
    white-space: pre-line;
    word-break: break-all;
    line-height: 25px;
    font-family: Microsoft Yahei, serif;
  }
  // 翻译卡片
  .translate-card {
    width: 200px;
    position: absolute;
    z-index: 1;

    .delete-button {
      top: 10px;
      right: -40px;
    }
  }
}
</style>
